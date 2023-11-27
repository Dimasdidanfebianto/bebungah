from odoo import models, fields ,api


class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    id_card = fields.Char(string='No Seri Kartu Tim Sukses')
    id_kk = fields.Char(string='No Kartu Keluarga')
    no_tps = fields.Char(string='No TPS')
    no_ktp = fields.Char(string='No KTP')
    id_kecamatan = fields.Char(string='Kecamatan')
    id_desa = fields.Char(string='Desa')
    id_foto = fields.Binary(string='Foto Kartu Tim Sukses')
    state= fields.Selection([
        ('sudah diterima', 'Sudah Diterima'),
        ('belum diterima', 'Belum Diterima'),
    ], string='Status Bantuan', default='belum diterima')
    
    