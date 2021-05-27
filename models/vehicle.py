# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class vehicle(models.Model):
    _inherit = "fleet.vehicle"

    driver = fields.Many2one('hr.employee', index=True, string='Conductor', domain="[('is_driver','=',True)]")
    vehicle_type = fields.Selection([
        ('cabezal', 'Cabezal'),
        ('camion', 'Camión'),
    ], string="Tipo de vehiculo", index=True, track_visibility='onchange')
    vehicle_color = fields.Char(string="Color del vehiculo")
    motor_number = fields.Char(string="Numero de motor")
    cilindraje = fields.Char(string="Cilindraje")
    marc_vehculo = fields.Char(string="Marca del vechiculo")

    # imagenes vehiculo 
    imagen_revision = fields.Binary("Revisión", index=True, attachment=True, help="Contiene foto de revision del vehículo, limited to 100x100px.")
    imagen_placa = fields.Binary("Placa de Vehículo", index=True, attachment=True, help="Contiene foto de placa del vehículo, limited to 100x100px.")
    
    # Extendidos
    odometer_unit = fields.Selection(selection_add=[('hours','Horas')])
