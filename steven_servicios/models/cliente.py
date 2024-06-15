# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Cliente(models.Model):
    _name = 'cliente'
    _description = _('Client')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(_('Client Code'), readonly=True, required=True, default="New", help=_("Client's code"))
    name = fields.Char(_('Name'), required=True, tracking=True, help=_("Client's name"))
    last_name = fields.Char(_('Last Name'), required=True, tracking=True, help=_("Client's last name"))
    dni_cli = fields.Char(_('ID'), tracking=True, help=_("Client's nacional identification number"))
    phone_number = fields.Char(_('Phone Number'), required=True, tracking=True, help=_("Client's phone number"))
    date = fields.Date(_('Registration Date'), required=True, tracking=True, help=_("Client's registration date"))
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], _('Priority'), default='0', index=True)
    cita_ids = fields.One2many('cita', 'cli_code', string='Citas')

    """ @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            name_lower = record.code.lower()
            existing_records = self.env['cliente'].search([
                ('code', 'ilike', record.code),
                ('id', '!=', record.id)
            ])
            for rec in existing_records:
                if rec.code.lower() == name_lower:
                    _logger.error("Duplicate Code found: %s", record.code)
                    raise ValidationError(_("The Client code must be unique.")) """
                
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_client = self.search([], order='id desc', limit=1)
            if last_client and last_client.code:
                last_code = last_client.code
                last_number = int(last_code[3:])
                new_number = last_number + 1
                new_code = 'CLI' + str(new_number).zfill(3)
            else:
                new_code = 'CLI001'
            vals['code'] = new_code
        return super(Cliente, self).create(vals)