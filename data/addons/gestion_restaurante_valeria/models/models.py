from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class Plato(models.Model):
    _name = 'gestion_restaurante_valeria.plato'
    _description = 'Modelo para gestionar los platos del restaurante'

    name = fields.Char(string="Nombre del Plato", required=True)
    description = fields.Text(string="Ingredientes/Descripción")
    price = fields.Float(string="Precio", required=True)
    preparation_time = fields.Integer(string="Tiempo de Preparación (minutos)", required=False, help="Tiempo estimado de preparación del plato")
    available = fields.Boolean(string="Disponible", default=True, required=True, help="Indica si el plato puede ser preparado en este momento")
    categoria_id = fields.Many2one('gestion_restaurante_valeria.categoria', string="Categoría", required=True)
    chef_id = fields.Many2one('gestion_restaurante_valeria.chef', string = 'Chef responsable')
    codigo = fields.Char(string="Código", required=True, compute="_get_codigo", readonly=True)
    chef_especializado = fields.Many2one('gestion_restaurante_valeria.chef', string = "Chef especializado", compute='compute_chef_especializado', store=True)
    menu = fields.Many2one(
        'gestion_restaurante_valeria.menu',
        string='Menú',
        ondelete='set null'
    )
    rel_ingredientes = fields.Many2many(
        comodel_name='gestion_restaurante_valeria.ingrediente',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes'
    )
    precio_iva = fields.Float(string="Precio con IVA", compute="_compute_precio_iva")
    descuento = fields.Float(string="Descuento (%)")
    precio_final = fields.Float(string="Precio Final", compute="_compute_precio_final", store=True)
    especialidad_chef = fields.Many2one('gestion_restaurante_valeria.categoria', string = "Especialidad del chef asignado", related = chef_id.especialidad, readonly=True)
    
    #método para asignar chef
    @api.depends('categoria_id')
    def _compute_chef_especializado(self): #TODO: ESTOY AQUIIIII
        for chef in self:
            try:
                _logger.debug(f"Buscando chef especializado...")
                if chef.categoria_id:
                    chef.chef_especializado = self.env['gestion_restaurante_valeria.chef'].search([('especialidad', '=', chef.categoria_id.id)], limit=1)
                    if not chef.chef_especializado:
                        _logger.warning(f"No se encontró chef especializado para la categoría {chef.categoria_id.name}")
            except Exception as e:
                raise ValidationError(f"Error al asignar chef: {str(e)}")       
                
    @api.depends('categoria_id')
    def _get_codigo(self):  
        for plato in self:
            try:
                _logger.debug(f"Generando código para plato ID: {plato.id}")
                if plato.categoria_id:
                    plato.codigo = f"{plato.categoria_id.name[:3].upper()}_{plato.id}" 
                else:
                    _logger.warning(f"Plato {plato.id} creado sin categoría")
                    plato.codigo = f"PLT_{plato.id}"
                _logger.info(f"Plato '{plato.name}' creado con precio {plato.price}")
            except Exception as e:
                raise ValidationError(f"No se pudo generar el código: {str(e)}")
    #método para añadir iva al precio
    @api.depends('price')
    def _compute_precio_iva(self):
        for plato in self:
            plato.precio_iva = plato.price * 1.10   
    #método para calcular descuento
    @api.depends('price', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if plato.price:
                if plato.descuento > 0:
                    plato.precio_final = plato.price * (1 - plato.descuento / 100)
                else:
                    plato.precio_final = plato.price
            else:
                _logger.error(f"Error calculando precio para plato {plato.id}: precio no definido")
                plato.precio_final = 0.0
    # método para validar precio
    @api.constrains('price')
    def _check_price(self):
        for plato in self:
            if plato.price < 0:
                raise ValidationError("El precio no puede ser negativo.")
    # método para validar tiempo de preparación - rangos
    @api.constrains('preparation_time')
    def _check_prep_time(self):
        for plato in self:
            if plato.preparation_time:
                if plato.preparation_time < 1 or plato.preparation_time > 240:
                    raise ValidationError("El tiempo debe ser 1-240 minutos")


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

    # método para validar fechas del menú
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for menu in self:
            if menu.fecha_inicio and menu.fecha_fin:
                if menu.fecha_fin < menu.fecha_inicio:
                    raise ValidationError("La fecha fin no puede ser anterior a la de inicio.")

    # validar menu con platos
    @api.constrains('platos_ids', 'activo')
    def _check_platos_menu(self):
        for menu in self:
            if menu.activo and len(menu.platos_ids) == 0:
                raise ValidationError("Un menú activo debe tener al menos un plato.")


class Ingrediente(models.Model):
    _name = 'gestion_restaurante_valeria.ingrediente'
    _description = 'Modelo para la gestión de los Ingredientes de los platos'

    name = fields.Char(string="Nombre", required=True)
    es_alergeno = fields.Boolean(string="¿Alérgenos?", default=False)
    descripcion = fields.Text(string="Descripción")
    
    rel_platos = fields.Many2many(
        comodel_name='gestion_restaurante_valeria.plato',
        relation='relacion_platos_ingredientes',
        column1='rel_ingredientes',
        column2='rel_platos',
        string='Platos que lo contienen'
    )

class Categoria(models.Model):
    _name = 'gestion_restaurante_valeria.categoria'
    _description = 'Modelo para gestionar las categorías de platos'

    name = fields.Char(string = "Nombre de la Categoría", required=True)
    description = fields.Text(string = "Descripción de la categoría")
    platos_ids = fields.One2many('gestion_restaurante_valeria.plato', 'categoria_id', string='Platos pertenecientes a esta categoría')
    ingredientes_comunes_ids = fields.Many2many('gestion_restaurante_valeria.ingrediente', string="Ingredientes comunes en esta categoría", compute = "_compute_ingredientes_comunes")

    @api.depends('platos_ids', 'platos_ids.rel_ingredientes')
    def _compute_ingredientes_comunes(self):
       for categoria in self:
           ingredientes_acumulados = self.env['gestion_restaurante_valeria.ingrediente']
           for plato in categoria.platos_ids:
                ingredientes_acumulados = ingredientes_acumulados + plato.rel_ingredientes
           categoria.ingredientes_comunes_ids = ingredientes_acumulados
           
     # modelo chef
class Chef(models.Model):
    _name = 'gestion_restaurante_valeria.chef'
    _description = 'Modelo para gestionar los chefs del restaurante'

    name = fields.Char(string="Nombre del Chef", required=True)
    especialidad = fields.Many2one('gestion_restaurante_valeria.categoria', string="Especialidad del Chef")
    platos_ids = fields.One2many('gestion_restaurante_valeria.plato', 'chef_id', string='Platos asignados al Chef')