# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    passwords_count = fields.Integer(compute='_compute_passwords_count', string='# of Passwords')

    def _compute_passwords_count(self):
        for res_partner in self:
                res_partner.passwords_count = len(self.env['res.partner.passwords'].search([('partner_id', 'child_of', [res_partner.id])]))