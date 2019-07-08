# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.depends('partner_id')
    def _compute_all_partner_tickets(self):
        self.ensure_one()
        ticket_data = self.env['helpdesk.ticket'].read_group([
            ('partner_id', '=', self.partner_id.id)
        ], ['partner_id'], ['partner_id'])
        if ticket_data:
            self.all_partner_tickets = ticket_data[0]['partner_id_count']

    @api.depends('partner_id')
    def _compute_passwords_count(self):
            for helpdeskticket in self:
                if helpdeskticket.partner_id:
                    helpdeskticket.passwords_count = len(self.env['res.partner.passwords'].search([('partner_id', 'child_of', [helpdeskticket.partner_id.id])]))
                else:
                    helpdeskticket.passwords_count = 0

    passwords_count = fields.Integer(compute='_compute_passwords_count', string=_('Contraseñas'))
    all_partner_tickets = fields.Integer(string=_('Todos los tiquets'), compute='_compute_all_partner_tickets')

    @api.multi
    def all_customer_tickets(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Todos los tiquets'),
            'res_model': 'helpdesk.ticket',
            'view_mode': 'kanban,tree,form,pivot,graph',
            'context': {'search_default_partner_id': self.partner_id.id}
        }