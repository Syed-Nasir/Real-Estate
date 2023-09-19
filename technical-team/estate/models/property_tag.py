from odoo import models, fields

class estateProperty(models.Model):
    _name='estate.property.tag'
    _description='Estate Property Tags'
    _order='name'
    

    name=fields.Char(string='Name',required=True)
    color = fields.Integer(string='Color')
