import base64
import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

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
            state = kw["state"]
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
                'state': state,
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
                    'state': newUser.state,
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
                    'no_ktp': user.no_ktp,
                    'id_desa': user.id_desa,
                    'id_kecamatan': user.id_kecamatan,
                    'id_kk': user.id_kk,
                    'no_tps': user.no_tps,
                    'id_card': user.id_card,
                    'state': user.state,
                    
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
            
    @http.route('/api/update_user', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def updateUser(self, **kw):
        if 'id' not in kw:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`id` is required.'
            }), headers={'Content-Type': 'application/json'})

        try:
            user_id = int(kw["id"])
        except ValueError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`id` must be a valid integer.'
            }), headers={'Content-Type': 'application/json'})

        User = request.env['res.partner'].sudo()
        user_to_update = User.search([('id', '=', user_id)], limit=1)

        if not user_to_update:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'User with id {user_id} not found.'
            }), headers={'Content-Type': 'application/json'})

        try:
            user_to_update.write({
                'state': 'sudah diterima',
            })

            users_with_same_kk = User.search([('id_kk', '=', user_to_update.id_kk)])
            for user in users_with_same_kk:
                user.write({
                    'state': 'sudah diterima',
                })

            return request.make_response(json.dumps({
                'status': 'success',
                'message': 'Berhasil mengupdate user dan pengguna dengan id_kk yang sama',
            }), headers={'Content-Type': 'application/json'})

        except ValidationError as ve:
            _logger.error(f"Validation Error: {ve}")
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Validation error: {ve}',
            }), headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error(f"Error updating user: {e}")
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error updating user. Error: {e}',
            }), headers={'Content-Type': 'application/json'})
            
            
    @http.route('/api/get_user/', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def getUseridCard(self, **kw):
        if 'id_card' not in kw:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': 'id_card is required'
            }), headers={'Content-Type': 'application/json'})

        id_card = kw['id_card']
        User = request.env['res.partner'].sudo()
        user_data = User.search([('id_card', '=', id_card)], limit=1)

        if not user_data:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'User with id_card {id_card} not found.'
            }), headers={'Content-Type': 'application/json'})

        user_data = user_data[0]

        response_data = {
            'id': user_data.id,
            'name': user_data.name,
            'phone': user_data.phone,
            'street': user_data.street,
            'no_ktp': user_data.no_ktp,
            'id_desa': user_data.id_desa,
            'id_kecamatan': user_data.id_kecamatan,
            'id_kk': user_data.id_kk,
            'no_tps': user_data.no_tps,
            'id_card': user_data.id_card,
            'state': user_data.state,
        }

        return request.make_response(json.dumps({
            'status': 'success',
            'message': f'User with id_card {id_card} found.',
            'data': response_data,
        }), headers={'Content-Type': 'application/json'})
