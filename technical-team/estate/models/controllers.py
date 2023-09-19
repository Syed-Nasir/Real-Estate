# -*- coding: utf-8 -*-
from odoo import http

class Estate(http.Controller):

    @http.route('/estate/estate/', auth='public', website = True)
    def index(self, **kw):
        Teachers = http.request.env['academy.teachers']
        return http.request.render('estate.index', {
             'teachers': Teachers.search([])
         })
