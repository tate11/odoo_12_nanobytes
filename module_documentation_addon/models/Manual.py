# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationManual(models.Model):
	_inherit = 'documentation.manual'

	partner_ids = fields.Many2many('res.partner', 'manual_partner_rel', 'manual_id', 'partner_id', string=_('Partners'))