# -*- coding: utf-8 -*-

import time
import logging
from time import mktime
from datetime import timedelta, datetime
from odoo import models, fields, api, exceptions, tools, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    signature_pin = fields.Integer("Signature Pin")
    #allow_more_fields = fields.Boolean('Allow More Fields', related='team_id.active_more_fields')
    active_more_fields = fields.Boolean(_("Active More Fields"), related='team_id.active_more_fields')
    fiscal_name = fields.Char(_("Fiscal Name"))
    comercial_name = fields.Char(_("Comercial Name"))
    web_site = fields.Char(_("Website"), default="")
    email = fields.Char(_("Email"))
    phone = fields.Char(_("Phone"))
    fax = fields.Char(_("Fax"))
    frontis = fields.Char(_("Frontis"), default="")
    enterprise_name = fields.Char(_("Enterprise name"))
    adress = fields.Char(_("Adress"))
    apartado_correos = fields.Char(_("Apartado de correos"), default="")
    city = fields.Char(_("City"))
    postal_code = fields.Char(_("Postal code"))
    province = fields.Char(_("Province"))
    phone2 = fields.Char(_("Phone 2"), default="")
    mobile = fields.Char(_("Mobile phone"))
    activity = fields.Char(_("Activity"))
    responsable = fields.Char(_("Responsable"))
    productos_expone = fields.Char(_("Productos que expone"))