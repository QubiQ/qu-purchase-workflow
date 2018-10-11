# Copyright 2018 valentin.vinagre@qubiq.es
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, fields, api, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier = fields.Many2one(
        'product.supplierinfo',
        string="Supplier Info",
        compute="_get_supplier_info",
        store=True,
        readonly=True,
    )

    limit_purchase_bool = fields.Boolean(
        string="Limit Purchase",
        compute="_get_supplier_info",
        store=True,
        readonly=True,
    )

    @api.multi
    def action_quota_view(self):
        self.ensure_one()
        if not self.product_id:
            return
        self._get_supplier_info()
        if self.supplier:
            view = self.env.ref('limit_stock_purchase_by_supplier.' +
                                'purchase_order_line_supplierinfo_form_view')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.supplierinfo',
                'res_id': self.supplier.id,
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'view_mode': 'form',
                'target': 'new',
            }

    @api.multi
    @api.depends('product_id', 'company_id', 'partner_id')
    @api.onchange('product_id', 'company_id', 'partner_id')
    def _get_supplier_info(self):
        for sel in self:
            if not sel.product_id:
                sel.supplier = False
                sel.limit_purchase_bool = False
                continue
            supplier = False
            limit_purchase_bool = False
            supplier = sel.product_id._select_seller(
                partner_id=sel.partner_id,
                quantity=sel.product_qty,
                date=sel.order_id.date_order and
                sel.order_id.date_order[:10],
                uom_id=sel.product_uom)
            if supplier:
                sel.supplier = supplier
                limit_purchase_bool = supplier.limit_purchase_bool
            sel.limit_purchase_bool = limit_purchase_bool
        return

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
