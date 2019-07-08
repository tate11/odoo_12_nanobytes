# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models, _

from odoo.exceptions import UserError, AccessError, ValidationError

import base64

import logging
_logger = logging.getLogger(__name__)


class SDDMandate(models.Model):
    _inherit = 'sdd.mandate'

    tipo_mandato = fields.Selection([('CORE','CORE'),('B2B','B2B')], string=u'Tipo de mandato', default='CORE')
        