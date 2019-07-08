# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class ResUsers(models.Model):
	_inherit = 'res.users'

	def _get_app_counter(self):
		for r in self:
			r.app_counter = len(self.env['documentation.app'].search([('owner_id', '=', r.id)]))

	def _get_script_counter(self):
		for r in self:
			r.script_counter = len(self.env['documentation.script'].search([('owner_id', '=', r.id)]))

	def _get_documentation_counter(self):
		for r in self:
			r.documentation_counter = len(self.env['documentation.documentation'].search([('owner_id', '=', r.id)]))

	def _get_manual_counter(self):
		for r in self:
			r.manual_counter = len(self.env['documentation.manual'].search([('owner_id', '=', r.id)]))

	app_counter           = fields.Integer(compute='_get_app_counter', string=_('App counter'))
	script_counter        = fields.Integer(compute='_get_script_counter', string=_('Script counter'))
	documentation_counter = fields.Integer(compute='_get_documentation_counter', string=_('Documentation counter'))
	manual_counter        = fields.Integer(compute='_get_manual_counter', string=_('Manual counter'))
