from odoo import models, fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class estateProperty(models.Model):
    _name='estate.property.offer'
    _description='Estate Property offers'
    _order = 'price desc'
    

    price           = fields.Float(string='Price',required=True)
    status          = fields.Selection(selection=[('accepted','Accepted'),('rejected','Rejected')],string='Status',copy=False)        
    partner_id      = fields.Many2one('res.partner',string='Partner',required=True)
    property_id     = fields.Many2one('estate.property',required=True)
    validity        = fields.Integer(string='Validity', default=7)
    date_deadline   = fields.Date(compute='_compute_deadline',inverse='_inverse_compute_deadline',string='Date Deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)



    @api.depends('validity','date_deadline')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline=fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_compute_deadline(self):
        for record in self:
            record.validity=(record.date_deadline - fields.Date.today()).days
    
    # def action_accepted(self):
    #     self.status = 'accepted'
    #     self.property_id.selling_price = self.price 
    #     self.property_id.buyer_id = self.partner_id.id
    #     self.property_id.state="offer_accepted"

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get('price'):
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                lower_price_offer = min(prop.offer_ids.mapped("price"))
                # print("==================", self.price, vals.get('price'))
                if vals.get('price') < lower_price_offer:
                    raise UserError("The offer must be higher than the existing offers")
            prop.state = 'offer_recieved'
        return super().create(vals)


    def action_accepted(self):
        # print('+++++++++++++++++++++++++++')
        for len1 in self:
            record1 = len1.mapped('property_id.offer_ids.status')

            for record in len1:
                if 'accepted' in record1:
                    raise ValidationError('One Offer Already acepted')

                else:
                    if  record.price >= self.property_id.expected_price * 0.9:
                        record.status = 'accepted'
                        record.property_id.selling_price = record.price
                        record.property_id.buyer_id = record.partner_id.id
                        record.property_id.state ='offer_accepted'
                    else:
                        raise ValidationError("Selling Price cannot be lower than 90% of the Expected Price.")
            

    def action_refused(self):
        self.status = 'rejected'
        self.property_id.selling_price = 0

    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
         'The offer price should be strictly positive'),
        ]
        