# -*- coding: utf-8 -*-
# from odoo import http


# class XyzExample(http.Controller):
#     @http.route('/xyz_example/xyz_example', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xyz_example/xyz_example/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('xyz_example.listing', {
#             'root': '/xyz_example/xyz_example',
#             'objects': http.request.env['xyz_example.xyz_example'].search([]),
#         })

#     @http.route('/xyz_example/xyz_example/objects/<model("xyz_example.xyz_example"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xyz_example.object', {
#             'object': obj
#         })
