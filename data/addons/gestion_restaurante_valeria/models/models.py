# from odoo import models, fields, api


# class gestion_restaurante_valeria(models.Model):
#     _name = 'gestion_restaurante_valeria.gestion_restaurante_valeria'
#     _description = 'gestion_restaurante_valeria.gestion_restaurante_valeria'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

