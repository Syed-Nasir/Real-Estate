# -*- coding: utf-8 -*-


from odoo import models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    # def action_do_something(self):
    #     print("Property is sold")
    #     self.env['account.move'].create(
    #         {
    #             'move_type' : 'out_invoice',
    #             'partner_id' : self.buyer_id.id,
    #             'invoice_line_ids' : [
    #                 (0,
    #                  0,
    #                     {
    #                         "name" :self.name,
    #                         "quantity" : 1,
    #                         "price_unit" : self.selling_price * 6/100,
    #                     },
    #                 ),
    #                 (0,
    #                  0,
    #                     {
    #                         "name" : "administrative fees",
    #                         "quantity" : 1,
    #                         "price_unit" : 100.00,
    #                     },
    #                 )],
    #         }
    #     )
    #     return super().action_do_something()
           



    def action_do_something(self):
        print("Property is sold")
        self.env['account.move'].create(
            {
                'move_type' : 'out_invoice',
                'partner_id' : self.buyer_id.id,
                'invoice_line_ids' : [
                   Command.create (
                     
                        {
                            "name" :self.name,
                            "quantity" : 1,
                            "price_unit" : self.selling_price * 0.06,
                        },
                    ),
                    Command.create(
                        {
                            "name" : "administrative fees",
                            "quantity" : 1,
                            "price_unit" : 100.00,
                        },
                    )],
            }
        )
        return super().action_do_something()