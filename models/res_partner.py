from odoo import models, fields ,api


class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    id_card = fields.Binary(string='Foto KTP')
    
    id_kk = fields.Char(string='No Kartu Keluarga')
    no_tps = fields.Char(string='No TPS')
    