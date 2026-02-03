from odoo import models, fields, api


class platos(models.Model):
    _name = 'gestion_restaurante_valeria.platos'
    _description = 'Modelo de Platos'

    name = fields.Char()
    value = fields.Char()

#    @api.depends('value')
#    def _value_pc(self):
#        for record in self:
#            record.value2 = float(record.value) / 100

