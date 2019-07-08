# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.http import request
#from odoo.addons.website_mail.controllers.main import _message_post_helper
from odoo.addons.portal.controllers.mail import _message_post_helper
import json
import time, random

from odoo.tools import pycompat, consteq

from odoo.exceptions import AccessError, MissingError
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)

class SignaturePin(CustomerPortal):


    @http.route(['/perso_signature_pin/generate_signature_pin'], type='json', auth="public", website=True)
    def generate_signature_pin(self, order_id, token=None, **post):
        _logger.info("<-- generate_signature_pin -->")
        _logger.info("order_id --> "+str(order_id))
        _logger.info("token --> "+str(token))
        Order = request.env['sale.order'].sudo().browse(order_id)
        _logger.info("Order.access_token --> "+str(Order.access_token))
        if token != Order.access_token: #or Order.require_payment:
            return request.render('website.404')

        signature_pin = int(str(''.join(random.choice('0123456789') for i in range(6))))
        Order.write({'signature_pin': signature_pin})

        if Order.partner_id.email:
            email = Order.partner_id.email
            mail = request.env['mail.mail']
            message = request.env['mail.message']          

            template_obj = request.env['mail.template']
            ir_model_data = request.env['ir.model.data']
            template_id = template_id = ir_model_data.get_object_reference('perso_signature_pin', 'email_template_pin_sale')[1]

            if template_id:
                template = template_obj.browse(template_id)
                values = template.sudo().generate_email(Order.id)
                values['email_to'] = email
                values['email_from'] = Order.company_id.email

                idMail = mail.sudo().create(values)

                mail.sudo().send([idMail.id])
                mail.sudo().process_email_queue()

        return True

    @http.route(['/perso_signature_pin/accept'], type='json', auth="public", website=True)
    def accept(self, order_id, token=None, signer=None, signer_pin=None, fiscal_name=None, comercial_name=None, frontis=None, enterprise_name=None,
        adress=None, apartado_correos=None, city=None, postal_code=None, province=None, web_site=None, email=None, phone=None, phone2=None, 
        fax=None, activity=None, responsable=None, productos_expone = None, **post):
        _logger.info("<-- accept -->")

        Order = request.env['sale.order'].sudo().browse(order_id)
        
        if token != Order.access_token: #or Order.require_payment:
            return request.render('website.404')
        if Order.state != 'sent':
            return -1
        if Order.signature_pin != signer_pin:
            return -2
        Order.action_confirm()
        message = _('Order signed by %s with the PIN: %s') % (signer,str(signer_pin),)
        _message_post_helper(message=message, res_id=order_id, res_model='sale.order', **({'token': token, 'token_field': 'access_token'} if token else {}))
        #Ticket #5730: Comrpobamos los campos opcionales y escribimos tanto los obligatorios como los opcionales que nos hayan pasado
        if web_site != None:
            Order.write({'web_site': web_site})
        if phone2 != None:
            Order.write({'phone2': phone2})
        if frontis != None:
            Order.write({'frontis': frontis})
        if apartado_correos != None:
            Order.write({'apartado_correos': apartado_correos})

        Order.write({
            'fiscal_name': fiscal_name,
            'comercial_name': comercial_name,
            'activity': activity,
            'enterprise_name': enterprise_name,
            'adress': adress,
            'productos_expone': productos_expone,
            'city': city,
            'postal_code': postal_code,
            'province': province,
            'email': email,
            'phone': phone,
            'fax': fax,
            'responsable': responsable
            })
        if Order.require_payment:
            return 2
        return 1

    def _document_check_access(self, model_name, document_id, access_token=None):
        document = request.env[model_name].browse([document_id])
        _logger.info("document: " + str(document))
        document_sudo = document.sudo().exists()
        if not document_sudo:
            raise MissingError("This document does not exist.")
        try:
            document.check_access_rights('read')
            document.check_access_rule('read')
        except AccessError:
            if not access_token or not consteq(document_sudo.access_token, access_token):
                raise
        return document_sudo
    
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        _logger.info("<-- my/orders -->")
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
            _logger.info("access_token: "+str(access_token))
            _logger.info("order_sudo: "+str(order_sudo))
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if order_sudo and request.session.get('view_quote_%s' % order_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % order_sudo.id] = now
            body = _('Quotation viewed by customer')
            _message_post_helper(res_model='sale.order', res_id=order_sudo.id, message=body, token=order_sudo.access_token, message_type='notification', subtype="mail.mt_note", partner_ids=order_sudo.user_id.sudo().partner_id.ids)

        values = {
            'sale_order': order_sudo,
            'message': message,
            'token': access_token,
            'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
            'report_type': 'html',
        }
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id

        if order_sudo.has_to_be_paid():
            domain = expression.AND([
                ['&', ('website_published', '=', True), ('company_id', '=', order_sudo.company_id.id)],
                ['|', ('specific_countries', '=', False), ('country_ids', 'in', [order_sudo.partner_id.country_id.id])]
            ])
            acquirers = request.env['payment.acquirer'].sudo().search(domain)

            values['acquirers'] = acquirers.filtered(lambda acq: (acq.payment_flow == 'form' and acq.view_template_id) or
                                                     (acq.payment_flow == 's2s' and acq.registration_view_template_id))
            values['pms'] = request.env['payment.token'].search(
                [('partner_id', '=', order_sudo.partner_id.id),
                ('acquirer_id', 'in', acquirers.filtered(lambda acq: acq.payment_flow == 's2s').ids)])

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_quotations_history', [])
        else:
            history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order_sudo))

        return request.render('sale.sale_order_portal_template', values)