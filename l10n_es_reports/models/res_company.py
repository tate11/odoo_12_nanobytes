# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def balance_sheet_menu_item_clicked(self):
        current_company = self.env['res.company']._company_default_get(
            'account.financial.html.report')

        spanish_coa_bs_map = {
            self.env.ref('l10n_es.account_chart_template_pymes'): self.env.ref("l10n_es_reports.financial_report_balance_sheet_pymes").id,
            self.env.ref('l10n_es.account_chart_template_full'): self.env.ref("l10n_es_reports.financial_report_balance_sheet_full").id,
            self.env.ref('l10n_es.account_chart_template_assoc'): self.env.ref("l10n_es_reports.financial_report_balance_sheet_assoc").id,
        }
        default_bs = self.env.ref(
            'account_reports.account_financial_report_balancesheet0').id

        return {
            'name': _('Balance de Situación'),
            'type': 'ir.actions.client',
            'tag': 'account_report',
            'context': {
                    'model': 'account.financial.html.report',
                    'id': spanish_coa_bs_map.get(current_company.chart_template_id, default_bs),
            }
        }

    @api.model
    def open_aeat_tax_report(self, modelo):
        report_wizard = self.env['l10n_es_reports.mod' + modelo + '.wizard'].create({})

        return {
            'name': _('AEAT Informe de Impuestos'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('l10n_es_reports.mod' + modelo + '_report_wizard_inherit').id,
            'res_model': 'l10n_es_reports.mod' + modelo + '.wizard',
            'type': 'ir.actions.act_window',
            'res_id': report_wizard.id,
            'target': 'new'
        }

    @api.model
    def open_model_200(self):

        report = self.env.ref('l10n_es_reports.mod_200')

        return {
            'type': 'ir.actions.client',
            'name': _('Modelo 200'),
            'tag': 'account_report',
            'context': {
                'model': 'account.financial.html.report',
                'id': report.id,
            }
        }

    @api.model
    def open_profit_and_loss_report(self):
        report = self.env.ref('l10n_es_reports.profit_and_loss_report')

        return {
            'type': 'ir.actions.client',
            'name': _('Perdidas y Ganancias'),
            'tag': 'account_report',
            'context': {
                'model': 'account.financial.html.report',
                'id': report.id,
            }
        }
