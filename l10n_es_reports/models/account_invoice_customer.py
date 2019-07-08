# Copyright 2018 Ionel Lazar <ilazar@nanobytes.es>

from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, pycompat
from odoo.tools.misc import format_date

from odoo.addons.web.controllers.main import clean_action


class ReportAccountInvoicesClients(models.AbstractModel):
    _name = "account.invoices.clients"
    _description = _("Invoices Clients")
    _inherit = "account.report"

    filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_month'}
    filter_cash_basis = False
    filter_all_entries = False
    filter_journals = False
    filter_analytic = True
    filter_unfold_all = False

    def get_templates(self):
        templates = super(ReportAccountInvoicesClients, self).get_templates()
        templates['main_template'] = 'account_reports.main_template'
        templates['line_template'] = 'account_reports.line_template'
        templates['search_template'] = 'account_reports.search_template'
        return templates

    def get_columns_name(self, options):
        return [{'name': _('Order')},
                {'name': _('Invoice Number')},
                {'name': _("Date invoice")},
                {'name': _("Date operation")},
                {'name': _("Concept")},
                {'name': _("Vat")},
                {'name': _("Partner")},
                {'name': _("Amount Untaxed"), 'class': 'number'},
                {'name': _("% Tax Rate"), 'class': 'number'},
                {'name': _("Amount Tax"), 'class': 'number'}, ]

    @api.model
    def get_lines(self, options, line_id=None):
        lines = []

        index = 1
        for invoice in self.env['account.invoice'].search([('type', 'in', ['out_invoice', 'out_refund']),
                                                           ('state', 'in', ['open', 'paid']), ('date_invoice', '>=', options.get(
                                                               'date').get('date_from')),
                                                           ('date_invoice', '<=', options.get('date').get('date_to'))], order='date_invoice, number'):
            for line in invoice.invoice_line_ids:
                tax_rate = 0
                amount_tax = 0
                price_unit = line.price_subtotal
                for tax_id in line.invoice_line_tax_ids:
                    if 'IVA' in tax_id.name:
                        if tax_id.amount_type == 'group':
                            tax_rate = 0
                        else:
                            tax_rate = tax_id.amount
                        amount_tax = line.price_subtotal * tax_rate / 100

                if invoice.type == 'out_refund':
                    price_unit = -price_unit
                    amount_tax = -amount_tax
                lines.append({
                    'id': 'invoice_' + str(invoice.id),
                    'name': str(index),
                    'level': 3,
                    'columns': [{'name': invoice.number}, {'name': invoice.date_invoice}, {'name': ''}, {'name': line.name},
                                {'name': invoice.partner_id.vat}, {'name': invoice.partner_id.name}, {'name': self.format_value(price_unit)}, {'name': tax_rate}, {'name': self.format_value(amount_tax)}, ],
                    'unfoldable': False,
                    'unfolded': False
                })
                index += 1

        return lines

    @api.model
    def get_report_name(self):
        return _("Invoices Clients")

    def format_date(self, dt_to, dt_from, options, dt_filter='date'):
        res = super(ReportAccountInvoicesClients, self).format_date(
            dt_to, dt_from, options, dt_filter)
        options_filter = options[dt_filter].get('filter', '')
        if isinstance(dt_to, pycompat.string_types):
            dt_to = datetime.strptime(dt_to, DEFAULT_SERVER_DATE_FORMAT)
        if 'month' in options_filter:
            return res
        if 'quarter' in options_filter:
            return res
        if 'year' in options_filter:
            return res
        if not dt_from:
            return _('Until %s') % (format_date(self.env, dt_to.strftime(DEFAULT_SERVER_DATE_FORMAT)),)
        else:
            return res
