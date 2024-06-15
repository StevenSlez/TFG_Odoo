# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Servicio(models.Model):
    _name = 'servicio'
    _description = _('Service')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(_('Service Code'), readonly=True, required=True, default="New", help=_("Service code"))
    name = fields.Char(_('Name'), required=True, tracking=True, help=_("Service name"))
    price = fields.Monetary(_('Price'), currency_field='currency_id', required=True, tracking=True, help=_("Service prices"))
    descr = fields.Char(_('Description'), required=True, tracking=True, help=_("Description of the service"))
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, tracking=True, default=lambda self: self.env.company.currency_id)

    """ @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            name_lower = record.code.lower()
            existing_records = self.env['servicio'].search([
                ('code', 'ilike', record.code),
                ('id', '!=', record.id)
            ])
            for rec in existing_records:
                if rec.code.lower() == name_lower:
                    _logger.error("Duplicate Code found: %s", record.code)
                    raise ValidationError(_("The Service code must be unique.")) """
    
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_service = self.search([], order='id desc', limit=1)
            if last_service and last_service.code:
                last_code = last_service.code
                last_number = int(last_code[3:])
                new_number = last_number + 1
                new_code = 'SER' + str(new_number).zfill(3)
            else:
                new_code = 'SER001'
            vals['code'] = new_code
        return super(Servicio, self).create(vals)