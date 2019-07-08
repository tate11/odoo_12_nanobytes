# Copyright 2018 Ionel Lazar <ilazar@nanobytes.es>

from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, pycompat
from odoo.tools.misc import format_date

from odoo.addons.web.controllers.main import clean_action


class ReportAccountInvestmentGoodsIrpf(models.AbstractModel):
    _name = "account.investment.goods.irpf"
    _description = _("Investment Goods")
    _inherit = "account.report"

    filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_month'}
    filter_cash_basis = False
    filter_all_entries = False
    filter_journals = False
    filter_analytic = True
    filter_unfold_all = False

    def get_templates(self):
        templates = super(ReportAccountInvestmentGoodsIrpf, self).get_templates()
        templates['main_template'] = 'account_reports.main_template'
        templates['line_template'] = 'account_reports.line_template'
        templates['search_template'] = 'account_reports.search_template'
        return templates

    def get_columns_name(self, options):
        return [{'name': _('Order')},
                {'name': _('Description')},
                {'name': _("Invoice Number")},
                {'name': _("Adquistion Date")},
                {'name': _("Adquisition Amount Untaxed")},
                {'name': _("Adquisition Amount Tax")},
                {'name': _("Amortization Start")},
                {'name': _("Amortization Period Amount"), 'class': 'number'},
                {'name': _("Amortization Cumulative Amount"), 'class': 'number'}, ]

    @api.model
    def get_lines(self, options, line_id=None):
        lines = []

        index = 1
        for asset in self.env['account.asset.asset'].search([], order='date'):

            invoice_number = ''
            amount_tax = 0
            start_date = ''
            period_amount = 0
            cumulative_amount = 0
            if asset.invoice_id:
                invoice_number = asset.invoice_id.number

                impuestos = []

                for line in asset.invoice_id.invoice_line_ids:
                    if line.product_id and line.product_id.asset_category_id == asset.category_id:
                        for impuesto in line.invoice_line_tax_ids:
                            impuestos.append(impuesto)
                        break

                amount_tax = 0

                for impuesto in impuestos:
                    if 'IVA' in impuesto.name:
                        if impuesto.amount_type == 'group':
                            tax_rate = 0
                        else:
                            tax_rate = impuesto.amount
                        amount_tax += asset.value * tax_rate / 100
                        _logger.warning(amount_tax)

            if asset.depreciation_line_ids:
                depreciation_lines = self.env['account.asset.depreciation.line'].search(
                    [('asset_id', '=', asset.id)], order='depreciation_date')
                if depreciation_lines:
                    start_date = depreciation_lines[0].depreciation_date

                date_to = datetime.strptime(options.get('date').get('date_to'), '%Y-%m-%d')
                date_from = datetime.strptime(options.get('date').get('date_from'), '%Y-%m-%d')

                period_lines = asset.depreciation_line_ids.filtered(lambda r: datetime.strptime(
                    r.depreciation_date, '%Y-%m-%d') <= date_to and datetime.strptime(r.depreciation_date, '%Y-%m-%d') >= date_from and r.move_check)
                period_amount = sum([period.amount for period in period_lines])

                cumulative_lines = asset.depreciation_line_ids.filtered(
                    lambda r: datetime.strptime(r.depreciation_date, '%Y-%m-%d') < date_from and r.move_check)
                cumulative_amount = sum([cumulative.amount for cumulative in cumulative_lines])

            lines.append({
                'id': 'asset_' + str(asset.id),
                'name': str(index),
                'level': 3,
                'columns': [{'name': asset.name}, {'name': invoice_number}, {'name': asset.date}, {'name': self.format_value(asset.value)},
                            {'name': self.format_value(amount_tax)}, {'name': start_date}, {'name': self.format_value(period_amount)}, {'name': self.format_value(cumulative_amount)}, ],
                'unfoldable': False,
                'unfolded': False
            })
            index += 1

        return lines

    @api.model
    def get_report_name(self):
        return _("Investment Goods")

    def format_date(self, dt_to, dt_from, options, dt_filter='date'):
        res = super(ReportAccountInvestmentGoodsIrpf, self).format_date(
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
