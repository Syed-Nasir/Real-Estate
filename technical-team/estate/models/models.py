from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'academy.teachers'
    # _inherit = 'estate.property'

    name = fields.Char()
    # property_id = fields.Many2one('estate.property.type', string='Properties', domain=[("state", "in", ["new", "offer_received"])] )