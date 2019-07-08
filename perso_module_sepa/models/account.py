# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models, _
from datetime import datetime, date
import calendar
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.exceptions import UserError

from odoo.tools.float_utils import float_repr
from odoo.tools.xml_utils import create_xml_node, create_xml_node_chain

from lxml import etree

import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    tipo_mandato = fields.Selection(string=u'Tipo de Mandato', related='sdd_mandate_id.tipo_mandato')


    def get_mandato(self):
        for r in self:
            if r.sdd_mandate_id and r.sdd_mandate_id.tipo_mandato:
                r.tipo_mandato = r.sdd_mandate_id.tipo_mandato

    def _sdd_xml_gen_partner(self, company_id, required_collection_date, payment_info_counter, mandate, CstmrDrctDbtInitn):
        _logger.info("<-- _sdd_xml_gen_partner -->")
        """ Appends to a SDD XML file being generated all the data related to a partner
        and his payments. self must be a recordset whose payments share the same partner.

        /! => Grouping the payments by mandate caused problems with Dutch banks, because
        of the too large number of distinct transactions in the file. We fixed that so that we now
        group on payment journal. This function is not used anymore
        and will be removed. It has been replaced by _sdd_xml_gen_payment_group.
        """
        PmtInf = create_xml_node(CstmrDrctDbtInitn, 'PmtInf')
        create_xml_node(PmtInf, 'PmtInfId', str(payment_info_counter))
        create_xml_node(PmtInf, 'PmtMtd', 'DD')
        create_xml_node(PmtInf, 'NbOfTxs', str(len(self)))
        create_xml_node(PmtInf, 'CtrlSum', float_repr(sum(x.amount for x in self), precision_digits=2))  # This sum ignores thecurrency, it is used as a checksum (see SEPA rulebook)

        PmtTpInf = create_xml_node_chain(PmtInf, ['PmtTpInf','SvcLvl','Cd'], 'SEPA')[0]
        tipo_mandato = ''
        for r in self:
            if r.tipo_mandato:
                tipo_mandato = r.tipo_mandato
                break
        create_xml_node_chain(PmtTpInf, ['LclInstrm','Cd'], tipo_mandato)
        create_xml_node(PmtTpInf, 'SeqTp', 'FRST')
        #Note: FRST refers to the COLLECTION of payments, not the type of mandate used
        #This value is only used for informatory purpose.

        create_xml_node(PmtInf, 'ReqdColltnDt', fields.Date.from_string(required_collection_date).strftime("%Y-%m-%d"))
        create_xml_node_chain(PmtInf, ['Cdtr','Nm'], company_id.name[:70])  # SEPA regulation gives a maximum size of 70 characters for this field
        create_xml_node_chain(PmtInf, ['CdtrAcct','Id','IBAN'], mandate.payment_journal_id.bank_account_id.sanitized_acc_number)
        create_xml_node_chain(PmtInf, ['CdtrAgt','FinInstnId','BIC'], mandate.payment_journal_id.bank_id.bic)

        CdtrSchmeId_Othr = create_xml_node_chain(PmtInf, ['CdtrSchmeId','Id','PrvtId','Othr','Id'], company_id.sdd_creditor_identifier)[-2]
        create_xml_node_chain(CdtrSchmeId_Othr, ['SchmeNm','Prtry'], 'SEPA')

        partner = None
        for partner_payment in self:
            if not partner:
                partner = partner_payment.partner_id
            elif partner != partner_payment.partner_id:
                raise UserError("Trying to generate a single XML payment group for payments with different partners.")

            partner_payment.sdd_xml_gen_payment(company_id, mandate.partner_id, partner_payment.name[:35], PmtInf)

    def _sdd_xml_gen_payment_group(self, company_id, required_collection_date, payment_info_counter, journal, CstmrDrctDbtInitn):
        _logger.info("<-- _sdd_xml_gen_payment_group -->")
        """ Generates a group of payments in the same PmtInfo node, provided
        that they share the same journal."""
        PmtInf = create_xml_node(CstmrDrctDbtInitn, 'PmtInf')
        create_xml_node(PmtInf, 'PmtInfId', str(payment_info_counter))
        create_xml_node(PmtInf, 'PmtMtd', 'DD')
        create_xml_node(PmtInf, 'NbOfTxs', str(len(self)))
        create_xml_node(PmtInf, 'CtrlSum', float_repr(sum(x.amount for x in self), precision_digits=2))  # This sum ignores thecurrency, it is used as a checksum (see SEPA rulebook)

        PmtTpInf = create_xml_node_chain(PmtInf, ['PmtTpInf','SvcLvl','Cd'], 'SEPA')[0]
        tipo_mandato = ''
        for r in self:
            if r.tipo_mandato:
                tipo_mandato = r.tipo_mandato
                break
        create_xml_node_chain(PmtTpInf, ['LclInstrm','Cd'], tipo_mandato)
        create_xml_node(PmtTpInf, 'SeqTp', 'FRST')
        #Note: FRST refers to the COLLECTION of payments, not the type of mandate used
        #This value is only used for informatory purpose.

        create_xml_node(PmtInf, 'ReqdColltnDt', fields.Date.from_string(required_collection_date).strftime("%Y-%m-%d"))
        create_xml_node_chain(PmtInf, ['Cdtr','Nm'], company_id.name[:70])  # SEPA regulation gives a maximum size of 70 characters for this field
        create_xml_node_chain(PmtInf, ['CdtrAcct','Id','IBAN'], journal.bank_account_id.sanitized_acc_number)
        create_xml_node_chain(PmtInf, ['CdtrAgt','FinInstnId','BIC'], journal.bank_id.bic)

        CdtrSchmeId_Othr = create_xml_node_chain(PmtInf, ['CdtrSchmeId','Id','PrvtId','Othr','Id'], company_id.sdd_creditor_identifier)[-2]
        create_xml_node_chain(CdtrSchmeId_Othr, ['SchmeNm','Prtry'], 'SEPA')

        for payment in self:
            payment.sdd_xml_gen_payment(company_id, payment.partner_id, payment.name[:35], PmtInf)