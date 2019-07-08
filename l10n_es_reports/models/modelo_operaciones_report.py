

from odoo import models, fields, api, _


class ModeloOperacionesReport(models.Model):
    _name = 'modelo.operaciones.report'
    _auto = False

    tipo = fields.Char('Tipo')
    anio = fields.Integer('Año')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    name_partner = fields.Char('Nombre cliente')
    importe_t1 = fields.Float('Importe T1')
    importe_t2 = fields.Float('Importe T2')
    importe_t3 = fields.Float('Importe T3')
    importe_t4 = fields.Float('Importe T4')
    importe_total = fields.Float('Importe Total')

    def init(self):
        self.env.cr.execute("""
            create or replace view modelo_operaciones_report as (
                with consulta as(
                    with
                        posiciones_compra as (
                            select id, name from account_fiscal_position where name not like '%Intracom%' and name not like 'Retenci%'
                        ),

                        posiciones_venta as (
                            select id, name from account_fiscal_position where name not like '%Intracom%' and name not like 'Retenci%'
                        ),

                        com as (
                            select distinct
                            partner_id,
                            date_part('year', date_invoice) anio
                            from account_invoice where state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))
                            group by partner_id, anio
                            having sum(amount_total_signed) >= 3005.06
                        ),
                        ven as (
                            select distinct
                            partner_id,
                            date_part('year', date_invoice) anio
                            from account_invoice where state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))
                            group by partner_id, anio
                            having sum(amount_total_signed) >= 3005.06
                        )

                        (select
                        'Compras (Clave A)' as tipo,
                        com.anio,
                        com.partner_id,
                        (select name from res_partner where id = com.partner_id) as name_partner,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 1 and partner_id = com.partner_id and date_part('year', date_invoice) = com.anio and state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))) as importe_t1,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 2 and partner_id = com.partner_id and date_part('year', date_invoice) = com.anio and state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))) as importe_t2,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 3 and partner_id = com.partner_id and date_part('year', date_invoice) = com.anio and state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))) as importe_t3,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 4 and partner_id = com.partner_id and date_part('year', date_invoice) = com.anio and state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))) as importe_t4,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where partner_id = com.partner_id and date_part('year', date_invoice) = com.anio and state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_compra))) as importe_total
                        from com)

                        union

                        (select
                        'Ventas (Clave B)' as tipo,
                        t.anio,
                        t.partner_id,
                        (select name from res_partner where id = t.partner_id) as name_partner,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 1 and partner_id = t.partner_id and date_part('year', date_invoice) = t.anio and state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))) as importe_t1,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 2 and partner_id = t.partner_id and date_part('year', date_invoice) = t.anio and state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))) as importe_t2,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 3 and partner_id = t.partner_id and date_part('year', date_invoice) = t.anio and state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))) as importe_t3,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where date_part('quarter', date_invoice) = 4 and partner_id = t.partner_id and date_part('year', date_invoice) = t.anio and state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))) as importe_t4,
                        (select coalesce(sum(amount_total_signed),0.00) from account_invoice where partner_id = t.partner_id and date_part('year', date_invoice) = t.anio and state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id is null or fiscal_position_id in (select id from posiciones_venta))) as importe_total
                        from ven as t)
                        order by anio, tipo, partner_id
                )
            select  ROW_NUMBER() over (order by consulta.partner_id)as id, * from consulta

            )
            """)


