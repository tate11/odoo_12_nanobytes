# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, registry
import logging
_logger = logging.getLogger(__name__)

class Partner(models.Model):
	_inherit = "res.partner"
	
#	acreedor = fields.Boolean('Acreedor')

	@api.model
	def create(self, vals):
		res = super(Partner, self).create(vals)
		
		if 'acreedor' in self.env['res.partner']._fields and res.acreedor:
			res.property_account_payable_id = self._new_account_number(res.name, res.parent_id, '4100')

		elif res.supplier:              
			res.property_account_payable_id = self._new_account_number(res.name, res.parent_id, '4000')

		if res.customer:            
			res.property_account_receivable_id = self._new_account_number(res.name, res.parent_id, '4300', 'receivable')
		

		return res

	@api.multi
	def write(self, vals):

		# Comprobar si la actualización es de acreedor, supplier, customer.
		acreedor = vals.get('acreedor')
		supplier = vals.get('supplier')
		customer = vals.get('customer')

		if(acreedor or supplier or customer):
			for elem in self:
				# Tenemos que apuntar a la cuenta contable por defecto.
				if ('acreedor' in self.env['res.partner']._fields and elem.acreedor and acreedor == False) or (elem.supplier and supplier == False):
					r = self.env['ir.property'].sudo().get('property_account_payable_id', 'res.partner')
					if (r):
						elem.property_account_payable_id = r

				if elem.customer and customer == False:
					r = self.env['ir.property'].sudo().get('property_account_receivable_id', 'res.partner')
					if (r):
						elem.property_account_receivable_id = r			

				# Apuntar la cuenta contable que debería.
				if 'acreedor' in self.env['res.partner']._fields and not elem.acreedor and acreedor:
					elem.property_account_payable_id = self._new_account_number(elem.name, elem.parent_id, '4100')

				elif not elem.supplier and supplier:
					elem.property_account_payable_id = self._new_account_number(elem.name, elem.parent_id, '4000')

				if not elem.customer and customer:            
					elem.property_account_receivable_id = self._new_account_number(elem.name, elem.parent_id, '4300', 'receivable')

		return super(Partner, self).write(vals)


	def _new_account_number(self, name, parent_id, number, t='payable'):
		accounts_id = self.env['account.account'].sudo().search([('code', '=like', '{0}%'.format(number))], limit=1, order='code desc').code
		accounts_id = int(accounts_id) + 1
		account = None

		if not parent_id:
			new_name = name
			type = self.env['account.account.type'].sudo().search([('type', '=', t)])

			values = {
				'code': accounts_id,
				'name': new_name,
				'user_type_id': type.id,
				'reconcile': True,
			}

			ok = 100
			account = None

			while (ok):
				with api.Environment.manage():
					with registry(self.env.cr.dbname).cursor() as new_cr:
						new_env = api.Environment(new_cr, self.env.uid, self.env.context)
						try:
							account = self.with_env(new_env).env['account.account'].sudo().create(values)
							ok = 0
							
						except:
							values['code'] += 1
							ok-=1
							pass
						new_env.cr.commit()
		return account
