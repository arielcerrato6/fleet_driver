# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError

class FleetAlphaProductTemplate(models.Model):
    _inherit = "product.template"

    product_km = fields.Float(string="Kilometros", digits=(12,2))

class FleetAlphaProductProduct(models.Model):
    _inherit = "product.product"

    product_km = fields.Float(string="Kilometros", digits=(12,2))