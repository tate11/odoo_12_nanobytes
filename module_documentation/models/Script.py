# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationScriptStep(models.Model):
	_name = 'documentation.script.step'
	_description = _('Step')

	name         = fields.Text(string=_('Description'), required=True)
	order        = fields.Integer(string=_('Order'))
	execute_type = fields.Selection([('app',_('App')), ('script',_('Script'))], string=_('Execute type'))
	app_id       = fields.Many2one('documentation.app', string=_('App'))
	another_id   = fields.Many2one('documentation.script', string=_('Script 2'))
	script_id    = fields.Many2one('documentation.script', ondelete='cascade', string=_('Script 1'))

class DocumentationScript(models.Model):
	_name = 'documentation.script'
	_description = _('Script')
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name               = fields.Char(string=_('Name'), required=True)
	image_thumbnail    = fields.Binary(string=_('Image'), attachment=True)
	category_id        = fields.Many2one('documentation.category', string=_('Category'))
	language_id        = fields.Many2one('documentation.language', string=_('Programming language'))
	have_documentation = fields.Selection([('no',_('No')), ('yes',_('Yes'))], string=_('Have documentation'), default='no')
	documentation_id   = fields.Many2one('documentation.documentation', string=_('Documentation'))
	tag_ids            = fields.Many2many('documentation.tag', 'script_tags_rel', 'script_id', 'tag_id', string=_('Tags'))
	owner_id           = fields.Many2one('res.users', default=lambda self: self.env.user, string=_('Owner'))
	description        = fields.Html(string=_('Description'))
	code               = fields.Text(string=_('Code'))
	step_ids           = fields.One2many('documentation.script.step', 'script_id', string=_('Steps'))