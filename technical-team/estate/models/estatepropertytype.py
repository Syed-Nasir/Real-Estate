from odoo import models, fields, api

class estateProperty(models.Model):
    _name='estate.property.type'
    _description='Estate Property Types'
    _order='sequence, name'
    

    name=fields.Char(string='Name',required=True)
    expected_price = fields.Float(string='Expected Price')           
    state = fields.Selection(selection=[('new','New'),('offer_recieved','Offer Recieved'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],required=True,copy=False,default='new')
    property_ids = fields.One2many('estate.property','property_type_id', string='Property Types')
    sequence = fields.Integer('Sequence',default = 1)
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for offers in self:
            offers.offer_count = self.env['estate.property.offer'].search_count([('property_type_id', '=', self.id)])
