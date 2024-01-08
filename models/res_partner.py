from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartnerKabupaten(models.Model):
    _name = 'res.partner.kabupaten'
    _description = 'Kabupaten'

    name = fields.Char(string='Nama Kabupaten', required=True)
    kecamatan_ids = fields.One2many('res.partner.kecamatan', 'kabupaten_id', string='Kecamatans')

class ResPartnerKecamatan(models.Model):
    _name = 'res.partner.kecamatan'
    _description = 'Kecamatan'

    name = fields.Char(string='Nama Kecamatan', required=True)
    kabupaten_id = fields.Many2one('res.partner.kabupaten', string='Kabupaten')

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    id_card = fields.Char(string='No Seri Kartu Tim Sukses')
    id_kk = fields.Char(string='No Kartu Keluarga')
    no_ktp = fields.Char(string='No KTP')
    code_minigold = fields.Char(string='Kode Minigold')
    state_pilih = fields.Selection([
        ('sudah memilih', 'Sudah Memilih'),
        ('belum memilih', 'Belum Memilih'),
    ], string='Status Pemilihan', default='belum memilih')
    kabupaten_id = fields.Many2one('res.partner.kabupaten', string='Kabupaten')
    kecamatan_id = fields.Many2one('res.partner.kecamatan', string='Kecamatan')
    no_tps = fields.Char(string='No TPS')
        
    id_desa = fields.Char(string='Nama Desa')
    id_foto = fields.Binary(string='Foto Kartu Tim Sukses')
    state_card = fields.Selection([
        ('aktif', 'Aktif'),
        ('belum aktif', 'Belum Aktif'),
    ], string='Status Kartu Tim Sukses', default='belum aktif')
    state= fields.Selection([
        ('sudah diterima', 'Sudah Diterima'),
        ('belum diterima', 'Belum Diterima'),
    ], string='Status Bantuan', default='belum diterima')
    
    @api.constrains('no_ktp')
    def _check_unique_no_ktp(self):
        for record in self:
            existing_record = self.search([('no_ktp', '=', record.no_ktp)])
            if len(existing_record) > 1:
                raise ValidationError('No KTP already exists.')
