import json
import logging
from odoo import http
from odoo.http import request


class BebungahAuth(http.Controller):
    @http.route('/api/login/', auth='public', methods=["POST"], csrf=False, cors="*", website=True)
    def login(self, **kw):
       # Validation
       try:
           login = kw["username"] 
       except KeyError:
           return request.make_response(json.dumps( {
                'status': 'failed',
                'message': '`username` is required.'
            }), headers={'Content-Type': 'application/json'})
       
       try:
           password = kw["password"]
       except KeyError:
           return request.make_response(json.dumps( {
                'status': 'failed',
                'message': '`password` is required.'
            }), headers={'Content-Type': 'application/json'})
       try:
           db = kw["db"]
           
       except KeyError:
           return request.make_response(json.dumps( {
                'status': 'failed',
                'message': '`db` is required.'
            }), headers={'Content-Type': 'application/json'})
       # Auth user
       http.request.session.authenticate(db, login, password)
       # Session info
       res = request.env['ir.http'].session_info()
       return request.make_response(json.dumps(res), headers={'Content-Type': 'application/json'})

     
