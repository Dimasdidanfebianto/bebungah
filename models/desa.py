from odoo import models, fields, api

class ResPartnerDesa(models.Model):
    _name = 'bebungah.desa'
    _description = 'bebungah.desa'

    name = fields.Char(string='Nama Desa', required=True)
    