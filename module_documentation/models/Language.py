# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationLanguage(models.Model):
	_name = 'documentation.language'
	_description = _('Programming language')

	def _get_app_counter(self):
		for r in self:
			r.app_counter = len(self.env['documentation.app'].search([('language_id', '=', r.id)]))

	def _get_script_counter(self):
		for r in self:
			r.script_counter = len(self.env['documentation.script'].search([('language_id', '=', r.id)]))

	name                  = fields.Char(string=_('Name'))
	app_counter           = fields.Integer(compute='_get_app_counter', string=_('App counter'))
	script_counter        = fields.Integer(compute='_get_script_counter', string=_('Script counter'))

	_sql_constraints = [
		('name_unique', 'unique(name)', _('Name must be unique!'))
	]