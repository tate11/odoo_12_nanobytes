# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, api, _


class ResCompany(models.Model):
	_inherit = "res.company"

	def _get_default_documentation_folder(self):
		return self.env.ref('documents_nanobytes_folder', raise_if_not_found=False)

	dms_nanobytes_settings = fields.Boolean()
	documentation_folder = fields.Many2one('documents.folder', default=_get_default_documentation_folder)
	documentation_tags_documentation = fields.Many2many('documents.tag', 'documentation_tags_table')
	documentation_tags_app = fields.Many2many('documents.tag', 'documentation_tags_documentation_table')
	documentation_tags_script = fields.Many2many('documents.tag', 'documentation_tags_app_table')
	documentation_tags_manual = fields.Many2many('documents.tag', 'documentation_tags_manual_table')

	@api.multi
	def write(self, values):
		for company in self:
			if not company.dms_nanobytes_settings and values.get('dms_nanobytes_settings'):
				attachments = self.env['ir.attachment'].search([('folder_id', '=', False),
																('res_model', 'in', ['documentation.documentation'])])
				if attachments.exists():
					vals = {}
					if values.get('documentation_folder'):
						vals['folder_id'] = values['documentation_folder']
					elif company.documentation_folder:
						vals['folder_id'] = company.documentation_folder.id

					if values.get('documentation_tags_documentation'):
						vals['tag_ids'] = values['documentation_tags_documentation']
					elif company.documentation_tags_documentation:
						vals['tag_ids'] = [(6, 0, company.documentation_tags_documentation.ids)]
					if len(vals):
						attachments.write(vals)

				attachments = self.env['ir.attachment'].search([('folder_id', '=', False),
																('res_model', 'in', ['documentation.app'])])
				if attachments.exists():
					vals = {}
					if values.get('documentation_folder'):
						vals['folder_id'] = values['documentation_folder']
					elif company.documentation_folder:
						vals['folder_id'] = company.documentation_folder.id

					if values.get('documentation_tags_app'):
						vals['tag_ids'] = values['documentation_tags_app']
					elif company.documentation_tags_app:
						vals['tag_ids'] = [(6, 0, company.documentation_tags_app.ids)]
					if len(vals):
						attachments.write(vals)

				attachments = self.env['ir.attachment'].search([('folder_id', '=', False),
																('res_model', 'in', ['documentation.script'])])
				if attachments.exists():
					vals = {}
					if values.get('documentation_folder'):
						vals['folder_id'] = values['documentation_folder']
					elif company.documentation_folder:
						vals['folder_id'] = company.documentation_folder.id

					if values.get('documentation_tags_script'):
						vals['tag_ids'] = values['documentation_tags_script']
					elif company.documentation_tags_script:
						vals['tag_ids'] = [(6, 0, company.documentation_tags_script.ids)]
					if len(vals):
						attachments.write(vals)

				attachments = self.env['ir.attachment'].search([('folder_id', '=', False),
																('res_model', 'in', ['documentation.manual'])])
				if attachments.exists():
					vals = {}
					if values.get('documentation_folder'):
						vals['folder_id'] = values['documentation_folder']
					elif company.documentation_folder:
						vals['folder_id'] = company.documentation_folder.id

					if values.get('documentation_tags_manual'):
						vals['tag_ids'] = values['documentation_tags_manual']
					elif company.documentation_tags_manual:
						vals['tag_ids'] = [(6, 0, company.documentation_tags_manual.ids)]
					if len(vals):
						attachments.write(vals)

		return super(ResCompany, self).write(values)
