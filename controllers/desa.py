import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class DesaAPI(http.Controller):

    @http.route('/api/assign_desa/', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def assign_desa(self, **kw):
        try:
            if 'id_desa' not in kw:
                return request.make_response(json.dumps({
                    'status': 'failed',
                    'message': 'id_desa diperlukan.'
                }), headers={'Content-Type': 'application/json'})

            id_desa_value = kw["id_desa"]


            desa_model = request.env['res.partner']

            desa_record = desa_model.sudo().search([('id_desa', '=', id_desa_value)], limit=1)

            if not desa_record:
                return request.make_response(json.dumps({
                    'status': 'failed',
                    'message': f'Record dengan id_desa {id_desa_value} tidak ditemukan.'
                }), headers={'Content-Type': 'application/json'})

            if not desa_record.name:
                return request.make_response(json.dumps({
                    'status': 'failed',
                    'message': f'Record dengan id_desa {id_desa_value} tidak memiliki nama desa.'
                }), headers={'Content-Type': 'application/json'})

        
            return request.make_response(json.dumps({
                'status': 'success',
                'message': f'Asignasi berhasil untuk desa dengan id_desa {id_desa_value}.',
                'desa_data': {
                    'id': desa_record.id,
                    'name': desa_record.name,
                    
                }
            }), headers={'Content-Type': 'application/json'})


        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': str(e)
            }), headers={'Content-Type': 'application/json'})
