from odoo import models, fields ,api
from odoo.exceptions import ValidationError
class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    id_card = fields.Char(string='No Seri Kartu Tim Sukses')
    id_kk = fields.Char(string='No Kartu Keluarga')
    no_ktp = fields.Char(string='No KTP')
    code_minigold = fields.Char(string='Kode Minigold')
    state_pilih = fields.Selection([
        ('sudah memilih', 'Sudah Memilih'),
        ('belum memilih', 'Belum Memilih'),
    ], string='Status Pemilihan', default='belum memilih')
    id_kabupaten= fields.Selection([
        ('',' - Pilih - '),
        ('banyumas','Banyumas'),
        ('cilacap','Cilacap'),
    ],string='Kabupaten', default='')
    id_kecamatan = fields.Selection([
        ('', ' - Pilih - '),
        ('patikraja', 'Patikraja'),
        ('purwokerto selatan', 'Purwokerto Selatan'),
        ('purwokerto barat', 'Purwokerto Barat'),
        ('purwokerto timur', 'Purwokerto Timur'),
        ('purwokerto utara', 'Purwokerto Utara'),
        ('sokaraja', 'Sokaraja'),
        ('kembaran', 'Kembaran'),
        ('sumbang', 'Sumbang'),
        ('baturraden', 'Baturraden'),
        ('kemranjen', 'Kemranjen'),
        ('umpiuh', 'Sumpiuh'),
        ('tambak', 'Tambak'),
        ('somagede', 'Somagede'),
        ('kalibagor', 'Kalibagor'),
        ('banyumas', 'Banyumas'),
        ('wangon', 'Wangon'),
        ('jatilawang', 'Jatilawang'),
        ('rawalo', 'Rawalo'),
        ('kebasen', 'Kebasen'),
        ('lumbir', 'Lumbir'),
        ('ajibarang', 'Ajibarang'),
        ('gumelar', 'Gumelar'),
        ('pekuncen', 'Pekuncen'),
        ('purwojati', 'Purwojati'),
        ('cilongok', 'Cilongok'),
        ('karanglewas', 'Karanglewas'),
        ('kedungbanteng', 'Kedungbanteng'),
        ('adipala', 'Adipala'),
        ('bantarsari', 'Bantarsari'),
        ('binangun', 'Binangun'),
        ('cilacap selatan', 'Cilacap Selatan'),
        ('cilacap tengah', 'Cilacap Tengah'),
        ('cilacap utara', 'Cilacap Utara'),
        ('cimanggu', 'Cimanggu'),
        ('cipari', 'Cipari'),
        ('dayeuhluhur', 'Dayeuhluhur'),
        ('gandrungmangu', 'Gandrungmangu'),
        ('jeruklegi', 'Jeruklegi'),
        ('kampung laut', 'Kampung Laut'),
        ('karangpucung', 'Karangpucung'),
        ('kawunganten', 'Kawunganten'),
        ('kedungreja', 'Kedungreja'),
        ('kesugihan', 'Kesugihan'),
        ('kroya', 'Kroya'),
        ('majenang', 'Majenang'),
        ('maos', 'Maos'),
        ('nusawungu', 'Nusawungu'),
        ('patimuan', 'Patimuan'),
        ('sampang', 'Sampang'),
        ('sidareja', 'Sidareja'),
        ('wanareja', 'Wanareja'),
    ], string='Kecamatan', default='')
    no_tps = fields.Char(string='No TPS')
    id_desa = fields.Char(string=' Desa')
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
    
    
   