class ModeloOperaciones349Report(models.Model):
    _name = 'modelo.operaciones349.report'
    _auto = False

    tipo = fields.Char('Tipo')
    anio = fields.Char('Anio')
    trimestre = fields.Char('Trimestre')
    mes = fields.Char('Mes')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    name_partner = fields.Char('Nombre cliente')
    importe_total = fields.Float('Importe Total')

    def init(self):
        self.env.cr.execute("""
            drop view if exists modelo_operaciones349_report;
            create view modelo_operaciones349_report as (
                with consulta as(
                    with
                        posiciones_compra as (
                            select id, name from account_fiscal_position where name like '%Intracom%'
                        ),

                        posiciones_venta as (
                            select id, name from account_fiscal_position where name like '%Intracom%'
                        ),

                        com as (
                            select distinct
                            partner_id,
                            date_part('year', date_invoice) anio,
                            date_part('quarter', date_invoice) trimestre,
                            date_part('month', date_invoice) mes
                            from account_invoice where state in ('open','paid') and type in ('in_invoice', 'in_refund') and (fiscal_position_id in (select id from posiciones_compra))
                            group by partner_id, anio, trimestre, mes
                        ),
                        ven as (
                            select distinct
                            partner_id,
                            date_part('year', date_invoice) anio,
                            date_part('quarter', date_invoice) trimestre,
                            date_part('month', date_invoice) mes
                            from account_invoice where state in ('open','paid') and type in ('out_invoice', 'out_refund') and (fiscal_position_id in (select id from posiciones_venta))
                            group by partner_id, anio, trimestre, mes
                        )

                        (select
                        'Compras Bienes (Clave A)' as tipo,
                        to_char(com.anio, '9999') as anio,
                        to_char(com.trimestre, '9') as trimestre,
                        to_char(com.mes, '99') as mes,
                        com.partner_id,
                        (select name from res_partner where id = com.partner_id) as name_partner,
                         (select sum(price_total) from account_invoice_line l
                          where (select tax_id from account_invoice_line_tax where invoice_line_id = l.id) in (11, 14, 29, 32, 35, 38)
                          and invoice_id in
                         (select id from account_invoice
                            where partner_id = com.partner_id
                            and date_part('year', date_invoice) = com.anio
                            and date_part('quarter', date_invoice) = com.trimestre
                            and date_part('month', date_invoice) = com.mes
                            and state in ('open','paid')
                            and type in ('in_invoice', 'in_refund')
                            and (fiscal_position_id in (select id from posiciones_compra)))) as importe_total
                        from com)

                        union

                        (select
                        'Compras Servicios (Clave I)' as tipo,
                        to_char(com.anio, '9999') as anio,
                        to_char(com.trimestre, '9') as trimestre,
                        to_char(com.mes, '99') as mes,
                        com.partner_id,
                        (select name from res_partner where id = com.partner_id) as name_partner,
                         (select sum(price_total) from account_invoice_line l
                          where (select tax_id from account_invoice_line_tax where invoice_line_id = l.id) in (8, 95, 98)
                          and invoice_id in
                         (select id from account_invoice
                            where partner_id = com.partner_id
                            and date_part('year', date_invoice) = com.anio
                            and date_part('quarter', date_invoice) = com.trimestre
                            and date_part('month', date_invoice) = com.mes
                            and state in ('open','paid')
                            and type in ('in_invoice', 'in_refund')
                            and (fiscal_position_id in (select id from posiciones_compra)))) as importe_total
                        from com)

                        union
                        (select
                        'Ventas Bienes (Clave E)' as tipo,
                        to_char(ven.anio, '9999') as anio,
                        to_char(ven.trimestre, '9') as trimestre,
                        to_char(ven.mes, '99') as mes,
                        ven.partner_id,
                        (select name from res_partner where id = ven.partner_id) as name_partner,
                         (select sum(price_total) from account_invoice_line l
                          where (select tax_id from account_invoice_line_tax where invoice_line_id = l.id) = 80
                          and invoice_id in
                         (select id from account_invoice
                            where partner_id = ven.partner_id
                            and date_part('year', date_invoice) = ven.anio
                            and date_part('quarter', date_invoice) = ven.trimestre
                            and date_part('month', date_invoice) = ven.mes
                            and state in ('open','paid')
                            and type in ('out_invoice', 'out_refund')
                            and (fiscal_position_id in (select id from posiciones_venta)))) as importe_total
                        from ven)

                        union

                        (select
                        'Venta Servicios (Clave S)' as tipo,
                        to_char(ven.anio, '9999') as anio,
                        to_char(ven.trimestre, '9') as trimestre,
                        to_char(ven.mes, '99') as mes,
                        ven.partner_id,
                        (select name from res_partner where id = ven.partner_id) as name_partner,
                         (select sum(price_total) from account_invoice_line l
                          where (select tax_id from account_invoice_line_tax where invoice_line_id = l.id) = 39
                          and invoice_id in
                            (select id from account_invoice
                                where partner_id = ven.partner_id
                                and date_part('year', date_invoice) = ven.anio
                                and date_part('quarter', date_invoice) = ven.trimestre
                                and date_part('month', date_invoice) = ven.mes
                                and state in ('open','paid')
                                and type in ('out_invoice', 'out_refund')
                                and (fiscal_position_id in (select id from posiciones_venta)))
                            ) as importe_total
                        from ven)
                )
            select  ROW_NUMBER() over (order by consulta.partner_id)as id, * from consulta where importe_total is not null
            )
            """)


