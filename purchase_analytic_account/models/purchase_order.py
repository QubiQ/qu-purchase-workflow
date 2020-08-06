# Copyright 2020 Jesus Ramoneda <jesus.ramoneda@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_account_move_line(self, move):
        res = super()._prepare_account_move_line(move)
        res['analytic_account_id'] = self.order_id.analytic_account_id
        return res
