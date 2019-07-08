# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class AccountBatchPayment(models.Model):
    _inherit = "account.batch.payment"

    def validate_batch(self):
        _logger.info("<-- validate_batch -->")
        records = self.filtered(lambda x: x.state == 'draft')

        #Comprobamos si todos los mandatos son del mismo tipo
        set_mandatos = set()
        for record in records:
            for payment in record.payment_ids:
                set_mandatos.add(payment.tipo_mandato)

        if len(set_mandatos) > 1:
            raise ValidationError(_("Los adeudos directos tienen que ser del mismo tipo de mandato."))
        else:
            for record in records:
                record.payment_ids.write({'state':'sent', 'payment_reference': record.name})
            records.write({'state': 'sent'})

            records = self.filtered(lambda x: x.file_generation_enabled)
            if records:
                return self.export_batch_payment()
    '''
    def export_batch_payment(self):
        export_file_data = {}
        #export and save the file for each batch payment
        for record in self:
            export_file_data = record._generate_export_file()
            if record.export_file:
                record.export_file = export_file_data['file']
            if record.export_file:
                record.export_filename = export_file_data['filename']
            if record.export_file_create_date:
                record.export_file_create_date = fields.Date.today()

        #if the validation was asked for a single batch payment, open the wizard to download the newly generated file
        if len(self) == 1:
            download_wizard = self.env['account.batch.download.wizard'].create({
                    'batch_payment_id': self.id,
                    'warning_message': export_file_data.get('warning'),
            })
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.batch.download.wizard',
                'target': 'new',
                'res_id': download_wizard.id,
            }

    def print_batch_payment(self):
        return self.env.ref('account_batch_payment.action_print_batch_payment').report_action(self, config=False)

    def _generate_export_file(self):
        """ To be overridden by modules adding support for different export format.
            This function returns False if no export file could be generated
            for this batch. Otherwise, it returns a dictionary containing the following keys:
            - file: the content of the generated export file, in base 64.
            - filename: the name of the generated file
            - warning: (optional) the warning message to display

        """
        self.ensure_one()
        return False
    '''