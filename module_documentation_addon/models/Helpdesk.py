# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class HelpdeskTicket(models.Model):
	_inherit = 'helpdesk.ticket'

	@api.multi
	def create_documentation(self):
		if self.stage_id.is_close:

			documentation_vals = {}
			index_ids = []

			max_message_process = int(self.env['ir.config_parameter'].sudo().get_param('module_documentation_addon.max_message_process'))

			if max_message_process < 1 or max_message_process == False:
				max_message_process = 5
			index = 0

			if self.message_ids:
				for message in self.message_ids:
					if message.body != '':
						if index < max_message_process or index == max_message_process:
							if message.body:
								index_ids.append((0,0,{'name': message.record_name,'content': message.body}))
					index = index + 1

			documentation_vals["name"] = self.name

			new_tags = []
			for tag in self.tag_ids:
				documentation_tag = self.env['documentation.tag'].search([('name', '=', tag.name)])
				if len(documentation_tag) > 0:
					new_tags.append(documentation_tag[0].id)
				else:
					documentation_tag = self.env['documentation.tag'].create({'name': tag.name})
					new_tags.append(documentation_tag.id)

			documentation_vals["tag_ids"] = [(6,0,new_tags)]

			category_id = False
			category = self.env['documentation.category'].search([('name','=','Helpdesk')])
			if len(category) > 0:
				category_id = category[0].id
			else:
				category = self.env['documentation.category'].create({'name': 'Helpdesk'})
				category_id = category.id
			documentation_vals["category_id"] = category_id
			if self.description:
				documentation_vals["description"] = self.description
			else:
				documentation_vals["description"] = " "
			if self.partner_id:
				documentation_vals["partner_ids"] = [(6,0,[self.partner_id.id])]
			documentation_vals["index_ids"] = index_ids


			documentation_id = self.env['documentation.documentation'].create(documentation_vals)

			view_ref = self.env['ir.model.data'].get_object_reference('module_documentation', 'view_documentation_documentation_form')
			view_id = view_ref and view_ref[1] or False

			return {
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'documentation.documentation',
				'views': [(view_id, 'form')],
				'view_id': view_id,
				'res_id': documentation_id.id,
				'target': 'new',
			}
		else:
			raise exceptions.ValidationError(_(u'The ticket must be closed to create documentation'))