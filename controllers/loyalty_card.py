import json
from odoo import http
from odoo.http import request

class BerbungahCard(http.Controller): 
    @http.route('/api/loyalty_card/', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def get_all_card(self, **kw):
        try:
            Card = request.env['loyalty.card'].sudo()
            
            card_data = []
            for card in Card.search([]):
                card_data.append({
                    'program_id': card.id,
                    'code': card.code,
                    'partner_id': card.partner_id.id,
                })
            return http.request.make_response(json.dumps(card_data), headers={'Content-Type': 'application/json'})
        
        except Exception as e:
            return http.request.make_response(json.dumps({'error': str(e)}), headers={'Content-Type': 'application/json'})
    
    @http.route('/api/update_code/', auth='user', methods=["POST"], csrf=False, cors="*", website=False)
    def assign_partner_to_card(self, **kw):
        try:
            if 'new_code' not in kw or 'partner_id' not in kw:
                return self.error_response('new_code dan partner_id diperlukan.')
            
            new_code_value = kw["new_code"]
            partner_id = int(kw["partner_id"])
            new_id_card = kw["id_card"]
            Card = request.env['loyalty.card'].sudo()
            card = Card.search([('partner_id', '=', False)], limit=1)

            if not card:
                return http.request.make_response(
                    json.dumps({'error': 'No available loyalty card with partner_id=False'}),
                    headers={'Content-Type': 'application/json'}
                )

            card.write({'partner_id': partner_id, 'code': new_code_value})

            partner = card.partner_id 
            partner.sudo().write({'code_minigold': new_code_value, 'state_card': 'aktif', 'id_card': new_id_card})

            card_data = {
                'program_id': card.id,
                'code': new_code_value,
                'partner_id': partner_id,
            }

            return http.request.make_response(
                json.dumps(card_data),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            return http.request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )

        
