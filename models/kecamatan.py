from odoo import models, fields, api

class ResPartnerKecamatan(models.Model):
    _name = 'bebungah.kecamatan'
    _description = 'bebungah.kecamatan'

    name = fields.Char(string='Nama Kecamatan', required=True)
    id_kabupaten = fields.Many2one('bebungah.kabupaten', string='Kabupaten')
    