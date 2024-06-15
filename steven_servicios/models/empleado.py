# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Empleado(models.Model):
    _name = 'empleado'
    _description = _('Employee')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(_('Employee Code'), readonly=True, required=True, default="New", help=_("Employee's code"))
    name = fields.Char(_('Name'), required=True, tracking=True, help=_("Employee's name"))
    last_name = fields.Char(_('Last Name'), required=True, tracking=True, help=_("Employee's last name"))
    dni_emp = fields.Char(_('ID'), required=True, tracking=True, help=_("Employee's nacional identification number"))
    phone_number = fields.Char(_('Phone Number'), required=True, tracking=True, help=_("Employee's phone number"))
    date = fields.Date(_('Contract Date'), required=True, tracking=True, help=_("Employee's contract date"))
    cita_ids = fields.One2many('cita', 'emp_code', string='Citas')

    """ @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            name_lower = record.code.lower()
            existing_records = self.env['empleado'].search([
                ('code', 'ilike', record.code),
                ('id', '!=', record.id)
            ])
            for rec in existing_records:
                if rec.code.lower() == name_lower:
                    _logger.error("Duplicate Code found: %s", record.code)
                    raise ValidationError(_("The Employee code must be unique.")) """
    
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_employee = self.search([], order='id desc', limit=1)
            if last_employee and last_employee.code:
                last_code = last_employee.code
                last_number = int(last_code[3:])
                new_number = last_number + 1
                new_code = 'EMP' + str(new_number).zfill(3)
            else:
                new_code = 'EMP001'
            vals['code'] = new_code
        return super(Empleado, self).create(vals)