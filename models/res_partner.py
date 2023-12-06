from odoo import models, fields ,api
from odoo.exceptions import ValidationError



class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    id_card = fields.Char(string='No Seri Kartu Tim Sukses')
    id_kk = fields.Char(string='No Kartu Keluarga')
    no_ktp = fields.Char(string='No KTP')
    id_kecamatan = fields.Selection([
        ('',' - Pilih - '),
        ('pekuncen','Pekuncen'),
        ('ajibarang','Ajibarang'),
        ('gumelar','Gumelar'),
        ('lumbir','Lumbir'),
        ],string='Kecamatan', default='')
    no_tps = fields.Selection([
        ('',' - Pilih - '),
        ('01',' 01'),
        ('02',' 02'),
        ('03',' 03'),
        ('04',' 04'),
        ('05',' 05'),
        ('06',' 06'),
        ('07',' 07'),
        ('08',' 08'),
        ('09',' 09'),
        ('10',' 10'),
        ('11',' 11'),
        ('12',' 12'),
        ('13',' 13'),
        ('14',' 14'),
        ('15',' 15'),
        ('16',' 16'),
        ('17',' 17'),
        ('18',' 18'),
        ('19',' 19'),
        ('20',' 20'),
        ('21',' 21'),
        ('22',' 22'),
        ('23',' 23'),
        ('24',' 24'),
        ('25',' 25'),
        ('26',' 26'),
        ('27',' 27'),
        ('28',' 28'),
        ('29',' 29'),
        ('30',' 30'),
        ('31',' 31'),
        ('32',' 32'),
        ('33',' 33'),
        ('34',' 34'),
        ('35',' 35'),
        ('36',' 36'),
    ], string='No TPS', default='')
    id_desa = fields.Selection([
        ('',' - Pilih - '),
        ('ajibarang kulon',' Ajibarang Kulon'),
        ('ajibarang wetan',' Ajibarang Wetan'),
        ('banjarsari',' Banjarsari'),
        ('ciberung',' Ciberung'),
        ('darmakradenan',' Darmakradenan'),
        ('jingkang',' Jingkang'),
        ('kalibenda',' Kalibenda'),
        ('karangbawang',' Karangbawang'),
        ('kracak',' Kracak'),
        ('lesmana',' Lesmana'),
        ('pancasan',' Pancasan'),
        ('pandansari',' Pandansari'),
        ('sawangan',' Sawangan'),
        ('tipar kidul',' Tipar Kidul'),
        ('parakan',' Parakan'),
        ('banjaranyar',' Banjaranyar'),
        ('candinegara',' Candinegara'),
        ('cibangkong',' Cibangkong'),
        ('cikembulan',' Cikembulan'),
        ('glempang',' Glempang'),
        ('karangkemiri',' Karangkemiri'),
        ('karangklesem',' Karangklesem'),
        ('krajan',' Krajan'),
        ('kranggan',' Kranggan'),
        ('pasiraman kidul',' Pasiraman Kidul'),
        ('pasiraman lor',' Pasiraman Lor'),
        ('pekuncen',' Pekuncen'),
        ('petahunan',' Petahunan'),
        ('semedo',' Semedo'),
        ('tumiyang',' Tumiyang'),
        ('cihonje',' Cihonje'),
        ('cilangkap',' Cilangkap'),
        ('gancang',' Gancang'),
        ('gumelar',' Gumelar'),
        ('karangkemojing',' Karangkemojing'),
        ('kedungurang',' Kedungurang'),
        ('paningkaban',' Paningkaban'),
        ('samudra',' Samudra'),
        ('samudra kulon',' Samudra Kulon'),
        ('tlaga',' Tlaga'),
        ('besuki',' Besuki'),
        ('canduk',' Canduk'),
        ('cidora',' Cidora'),
        ('cingebul',' Cingebul'),
        ('cirahab',' Cirahab'),
        ('dermaji',' Dermaji'),
        ('karanggayam',' Karanggayam'),
        ('kedunggede',' Kedunggede'),
        ('lumbir',' Lumbir'),
        ('parungkamal',' Parungkamal'),
        ], string='Desa', default='')
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
    
    
   
