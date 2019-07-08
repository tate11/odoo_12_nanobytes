# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, exceptions, tools, _

_logger = logging.getLogger(__name__)


class CrmTeam(models.Model):
	_inherit = 'crm.team'

	active_more_fields = fields.Boolean(_("Active More Fields"))

	@api.onchange('active_more_fields')
	def on_change_active_more_fields(self):
		sale_orders = self.env['sale.order'].search([('team_id','=',self.id)])
		for s in sale_orders:
			s.write({'allow_more_fields': self.active_more_fields})
			if not self.active_more_fields:
				s.write({'active_more_fields': self.active_more_fields})