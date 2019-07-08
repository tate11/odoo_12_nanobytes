# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _


class DocumentationBoard(models.Model):
	_name = 'documentation.board'
	_description = _('Dashboard')

	@api.depends('used_model')
	def _get_count_item(self):
		for r in self:
			res = 0
			if r.used_model:
				res = len(self.env[r.used_model].search([]))
			r.item_count = res

	name       = fields.Char(string=_('Name'), required=True, translate=True)
	used_model = fields.Char(string=_('Model'), required=True)
	used_view  = fields.Char(string=_('View'), required=True)
	item_count = fields.Integer(compute='_get_count_item', string=_('Item count'))
	item_name  = fields.Char(string=_('Items name'), translate=True)

	@api.multi
	def action_open_view(self):
		if self.used_view:
			return self.env['ir.actions.act_window'].for_xml_id('module_documentation', self.used_view)