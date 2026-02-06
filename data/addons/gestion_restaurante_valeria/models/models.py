from odoo import models, fields, api


class Plato(models.Model):
    _name = 'gestion_restaurante_valeria.plato'
    _description = 'Modelo para gestionar los platos del restaurante'

    name = fields.Char(string="Nombre del Plato", required=True)
    description = fields.Text(string="Ingredientes/Descripción")
    price = fields.Float(string="Precio", required=True)
    preparation_time = fields.Integer(string="Tiempo de Preparación (minutos)", required=False, help="Tiempo estimado de preparación del plato")
    available = fields.Boolean(string="Disponible", default=True, required=True, help="Indica si el plato puede ser preparado en este momento")
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
    menu = fields.Many2one(
        'gestion_restaurante_valeria.menu',
        string = 'Menú',
        ondelete='set null'
    )
    rel_ingredientes = fields.Many2many(
        comodel_name = 'gestion_restaurante_valeria.ingrediente',
        relation = 'relacion_platos_ingredientes',
        column1 = 'rel_platos',
        column2 = 'rel_ingredientes',
        string = 'Ingredientes'
    )


class Menu(models.Model):
    _name = 'gestion_restaurante_valeria.menu'
    _description = 'Modelo para gestionar los menús del restaurante'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de final")
    activo = fields.Boolean(string="Activo", default=True)
    platos = fields.One2many(
        'gestion_restaurante_valeria.plato',
        'menu',
        string='Platos del Menú'
    )
    
class Ingrediente(models.Model):
    _name = 'gestion_restaurante_valeria.ingrediente'
    _description = 'Modelo para la gestión de los Ingredientes de los platos'

    name = fields.Char(string="Nombre", required=True)
    es_alergeno = fields.Boolean(string="¿Alérgenos?", default=False)
    descripcion = fields.Text(string="Descripción")
    
    rel_platos = fields.Many2many(
        comodel_name = 'gestion_restaurante_valeria.plato',
        relation = 'relacion_platos_ingredientes',
        column1 = 'rel_ingredientes',
        column2 = 'rel_platos',
        string = 'Platos que lo contienen'
    )