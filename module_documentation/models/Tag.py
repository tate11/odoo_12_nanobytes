# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationTag(models.Model):
	_name = 'documentation.tag'
	_description = _('Tag')

	name  = fields.Char(_('Name'))
	color = fields.Integer(_('Color'))

	_sql_constraints = [
		('name_uniq', 'unique (name)', _("Name must be unique!")),
	]