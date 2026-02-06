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
            ('principal', 'Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida')
        ],
        default='principal'
    )
    codigo = fields.Char(string="Código", required=True, compute="_get_codigo", readonly=True)

    @api.depends('category')
    def _get_codigo(self):  
        for plato in self:
            if plato.category:
                plato.codigo = f"{plato.category[:3].upper()}_{plato.id}" 
            else:
                plato.codigo = f"PLT_{plato.id}"
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
    precio_iva = fields.Float(string = "Precio con IVA", compute="_compute_precio_iva")
    @api.depends('price')
    def _compute_precio_iva(self):
        for plato in self:
            plato.precio_iva = plato.price * 1.10   
    descuento = fields.Float(string="Descuento (%)")
    precio_final = fields.Float(string="Precio Final", compute="_compute_precio_final", store=True)
    @api.depends('price', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if plato.price:
                if plato.descuento > 0:
                    plato.precio_final = plato.price * (1 - plato.descuento / 100)
                else:
                    plato.precio_final = plato.price
            else: 
                plato.precio_final = 0.0


class Menu(models.Model):
    _name = 'gestion_restaurante_valeria.menu'
    _description = 'Modelo para gestionar los menús del restaurante'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de final")
    activo = fields.Boolean(string="Activo", default=True)
    platos_ids = fields.One2many(
        'gestion_restaurante_valeria.plato',
        'menu',
        string='Platos del Menú'
    )
    precio_total = fields.Float(string="Precio Total", compute="_compute_precio_total", store=True)

    @api.depends('platos_ids', 'platos_ids.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            if menu.platos_ids:
                total = 0.0
                for plato in menu.platos_ids:
                    total += plato.precio_final
                menu.precio_total = total
            else:
                menu.precio_total = 0.0
    
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