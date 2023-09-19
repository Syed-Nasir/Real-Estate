from odoo import models, fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils



class estateProperty(models.Model):
    _name='estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Estate Property Model'
    _order='id desc'
    

    name=fields.Char(string='Name',required=True)
    description = fields.Char(string='Description')
    postcode= fields.Integer(string="Postcode")
    orientation = fields.Selection(selection=[
                                            ('north','North'),
                                            ('south','South'),
                                            ('west','West'),
                                            ('east','East')
                                            ])
    date_availability  = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3),copy=False, string='Available')                        
    expected_price = fields.Float(string='Expected Price')         
    selling_price = fields.Float (string='Selling price',copy=False)       
    bedrooms = fields.Integer (string='Bedrooms',default=2)                    
    living_area = fields.Integer (string='Living Area')                  
    facades = fields.Integer (string='Facades')                    
    garden = fields.Boolean (string='Garden')                                
    garden_area = fields.Integer (string='Garden Area')                  
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())

    active = fields.Boolean(selection=[
                                        (True,'Active'),
                                        (False,'Inactive')],default=True)

    state = fields.Selection(selection=[
                                        ('new','New'),
                                        ('offer_recieved','Offer Recieved'),
                                        ('offer_accepted','Offer Accepted'),
                                        ('sold','Sold'),
                                        ('cancelled','Cancelled')],required=True,copy=False,default='new', tracking = True)

    property_id = fields.Many2one('estate.property.type', string='Property Types')
    salesman_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag',widget="many2many_tags", string='Tags')
    offer_ids = fields.One2many('estate.property.offer','property_id',string='offers')
    total_area = fields.Float(compute='_compute_total', string='Total Area', store=True)
    best_price = fields.Float(compute='_compute_best_offer',string='Best Offer', store=True)
    property_type_id = fields.Many2one('estate.property.type',string='Property Types')
    color = fields.Integer(string = 'Color')

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_price=max(record.offer_ids.mapped('price'),default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.orientation='north'
        else:
            self.garden_area=0
            self.orientation=False


    def add_offer(self):
        action = self.env.ref('estate.launch_the_wizard').read()[0]
        return action
        

    def action_do_something(self):
        if self.state == 'cancelled':
            raise UserError('Cancelled property can not be Sold')
        else:
            self.state = "sold"
        

    def action_cancel_something(self):
        if self.state == 'sold':
            raise UserError('Sold property can not be Cancelled')
        else:
            self.state = 'cancelled'

    @api.constrains('property_id', 'tag_ids')
    def _check_names(self):
        for record in self:
            print("========================", record.tag_ids.mapped('name'))
            if record.property_id.name in  record.tag_ids.mapped('name'):
                raise ValidationError("Fields Property Type and Tags must be different..!")

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        
        for offer in self.offer_ids:
            if offer.status == "accepted":
                self.selling_price = offer.price
                break
        else:
            self.selling_price = 0

    def unlink(self):  
        if self.state not in ['new','cancelled']:
            raise ValidationError('You can not delete a property which is not new and cancelled')
        return super().unlink()

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive'),
        ('selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be strictly positive'),

    ]