from odoo import models, fields, api

class ResPartnerKabupaten(models.Model):
    _name = 'bebungah.kabupaten'
    _description = 'bebungah.kabupaten'

    name = fields.Char(string='Nama Kabupaten', required=True)
    kecamatan_ids = fields.One2many('bebungah.kecamatan', 'id_kabupaten', string='Kecamatans')