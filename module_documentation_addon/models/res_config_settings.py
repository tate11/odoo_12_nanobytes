# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
		_inherit = 'res.config.settings'

		def _get_default_documentation_folder(self):
				folder_id = self.env.user.company_id.documentation_folder
				if folder_id.exists():
						return folder_id
				return False

		dms_nanobytes_settings = fields.Boolean(related='company_id.dms_nanobytes_settings', readonly=False,
																					default=lambda self: self.env.user.company_id.dms_nanobytes_settings,
																					string=_("Documentation Folder"))
		documentation_folder = fields.Many2one('documents.folder', related='company_id.documentation_folder', readonly=False,
																		 default=_get_default_documentation_folder,
																		 string=_("documentation default folder"))
		documentation_tags_documentation = fields.Many2many('documents.tag', 'documentation_tags_documentation_table',
																		related='company_id.documentation_tags_documentation', readonly=False,
																		default=lambda self: self.env.user.company_id.documentation_tags_documentation.ids,
																		string=_("Documentation Tags"))
		documentation_tags_app = fields.Many2many('documents.tag', 'documentation_tags_app_table',
																		related='company_id.documentation_tags_app', readonly=False,
																		default=lambda self: self.env.user.company_id.documentation_tags_app.ids,
																		string=_("App Tags"))
		documentation_tags_script = fields.Many2many('documents.tag', 'documentation_tags_script_table',
																		related='company_id.documentation_tags_script', readonly=False,
																		default=lambda self: self.env.user.company_id.documentation_tags_script.ids,
																		string=_("Script Tags"))
		documentation_tags_manual = fields.Many2many('documents.tag', 'documentation_tags_manual_table',
																		related='company_id.documentation_tags_manual', readonly=False,
																		default=lambda self: self.env.user.company_id.documentation_tags_manual.ids,
																		string=_("Manual Tags"))
