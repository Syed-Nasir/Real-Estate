from odoo import models, fields,api

class estatePropertyWizard(models.TransientModel):
    _name='estate.property.wizard'
    _description='Estate Property Model Wizard'

    # name = fields.Char(string = 'Name', required = True)
    price = fields.Float(string='Price',required=True)    

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    # date_deadline   = fields.Date(compute='_compute_deadline',inverse='_inverse_compute_deadline',string='Date Deadline')



    def make_offer(self):
        properties = self.env.context.get('active_ids')
        print("===========selected==============", properties)
        for record in properties:
            offer =  self.env['estate.property.offer'].create({
                'property_id':record,
                'price': self.price,
                'partner_id': self.buyer_id.id,
                # 'date_deadline': self.date_deadline
            })
        return offer

    