# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, exceptions, _

class DocumentationDocumentation(models.Model):
	_inherit = 'documentation.documentation'

	partner_ids = fields.Many2many('res.partner', 'documentation_partner_rel', 'documentation_id', 'partner_id', string=_('Partners'))