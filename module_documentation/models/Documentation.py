# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationDocumentationIndex(models.Model):
	_name = 'documentation.documentation.index'
	_description = _('Index')

	name             = fields.Char(string=_('Name'), required=True)
	content          = fields.Text(string=_('Content'))
	order            = fields.Integer(string=_('Order'))
	execute_type     = fields.Selection([('app',_('App')), ('script',_('Script'))], string=_('Execute type'))
	app_id           = fields.Many2one('documentation.app', string=_('App'))
	script_id        = fields.Many2one('documentation.script', string=_('Script'))
	documentation_id = fields.Many2one('documentation.documentation', ondelete='cascade', string=_('Documentation'))

class DocumentationDocumentation(models.Model):
	_name = 'documentation.documentation'
	_description = _('Documentation')
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name               = fields.Char(string=_('Name'), required=True)
	image_thumbnail    = fields.Binary(string=_('Image'), attachment=True)
	category_id        = fields.Many2one('documentation.category', string=_('Category'))
	tag_ids            = fields.Many2many('documentation.tag', 'documentation_tags_rel', 'documentation_id', 'tag_id', string=_('Tags'))
	owner_id           = fields.Many2one('res.users', default=lambda self: self.env.user, string=_('Owner'))
	description        = fields.Html(string=_('Description'))
	index_ids          = fields.One2many('documentation.documentation.index', 'documentation_id', string=_('Indexes'))