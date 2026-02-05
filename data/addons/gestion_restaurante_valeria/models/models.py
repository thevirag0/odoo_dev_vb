from odoo import models, fields, api


class Plato(models.Model):
    _name = 'gestion_restaurante_valeria.plato'
    _description = 'Modelo para gestionar los platos del restaurante'

    name = fields.Char(string="Nombre del Plato", required=True)
    description = fields.Text(string="Ingredientes/Descripción")
    price = fields.Float(string="Precio", required=True)
    preparation_time = fields.Integer(string="Tiempo de Preparación (minutos)", required=False, help="Tiempo estimado de preparación del plato")
    available = fields.Boolean(string="Disponible", default="True", required=True, help="Indica si el plato puede ser preparado en este momento")
    category = fields.Selection(
        string="Categoría",
        selection=[
            ('entrante', 'Entrante'),
            ('plato_principal', 'Plato Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida')
        ],
        default='plato_principal'
    )
