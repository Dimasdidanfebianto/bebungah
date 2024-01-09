from odoo import models, fields, api

class ResPartnerKabupaten(models.Model):
    _name = 'bebungah.kabupaten'
    _description = 'bebungah.kabupaten'

    name = fields.Char(string='Nama Kabupaten', required=True)
    # kabupaten_id = fields.Many2one('bebungah.kabupaten', string='Kabupaten')
    