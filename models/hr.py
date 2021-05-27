# -*- coding: utf-8 -*-

from typing import DefaultDict
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class Employee(models.Model):
    _inherit = "hr.employee"

    is_driver = fields.Boolean(string='Es conductor')
    drivers_license = fields.Char(string='Licencia de conducir')
    driver_status = fields.Selection([
        ('libre','Libre'),
        ('asignado','Asignado'),
        ('no_disponible','No disponible')
        ], string='Estatus de conductor', index=True, default="libre",readonly=True)
    trips_count = fields.Integer(string='Conteo de viajes asignados', default=0, readonly=True)

    # Imagen de licencia del conductor
    imagen_licencia = fields.Binary("Licencia", index=True, attachment=True, help="Contiene foto de licencia del conductor, limited to 100x100px.")
    # licencia_image_url = fields.Char(string='URL de imagen de licencia', required=True)