# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationAppVersion(models.Model):
	_name = 'documentation.app.version'
	_description = _('Version')

	name         = fields.Char(string=_('Name version'))
	name_file    = fields.Char(string=_('Filename'))
	file         = fields.Binary(string=_('File'), filters='*.tar.gz, *.zip, *.rar, *.apk, *.jar, *.app', attachment=True)
	date_version = fields.Datetime(string=_('Date version'))
	app_id       = fields.Many2one('documentation.app', ondelete='cascade', string=_('App'))


class DocumentationAppClass(models.Model):
	_name = 'documentation.app.class'
	_description = _('Class')

	line_type = fields.Selection([('file', _('File')),('folder', _('Folder'))], required=True, string=_('Type'), default='file')
	name      = fields.Char(string=_('Name'), required=True)
	code      = fields.Text(string=_('Class'))
	app_id    = fields.Many2one('documentation.app', ondelete='cascade', string=_('App'))

class DocumentationApp(models.Model):
	_name = 'documentation.app'
	_description = _('App')
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name               = fields.Char(string=_('Name'), required=True)
	image_thumbnail    = fields.Binary(string=_('Image'), attachment=True)
	category_id        = fields.Many2one('documentation.category', string=_('Category'))
	language_id        = fields.Many2one('documentation.language', string=_('Programming language'))
	have_documentation = fields.Selection([('no',_('No')), ('yes',_('Yes'))], string=_('Have documentation'), default='no')
	documentation_id   = fields.Many2one('documentation.documentation', string=_('Documentation'))
	tag_ids            = fields.Many2many('documentation.tag', 'app_tags_rel', 'app_id', 'tag_id', string=_('Tags'))
	owner_id           = fields.Many2one('res.users', default=lambda self: self.env.user, string=_('Owner'))
	description        = fields.Html(string=_('Description'))
	storage_type       = fields.Selection([('binary', _('Binary')),('class', _('Class'))], string=_('Storage type'), default='binary')
	name_file          = fields.Char(string=_('Filename'))
	file               = fields.Binary(string=_('File'), filters='*.tar.gz, *.zip, *.rar, *.apk, *.jar, *.app', attachment=True)
	version_ids        = fields.One2many('documentation.app.version', 'app_id', string=_('Versions'))
	class_ids          = fields.One2many('documentation.app.class', 'app_id', string=_('Classes'))