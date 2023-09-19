{
	'application': True,
	'name':'estate',
	'Website':'www.odoo.com',
	'summary':'welcome to odoo',
	 "depends": [
        "mail",
		"website",
    ],
	'category':'Real Estate/ Brokerage',
	
	'data':[
		'security/ir.model.access.csv',
		'security/security.xml',
		'demo/estate_property.xml',
		'wizard/wizard_views.xml',
		'views/estate_property_view.xml',
		'views/property_type.xml',
		'views/property_tags.xml',
		'views/estate_property_offers.xml',
		'views/res_users_views.xml',
		'views/web_templates.xml',
		'report/estate_property_reports.xml',
		'report/estate_property_templates.xml',
		
	],	
}
