# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Analytic Account",
    "summary": "Purchase Analytic Account",
    "version": "13.0.1.0.0",
    "category": "Pro",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'purchase',
        'account'
    ],
    "data": [
        'views/purchase_order.xml'
    ],
}