class Modelo180Report(models.Model):
    _name = 'modelo.180.report'
    _auto = False

    clave = fields.Char('Clave')
    anio = fields.Char('Ejercicio')
    name_partner = fields.Char('Nombre')
    nif_partner = fields.Char('NIF')
    provincia = fields.Char('Provincia')
    rend_dinerario = fields.Float('Bases retenciones e ingresos a cuenta')
    cuota_dineraria = fields.Float('Retenciones e ingresos a cuenta')
    porcentaje = fields.Float('Porcentaje')

    def init(self):
        self.env.cr.execute("""
            drop view if exists modelo_180_report;
            create view modelo_180_report as (
                with consulta as(

                    with impuestos_irpf as(
                    select distinct(account_tax_id) from account_tax_account_tag where account_account_tag_id in (select id from account_account_tag where name ilike 'mod115%')
                    ),
                    datos_115 as
                    (
                    select extract(year from date) as anio, partner_id, 'base' as tipo, account_tax_id as tax_id, sum(balance) as balance from account_move_line aml inner join account_move_line_account_tax_rel amlatr on (aml.id = amlatr.account_move_line_id) where account_tax_id in (select account_tax_id from impuestos_irpf) group by account_tax_id, partner_id, anio
                    union
                    select extract(year from date) as anio, partner_id, 'cuota' as tipo, tax_line_id as tax_id, sum(balance) as balance from account_move_line aml where tax_line_id in (select account_tax_id from impuestos_irpf) group by tax_line_id, partner_id, anio
                    )

                    select
                    cast (anio as integer) as anio,
                    '1' as clave,
                    (select vat from res_partner where id = partner_id) as nif_partner,
                    (select name from res_partner where id = partner_id) as name_partner,
                    (select name from res_country_state where id = (select state_id from res_partner where id = partner_id)) as provincia,
                    sum((case when tipo = 'base' then balance
                    else 0
                    end)) as rend_dinerario,
                    (select -amount from account_tax where id = d.tax_id) as porcentaje,
                    sum((case when tipo = 'cuota' then -balance
                    else 0
                    end)) as cuota_dineraria
                    from datos_115 d group by anio, partner_id, clave, tax_id

                )
            select  ROW_NUMBER() over (order by consulta.anio, consulta.name_partner)as id, * from consulta
            )
            """)


class Modelo190Report(models.Model):
    _name = 'modelo.190.report'
    _auto = False

    clave = fields.Char('Clave')
    anio = fields.Char('Ejercicio')
    name_partner = fields.Char('Nombre')
    nif_partner = fields.Char('NIF')
    provincia = fields.Char('Provincia')
    rend_dinerario = fields.Float('Percepción dineraria íntegra')
    cuota_dineraria = fields.Float('Retenciones practicadas')
    porcentaje = fields.Float('Porcentaje')

    def init(self):
        self.env.cr.execute("""
            drop view if exists modelo_190_report;
            create view modelo_190_report as (
                with consulta as(

                    with impuestos_irpf as(
                    select distinct(account_tax_id) from account_tax_account_tag where account_account_tag_id in (select id from account_account_tag where name ilike 'mod111%')
                    ),
                    datos_111 as
                    (
                    select extract(year from date) as anio, partner_id, 'base' as tipo, account_tax_id as tax_id, sum(balance) as balance from account_move_line aml inner join account_move_line_account_tax_rel amlatr on (aml.id = amlatr.account_move_line_id) where account_tax_id in (select account_tax_id from impuestos_irpf) group by account_tax_id, partner_id, anio
                    union
                    select extract(year from date) as anio, partner_id, 'cuota' as tipo, tax_line_id as tax_id, sum(balance) as balance from account_move_line aml where tax_line_id in (select account_tax_id from impuestos_irpf) group by tax_line_id, partner_id, anio
                    )

                    select
                    cast (anio as integer) as anio,
                    (case when exists(select * from account_tax_account_tag where account_tax_id = d.tax_id and account_account_tag_id = 4) then 'A'
                    else 'G - 01'
                    end) as clave,
                    (select vat from res_partner where id = partner_id) as nif_partner,
                    (select name from res_partner where id = partner_id) as name_partner,
                    (select name from res_country_state where id = (select state_id from res_partner where id = partner_id)) as provincia,
                    sum((case when tipo = 'base' then balance
                    else 0
                    end)) as rend_dinerario,
                    (select -amount from account_tax where id = d.tax_id) as porcentaje,
                    sum((case when tipo = 'cuota' then -balance
                    else 0
                    end)) as cuota_dineraria
                    from datos_111 d group by anio, partner_id, clave, tax_id

                )
            select  ROW_NUMBER() over (order by consulta.anio, consulta.name_partner)as id, * from consulta
            )
            """)
