# -*- coding: utf-8 -*-
# from odoo import http


# class Bebungah(http.Controller):
#     @http.route('/bebungah/bebungah/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bebungah/bebungah/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bebungah.listing', {
#             'root': '/bebungah/bebungah',
#             'objects': http.request.env['bebungah.bebungah'].search([]),
#         })

#     @http.route('/bebungah/bebungah/objects/<model("bebungah.bebungah"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bebungah.object', {
#             'object': obj
#         })
