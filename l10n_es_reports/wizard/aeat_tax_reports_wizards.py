# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class AEATTaxReportWizard(models.TransientModel):
    _name = 'l10n_es_reports.aeat.report.wizard'
    _modelo = None  # To be defined in subclasses as 'xxx', where xxx is the modelo number
    # of the implemented AEAT tax report

    def close_and_show_report(self):
        report = self.env.ref('l10n_es_reports.mod_' + self._modelo)
        return {
            'type': 'ir.actions.client',
            'name': _('Modelo %s') % self._modelo,
            'tag': 'account_report',
            'context': {
                'model': 'account.financial.html.report',
                'id': report.id,
                'aeat_wizard_id': self.id,
                'aeat_modelo': self._modelo,
            }
        }


class Mod111Wizard(models.TransientModel):

    _name = 'l10n_es_reports.mod111.wizard'
    _inherit = 'l10n_es_reports.aeat.report.wizard'
    _modelo = '111'

    casilla_10 = fields.Integer(string="[10] Nº de perceptores", default=0)
    casilla_11 = fields.Float(
        string="[11] Valor percepciones en especie", default=0)
    casilla_12 = fields.Float(
        string="[12] Importe de los ingresos a cuenta", default=0)
    casilla_13 = fields.Integer(string="[13] Nº de perceptores", default=0)
    casilla_14 = fields.Float(
        string="[14] Importe de las percepciones", default=0)
    casilla_15 = fields.Float(
        string="[15] Importe de las retenciones", default=0)
    casilla_16 = fields.Integer(string="[16] Nº de perceptores", default=0)
    casilla_17 = fields.Float(
        string="[17] Valor percepciones en especie", default=0)
    casilla_18 = fields.Float(
        string="[18] Importe de los ingresos a cuenta", default=0)
    casilla_19 = fields.Integer(string="[19] Nº de perceptores", default=0)
    casilla_20 = fields.Float(
        string="[20] Importe de las percepciones", default=0)
    casilla_21 = fields.Float(
        string="[21] Importe de las retenciones", default=0)
    casilla_22 = fields.Integer(string="[22] Nº de perceptores", default=0)
    casilla_23 = fields.Float(
        string="[23] Valor percepciones en especie", default=0)
    casilla_24 = fields.Float(
        string="[24] Importe de los ingresos a cuenta", default=0)
    casilla_25 = fields.Integer(string="[25] Nº de perceptores", default=0)
    casilla_26 = fields.Float(
        string="[26] Contraprestaciones satisfechas", default=0)
    casilla_27 = fields.Float(
        string="[27] Importe de los ingresos a cuenta", default=0)
    casilla_29 = fields.Float(
        string="[29] Resultados a ingresar anteriores", default=0)


class Mod115Wizard(models.TransientModel):
    _name = 'l10n_es_reports.mod115.wizard'
    _inherit = 'l10n_es_reports.aeat.report.wizard'
    _modelo = '115'

    casilla_04 = fields.Float(
        string="[04] Resultados a ingresar anteriores", default=0)


class Mod303Wizard(models.TransientModel):
    _name = 'l10n_es_reports.mod303.wizard'
    _inherit = 'l10n_es_reports.aeat.report.wizard'
    _modelo = '303'

    casilla_43 = fields.Float(
        string="[43] Regularización bienes de inversión", default=0)
    casilla_44 = fields.Float(string="[44] Regularización por aplicación del porcentaje definitivo de prorrata",
                              default=0)
    casilla_62 = fields.Float(string="[62] Base imponible", default=0)
    casilla_63 = fields.Float(string="[63] Cuota", default=0)
    casilla_65 = fields.Float(
        string="[65] % Atribuible a la Administración", default=0)
    casilla_67 = fields.Float(
        string="[67] Cuotas a compensar de periodos anteriores", default=0)
    casilla_68 = fields.Float(
        string="[68] Resultado de la regularización anual", default=0)
    casilla_69 = fields.Float(string="[69] Resultado", default=0)


class Mod390Wizard(models.TransientModel):
    _name = 'l10n_es_reports.mod390.wizard'
    _inherit = 'l10n_es_reports.aeat.report.wizard'
    _modelo = '390'

    casilla_63 = fields.Float(
        string="[63] Regularización bienes de inversión", default=0)
    casilla_522 = fields.Float(string="[522] Regularización por aplicación del porcentaje definitivo de prorrata",
                               default=0)


class Mod200Wizard(models.TransientModel):
    _name = 'l10n_es_reports.mod200.wizard'
    _inherit = 'l10n_es_reports.aeat.report.wizard'
    _modelo = '200'

    casilla_63 = fields.Float(
        string="[63] Regularización bienes de inversión", default=0)
    casilla_522 = fields.Float(string="[522] Regularización por aplicación del porcentaje definitivo de prorrata",
                               default=0)
