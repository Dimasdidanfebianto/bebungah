import base64
import json
import logging
import math
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

#api untuk REGISTRASI 
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
            
            existing_user = request.env['res.partner'].sudo().search([('no_ktp', '=', no_ktp)])
            if existing_user:
                return request.make_response(json.dumps({
                    'status': 'failed',
                    'message': 'User with same no ktp already exists.'
                }), headers={'Content-Type': 'application/json'})

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
        
        
    #ENDPOINT UNTUK GET ALL USER   
    @http.route('/api/get_all_users', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def get_all_users(self, **kw):
        try:
            User = request.env['res.partner'].sudo()

            page = int(kw.get('page', 1))
            limit = int(kw.get('limit', 20)) 

            try:
                page = max(page, 1)
                limit = max(limit, 1)
            except ValueError:
                page = 1
                limit = 10

            offset = (page - 1) * limit

            id_kk = kw.get('id_kk', False)
            domain = [('id_kk', '=', id_kk)] if id_kk else []
            users = User.search(domain, offset=offset, limit=limit)



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
                    'state_card': user.state_card,
                    'state_pilih': user.state_pilih,
                    'code_minigold': user.code_minigold
                })

            total_count = User.search_count([])

            total_pages = math.ceil(total_count / limit)

            meta = {
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }

            return request.make_response(json.dumps({
                'status': 'success',
                'message': 'Berhasil mendapatkan data semua user',
                'data': user_data,
                'meta': meta
            }), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error: {e}',
            }), headers={'Content-Type': 'application/json'})

    #ENDPOINT UNTUK UPDATE STATUS PEMILIH USER        
    @http.route('/api/update_user', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def updateUser(self, **kw):
        if 'code_minigold' not in kw:
            return self.error_response('`code_minigold` is required.')

        try:
            minigold = request.env['res.partner'].sudo()
            user_to_update = minigold.search([('code_minigold', '=', kw['code_minigold'])], limit=1)

            if not user_to_update:
                return self.error_response(f'User with code_minigold {kw["code_minigold"]} not found.')

            user_to_update.write({
                'state_pilih': 'sudah memilih',
            })

            return self.success_response('Berhasil mengupdate user.')

        except ValidationError as ve:
            _logger.error(f"Validation Error: {ve}")
            return self.error_response(f'Validation error: {ve}')

        except Exception as e:
            _logger.error(f"Error updating user: {e}")
            return self.error_response(f'Error updating user. Error: {e}')
            
     #ENDPOINT UNTUK GET USER BY ID_CARD       
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
            'state_card': user_data.state_card,
            'state_pilih': user_data.state_pilih,
        }

        return request.make_response(json.dumps({
            'status': 'success',
            'message': f'User with id_card {id_card} found.',
            'data': response_data,
        }), headers={'Content-Type': 'application/json'})
        
        
     #ENDPOINT UNTUK UPDATE BANTUAN    
    @http.route('/api/update_bantuan/', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def updateBantuan(self, **kw):
        if 'code_minigold' not in kw:
            return self.error_response('`code_minigold` is required.')

        try:
            minigold = request.env['res.partner'].sudo()
            user_to_update = minigold.search([('code_minigold', '=', kw['code_minigold'])], limit=1)

            if not user_to_update:
                return self.error_response(f'User with code_minigold {kw["code_minigold"]} not found.')

            user_to_update.write({
                'state': 'sudah diterima',
            })

            return self.success_response('Berhasil mengupdate user.')

        except ValidationError as ve:
            _logger.error(f"Validation Error: {ve}")
            return self.error_response(f'Validation error: {ve}')

        except Exception as e:
            _logger.error(f"Error updating user: {e}")
            return self.error_response(f'Error updating user. Error: {e}')
                
            
        

        
         

        
        


            
    




        
        
