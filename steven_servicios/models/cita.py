# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Cita(models.Model):
    _name = 'cita'
    _description = _('Appointment')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(_('Appointment Code'), readonly=True, required=True, default="New", help=_("Appointment Code"))
    cli_code = fields.Many2one('cliente', string=_('Client'), required=True, tracking=True, help=_("Client Code"))
    cliente_last_name = fields.Char(string=_('Last Name'), related='cli_code.last_name', readonly=True)
    ser_code = fields.Many2one('servicio', string=_('Service'), required=True, tracking=True, help=_("Service Code"))
    emp_code = fields.Many2one('empleado', string=_('Employee'), required=True, tracking=True, help=_("Employee Code"))
    cita_date = fields.Datetime(_("Date"), required=True, tracking=True, help=_("Appointment Date and Time"))
    cita_status = fields.Selection(
        [('overdue', 'Overdue'), ('today', 'Today'), ('future', 'Future')],
        string=_("Status"), compute='_compute_cita_status', store=True)
    active = fields.Boolean(string=_('Active'), default=True)

    @api.depends('cita_date')
    def _compute_cita_status(self):
        for record in self:
            if record.cita_date:
                now = datetime.now()
                cita_date = fields.Datetime.from_string(record.cita_date)
                if cita_date.date() == now.date():
                    record.cita_status = 'today'
                elif cita_date < now:
                    record.cita_status = 'overdue'
                else:
                    record.cita_status = 'future'
    
    @api.model
    def update_cita_statuses(self):
        citas = self.search([])
        for cita in citas:
            cita._compute_cita_status()

    """ @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            code_lower = record.code.lower()
            existing_records = self.env['cita'].search([
                ('code', 'ilike', record.code),
                ('id', '!=', record.id)
            ])
            for rec in existing_records:
                if rec.code.lower() == code_lower:
                    _logger.error("Duplicate Code found: %s", record.code)
                    raise ValidationError(_("The Appointment code must be unique.")) """
    
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_appointment = self.search([], order='id desc', limit=1)
            if last_appointment and last_appointment.code:
                last_code = last_appointment.code
                last_number = int(last_code[3:])
                new_number = last_number + 1
                new_code = 'APP' + str(new_number).zfill(3)
            else:
                new_code = 'APP001'
            vals['code'] = new_code
        return super(Cita, self).create(vals)

    @api.constrains('cita_date', 'emp_code')
    def _check_unique_appointment(self):
        for appointment in self:
            if appointment.emp_code and appointment.cita_date:
                same_time_appointments = self.search([
                    ('emp_code', '=', appointment.emp_code.id),
                    ('cita_date', '=', appointment.cita_date),
                    ('id', '!=', appointment.id)
                ])
                if same_time_appointments:
                    raise ValidationError(_("This employee already has an appointment at this time."))
                
    @api.constrains('cita_date')
    def _check_appointment_interval(self):
        for appointment in self:
            if appointment.cita_date:
                same_employee_appointments = self.search([
                    ('emp_code', '=', appointment.emp_code.id),
                    ('cita_date', '>=', appointment.cita_date - timedelta(minutes=45)),
                    ('cita_date', '<=', appointment.cita_date + timedelta(minutes=45)),
                    ('id', '!=', appointment.id)
                ])
                if same_employee_appointments:
                    raise ValidationError(_("Employee must have at least 45 minutes between appointments."))