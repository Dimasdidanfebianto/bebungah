from odoo import models, fields, api

class ResPartnerKabupaten(models.Model):
    _name = 'bebungah.kecamatan'
    _description = 'bebungah.kecamatan'

    name = fields.Char(string='Nama Kecamatan', required=True)
    # kecamatan_ids = fields.One2many('bebungah.kecamatan', 'kabupaten_id', string='Kecamatans')
    