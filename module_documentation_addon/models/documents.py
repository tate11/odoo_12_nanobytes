# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class IrAttachment(models.Model):
	_name = 'ir.attachment'
	_inherit = 'ir.attachment'

	def _set_folder_settings(self, vals):
		vals = super(IrAttachment, self)._set_folder_settings(vals)
		if vals.get('res_model') in ('documentation.documentation', 'documentation.app', 'documentation.script', 'documentation.manual') \
				and self.env.user.company_id.dms_nanobytes_settings \
				and not vals.get('folder_id'):
			folder = self.env.user.company_id.documentation_folder
			if folder.exists():
				vals.setdefault('folder_id', folder.id)

				documentation_tags = []
				if vals.get('res_model') == 'documentation.documentation':
					documentation_tags = self.env.user.company_id.documentation_tags_documentation.ids
				if vals.get('res_model') == 'documentation.app':
					documentation_tags = self.env.user.company_id.documentation_tags_app.ids
				if vals.get('res_model') == 'documentation.script':
					documentation_tags = self.env.user.company_id.documentation_tags_script.ids
				if vals.get('res_model') == 'documentation.manual':
					documentation_tags = self.env.user.company_id.documentation_tags_manual.ids

				vals.setdefault('tag_ids', [(6, 0, documentation_tags)])
		return vals
