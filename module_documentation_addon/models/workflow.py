# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class WorkflowActionRuleDocumentation(models.Model):
	_inherit = ['documents.workflow.rule']

	has_business_option = fields.Boolean(default=True, compute='_get_business')
	create_model = fields.Selection(selection_add=[('documentation.app', _("App")),('documentation.script', _("Script")),('documentation.documentation', _("Documentation")),('documentation.manual', _("Manual"))])

	def create_record(self, attachments=None):
		rv = super(WorkflowActionRuleDocumentation, self).create_record(attachments=attachments)
		if self.create_model == 'documentation.app' or self.create_model == 'documentation.script' or self.create_model == 'documentation.documentation' or self.create_model == 'documentation.manual':

			model_name = ''
			if self.create_model == 'documentation.app':
				model_name = _('app')
			if self.create_model == 'documentation.script':
				model_name = _('script')
			if self.create_model == 'documentation.documentation':
				model_name = _('documentation')
			if self.create_model == 'documentation.manual':
				model_name = _('manual')

			new_obj = self.env[self.create_model].create({'name': _('%s created from DMS') % model_name})

			for attachment in attachments:
				this_attachment = attachment
				if attachment.res_model or attachment.res_id:
					this_attachment = attachment.copy()

				this_attachment.write({'res_model': self.create_model,
									   'res_id': new_obj.id,
									   'folder_id': this_attachment.folder_id.id})

			view_id = new_obj.get_formview_id()
			return {
				'type': 'ir.actions.act_window',
				'res_model': self.create_model,
				'name': _("New ") % model_name,
				'context': self._context,
				'view_type': 'form',
				'view_mode': 'form',
				'views': [(view_id, "form")],
				'res_id': new_obj.id if new_obj else False,
				'view_id': view_id,
			}
		return rv
