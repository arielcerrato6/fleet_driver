# -*- coding: utf-8 -*-

from typing import DefaultDict
from odoo import models, fields, api

status_motorista = [
    ('1', 'Movimiento'),
    ('2', 'Asiganado'),
    ('3', 'Libre'),
]

status_carretera = [
    ('1', 'Tomas en carretera'),
    ('2', 'Falla de equipo'),
    ('3', 'Accidente'),
]

AVAILABLE_PRIORITIES = [
    ('0', 'Bajo'),
    ('1', 'Medio'),
    ('2', 'Alto'),
    ('3', 'Muy alto'),
]

class fleet_driver(models.Model):
    _name = 'ficha_conductor'
    _rec_name = 'conductor'
    _order = "id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    conductor = fields.Many2one('hr.employee', index=True, string='Conductor')
    order_id = fields.Many2one('sale.order', index=True, string="No. de orden", readonly=True)
    # licencia = fields.Char(string="Licencia")
    estatus_motorista = fields.Selection(status_motorista, string='Estatus Motorista', index=True, default=status_motorista[0][0])
    estatus_carre = fields.Selection(status_carretera, string='Estatus Carretera', index=True, default="")
    # telefono = fields.Char('Telefono', track_visibility='onchange')
    description = fields.Text('Observaciones', track_visibility='onchange')
    vehicle = fields.Many2one('fleet.vehicle', string='Vehiculo')
    drivers_license = fields.Char(string="Licencia", readonly=True)

    # Etapas
    # def _get_default_etapa(self):
    #     return self.env['etapas_fleet_vehicle'].search([], limit=1).id

    # Estatus -----
    def _get_default_state(self):
        state = self.env.ref('fleet_driver.fleet_status_state_free', raise_if_not_found=False)
        return state if state and state.id else False

    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     return self.env['fleet.driver.state'].search([], order=order)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):      
        search_domain = [('id', 'in', stages.ids)]
        stage_ids = stages._search(search_domain, order=order)
        return stages.browse(stage_ids)

    state_id = fields.Many2one('fleet.driver.state', 'State',
        default=_get_default_state, group_expand='_read_group_stage_ids',
        track_visibility="onchange",
        help='Estado actual del Conductor', ondelete="set null")
    # Estatus cierre -----

    # @api.model
    # def _read_group_etapas(self, stages, domain, order):
    #     etapas = self.env['etapas_fleet_vehicle'].search([])
    #     return etapas

    # etapa = fields.Many2one('etapas_fleet_vehicle', string='Etapa', group_expand='_read_group_etapas', default=_get_default_etapa, track_visibility='onchange')
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Prioridad', index=True, default=AVAILABLE_PRIORITIES[0][0])
    probability = fields.Float('Probabilidad (%)', required=True, default=1, help="Probabilidad promedio.")

    @api.multi
    @api.onchange('conductor')
    def onchange_conductor(self):
        if not self.conductor:
            self.update({
                'drivers_license': "",
            })
            return
            
        else:
            self.drivers_license = self.conductor.drivers_license

    @api.multi
    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id.sequence == 3:
            self.conductor.trips_count -= 1          
        else:
            pass

class FleetDriverState(models.Model):
    _name = 'fleet.driver.state'
    _order = 'sequence asc'
    _description = 'Driver Status'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Orden de las etapas")

    _sql_constraints = [('fleet_state2_name_unique', 'unique(name)', 'Etapa ya existe')]   

