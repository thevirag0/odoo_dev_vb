from odoo import models, fields, api


class Plato(models.Model):
    _name = 'gestion_restaurante_valeria.plato'
    _description = 'Modelo para gestionar los platos del restaurante'

    name = fields.Char(string="Nombre del Plato", required=True)
    description = fields.Text(string="Ingredientes/Descripción")
