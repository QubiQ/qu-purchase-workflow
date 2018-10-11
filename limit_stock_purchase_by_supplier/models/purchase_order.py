# Copyright 2018 valentin.vinagre@qubiq.es
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    @api.depends('partner_id', 'company_id')
    @api.onchange('partner_id', 'company_id')
    def update_seller_invoice_line(self):
        for sel in self:
            for order_line in self.order_line:
                order_line.sudo()._get_supplier_info()
