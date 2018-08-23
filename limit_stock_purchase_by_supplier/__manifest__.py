# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

{
    'name': 'Limit Stock Purchase By Supplier',
    'summary': 'Limit stock purchase',
    'version': '11.0.1.0.0',
    'author': 'QubiQ, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.qubiq.es',
    'depends': [
        'purchase',
        'stock',
        'product',
    ],
    'data': [
        'views/product_supplierinfo.xml',
    ],
    'category': 'Purchase',
    'installable': True,
    'application': False,
}
