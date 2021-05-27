# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError

class Sale_orders(models.Model):
    _inherit = "sale.order"

    # driver = fields.Many2one('hr.employee', index=True, string='Conductor', required=True)
    fichas_count = fields.Integer(string='Viaje')
    rel_ficha_viaje = fields.Many2one('ficha_conductor', index=True, string='Ficha de viaje', readonly=True)

    #Función crear ficha de viaje.
    @api.multi
    def crear_nueva_ficha_viaje(self):
        stage = self.env['sale.order'].search([('id', '=', self.id)], limit=1)
        create_trip = self.env['ficha_conductor']

        order_line_list =[]
        for orders in self.order_line:
            nueva_ficha_viaje = {
                'order_id':orders.order_id.id,
                'conductor': orders.driver_line.id,
                'etapa': '1',
                'vehicle': orders.vehicle_id.id,
                'estatus_carre': '1',
                # 'description': format(order_line_list,sep = "\n")
                'description': orders.name
            }
            create_trip.create(nueva_ficha_viaje)
            orders.driver_line.trips_count += 1

    #Modifico el boton de confirmar el pedido en el modulo de ventas sale_order.
    @api.multi
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now()
        })

        #Crear nueva ficha de viaje
        self.crear_nueva_ficha_viaje()

        self._action_confirm()
        
        #Conteo de fichas de viaje
        self.fichas_count = len(self.env['ficha_conductor'].search([('order_id', '=', self.id)]))

        # Link al ficha del viaje
        # self.rel_ficha_viaje = self.env['ficha_conductor'].search([('order_id', '=', self.id)])

        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()

        return True

    #Boton de seguimiento viajes/ficha
    @api.multi
    def document_view_ficha_viaje(self):
        self.ensure_one()
        domain = [('order_id', '=', self.id)]
        return {
            'name': _('Ficha Viaje'),
            'domain': domain,
            'res_model': 'ficha_conductor',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'kanban',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click para crear un nuevo 
                        </p>'''),
            'limit': 80,
            'context': "{'default_order_id': '%s'}" % self.id
        }
    
    document_count_ficha_viaje = fields.Char(string='Viajes')


class FleetAlphaSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sales Order Line'

    driver_line = fields.Many2one('hr.employee', index=True, string='Conductor',  domain="[('is_driver','=',True)]", required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', index=True, string='Vehículo',  domain="[('driver','=', driver_line)]", required=True)
    date_start = fields.Date(string="Fecha inicio")
    date_end = fields.Date(string="Fecha fin")
    days = fields.Integer(string="Dias")
    product_km = fields.Char(string="Km")

    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            self.update({
                'product_km': False,
            })
            return
            
        else:
            self.product_km = self.product_id.product_km

"&", ["purchase_ok","=",True], ["sale_ok","=",True],