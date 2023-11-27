import base64
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class BebungahUser(http.Controller):

    @http.route('/api/create', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def userCreate(self, **kw):
        try:
            name = kw["name"]
            phone = kw["phone"]
            street = kw["street"]
            no_ktp = kw["no_ktp"]
            id_desa = kw["id_desa"]
            id_kecamatan = kw["id_kecamatan"]
            id_kk = kw["id_kk"]
            no_tps = kw["no_tps"]
            id_card = kw["id_card"]
            id_foto = kw["id_foto"]
            image_1920 = kw["image_1920"]

            image_base64_1920 = base64.b64encode(image_1920.read()).decode('utf-8') if image_1920 else None
            image_base64_id_foto = base64.b64encode(id_foto.read()).decode('utf-8') if id_foto else None

            User = request.env['res.partner'].sudo()
            newUser = User.create({
                'name': name,
                'phone': phone,
                'street': street,
                'no_ktp': no_ktp,
                'id_desa': id_desa,
                'id_kecamatan': id_kecamatan,
                'id_kk': id_kk,
                'no_tps': no_tps,
                'id_card': id_card,
                'id_foto': image_base64_id_foto,
                'image_1920': image_base64_1920
            })

            return request.make_response(json.dumps({
                'status': 'success',
                'message': 'Berhasil menambahkan user',
                'data': {
                    'id': newUser.id,
                    'name': newUser.name,
                    'phone': newUser.phone,
                    'street': newUser.street,
                    'no_ktp': newUser.no_ktp,
                    'id_desa': newUser.id_desa,
                    'id_kecamatan': newUser.id_kecamatan,
                    'id_kk': newUser.id_kk,
                    'no_tps': newUser.no_tps,
                    'id_card': newUser.id_card,
                    'id_foto': image_base64_id_foto,
                    'image_1920': image_base64_1920
                }
            }), headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error(f"Error creating user: {e}")
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error creating user. Error: {e}',
            }), headers={'Content-Type': 'application/json'})


    def convert_image_to_base64(self, image):
        try:
            encoded_image = base64.b64encode(image.read())
            return encoded_image
        except Exception as e:
            _logger.error(f"Error converting image to base64: {e}")
                
            return None
        
    @http.route('/api/get_all_users', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def get_all_users(self, **kw):
        try:
            User = request.env['res.partner'].sudo()
            users = User.search([])

            user_data = []
            for user in users:
                user_data.append({
                    'id': user.id,
                    'name': user.name,
                    'phone': user.phone,
                    'street': user.street,
                    'id_kk': user.id_kk,
                    'no_tps': user.no_tps
                    
                })

            return request.make_response(json.dumps({
                'status': 'success',
                'message': 'Berhasil mendapatkan  data semua user',
                'data': user_data,
            }), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error: {e}',
            }), headers={'Content-Type': 'application/json'})   
