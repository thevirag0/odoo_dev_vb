# from odoo import http


# class GestionRestauranteValeria(http.Controller):
#     @http.route('/gestion_restaurante_valeria/gestion_restaurante_valeria', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_valeria/gestion_restaurante_valeria/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_valeria.listing', {
#             'root': '/gestion_restaurante_valeria/gestion_restaurante_valeria',
#             'objects': http.request.env['gestion_restaurante_valeria.gestion_restaurante_valeria'].search([]),
#         })

#     @http.route('/gestion_restaurante_valeria/gestion_restaurante_valeria/objects/<model("gestion_restaurante_valeria.gestion_restaurante_valeria"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_valeria.object', {
#             'object': obj
#         })

