# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class PresentacionImpuestos(models.Model):
    _name = 'presentacion.impuestos'

    name = fields.Char('Nombre')
    date_from = fields.Date('Desde')
    date_to = fields.Date('Hasta')
    date_asiento = fields.Date('Fecha asiento')
    journal_id = fields.Many2one('account.journal', 'Diario de asiento')
    estado = fields.Selection(
        [('draft', 'Borrador'), ('done', 'Validada')], 'Estado', default='draft')

    cuenta_hacienda_acreedora_id = fields.Many2one(
        'account.account', 'Cuenta Hacienda Acreedora por IVA')
    cuenta_hacienda_deudora_id = fields.Many2one(
        'account.account', 'Cuenta Hacienda Deudora por IVA')

    move_id = fields.Many2one('account.move', 'Asiento')

    line_ids = fields.One2many('presentacion.impuestos.linea',
                               'presentacion_id', 'Lineas presentadas')

    selector_impuesto = fields.Selection([('iva', 'IVA'), ], default='iva')

    @api.multi
    def presentar(self):
        if self.line_ids:

            lineas_a_crear = []

            for linea in self.line_ids:
                linea_conta = {
                    'account_id': linea.account_id.id,
                    'tax_presentacion_id': linea.tax_id.id,
                    'tipo_factura_presentacion': linea.tipo_factura,
                    'credit': linea.balance < 0 and -linea.balance or 0.00,
                    'debit': linea.balance >= 0 and linea.balance or 0.00,
                }
                lineas_a_crear.append((0, 0, linea_conta))

            balance = sum([linea.balance for linea in self.line_ids])
            linea_hacienda = False
            if balance >= 0:
                linea_hacienda = (0, 0, {
                    'account_id': self.cuenta_hacienda_acreedora_id.id,
                    'credit': balance,
                    'debit': 0.00,
                })
            else:
                linea_hacienda = (0, 0, {
                    'account_id': self.cuenta_hacienda_deudora_id.id,
                    'credit': 0.00,
                    'debit': -balance,
                })
            lineas_a_crear.append(linea_hacienda)

            asiento = self.env['account.move']._sequence({
                'date': self.date_asiento,
                'journal_id': self.journal_id.id,
                'ref': self.name,
                'line_ids': lineas_a_crear,
            })

            asiento.post()

            self.move_id = asiento.id

            self.estado = 'done'
            return True
        return False

    @api.multi
    def cancelar(self):
        if self.move_id:
            self.move_id.button_cancel()
        self.estado = 'draft'
        return True

    @api.multi
    def rellenar(self):
        self.line_ids.unlink()

        if self.selector_impuesto == 'iva':
            consulta = """select account_id,
                tax_line_id,
                (select
                (case when type like '%%refund%%' then 'refunds'
                else 'invoices'
                end) as type
                from account_invoice where id = invoice_id) as invoice_type,
                round(sum(debit),2) as debe, round(sum(credit),2) as haber, round(sum(balance),2) as balance from account_move_line
                where
                move_id in (select id from account_move where state = 'posted')
                and tax_line_id in (select distinct(account_tax_id) from account_tax_account_tag where account_account_tag_id in (select id from account_account_tag where name ilike '%%mod303%%'))
                and date between %s and %s
                group by account_id, tax_line_id, invoice_type
                order by tax_line_id, account_id, invoice_type, round(sum(balance),2)"""
            self.env.cr.execute(consulta, (self.date_from, self.date_to))
            lineas_conta = self.env.cr.fetchall()

            lineas_a_crear = []

            for linea_conta in lineas_conta:
                linea_datos = (0, 0, {
                    'account_id': linea_conta[0],
                    'tax_id': linea_conta[1],
                    'tipo_factura': linea_conta[2],
                    'debe': linea_conta[3],
                    'haber': linea_conta[4],
                    'balance': -linea_conta[5],
                })
                lineas_a_crear.append(linea_datos)

            if lineas_a_crear:
                self.write({'line_ids': lineas_a_crear})


class PresentacionImpuestosLineas(models.Model):
    _name = 'presentacion.impuestos.linea'

    presentacion_id = fields.Many2one('presentacion.impuestos', 'Presentación')

    tax_id = fields.Many2one('account.tax', 'Impuesto')
    account_id = fields.Many2one('account.account', 'Cuenta contable')
    debe = fields.Monetary('Debe')
    haber = fields.Monetary('Haber')
    balance = fields.Monetary('Balance')
    tipo_factura = fields.Selection(
        [('invoices', 'Facturas'), ('refunds', 'Rectificativas')], 'Tipo Factura')
    currency_id = fields.Many2one('res.currency', _(
        'Currency'), default=lambda self: self.env['res.currency'].search([('name', '=', 'EUR')]))


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_presentacion_id = fields.Many2one(
        'account.tax', 'Impuesto presentacion')
    tipo_factura_presentacion = fields.Char('Tipo factura presentacion')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def sequence(self, vals):

        if vals['journal_id'] == 1:
            vals['sequence_number_next'] = 6

        elif vals['journal_id'] == 2:
            vals['sequence_number_next'] = 3

        record = super(AccountInvoice, self)._sequence(vals)

        return record
