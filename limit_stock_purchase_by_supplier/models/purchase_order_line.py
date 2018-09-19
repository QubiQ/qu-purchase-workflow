# Copyright 2018 valentin.vinagre@qubiq.es
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, api, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id', 'product_qty', 'product_uom')
    def check_quantity_seller(self):
        if not self.product_id:
            return
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)
        res = {}
        if seller and seller.limit_purchase_bool and \
           seller.limit_purchase_purchase_line_warn != 'none' and \
           seller.limit_purchase_actual + self.product_qty >=\
           seller.limit_purchase_quantity:
            title = _("Warning for %s") % self.product_id.name
            message = _(
                "The quantity exceeded the maximum"
                " for the supplier.\n The consumed quantity: %s from %s" % (
                    seller.limit_purchase_actual,
                    seller.limit_purchase_quantity)
            )
            warning = {
                'title': title,
                'message': message
                }
            res = {'warning': warning}
            if seller.limit_purchase_purchase_line_warn == 'block':
                self.product_id = False
        return res
