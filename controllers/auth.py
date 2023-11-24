import base64
import io
from odoo import http
from odoo.http import request
import json
import logging


_logger = logging.getLogger(__name__)


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

    @http.route('/api/create', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def userCreate(self, **kw):
        name = kw["name"]
        phone = kw["phone"]
        street = kw["street"]
        id_card = kw["id_card"]
        try:
            image_binary = base64.b64encode(kw['image_1920'].read()) if kw.get('image_1920') else False
            id_card = base64.b64encode(kw['id_card'].read()) if kw.get('id_card') else False

            User = request.env['res.partner'].sudo()
            newUser = User.create({
                'name': name,
                'phone': phone,
                'street': street,
                'image_1920': image_binary,
                'id_card ': image_binary
            })
     
        except Exception as e:
            _logger.error(f"Error creating user: {e}")
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error creating user. Error: {e}',
            }), headers={'Content-Type': 'application/json'})
        image_base64 = image_binary.decode('utf-8') if image_binary else None
    
        
        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'Berhasil menambahkan user',
            'data': {
                'id': newUser.id,
                'name': newUser.name,
                'phone': newUser.phone,
                'street': newUser.street,
                'image_1920': image_base64,
                'id_card': id_card
            }
        }), headers={'Content-Type': 'application/json'})

    def convert_image_to_base64(self, image):
        try:
            encoded_image = base64.b64encode(image.read())
            return encoded_image
        except Exception as e:
            _logger.error(f"Error converting image to base64: {e}")
            
            return None
        
    @http.route('/api/upload/profilePhoto', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def uploadProfilePhoto(self, **kw):
        photoUser = request.env['res.partner'].sudo().search([
            ("id", "=", request.env.uid)
        ])

        photoUser = photoUser[0]

        image_1920 = request.httprequest.files.getlist('Profile')

        for file in image_1920:
            attachment = file.read()
            redableProfile = io.BytesIO(attachment)
    
        encodedImage = base64.b64encode(redableProfile.getvalue())

        photoUser.write({
            'image_1920': encodedImage
        })
        
        return request.make_response(json.dumps(       {
            'status': 'success',
            'message': 'Photo Profile Berhasil Diedit',
            }), headers={'Content-Type': 'application/json'})
        
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
                    
                })

            return request.make_response(json.dumps({
                'status': 'success',
                'message': 'Berhasil mendapatkan user',
                'data': user_data,
            }), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': f'Error: {e}',
            }), headers={'Content-Type': 'application/json'})    
