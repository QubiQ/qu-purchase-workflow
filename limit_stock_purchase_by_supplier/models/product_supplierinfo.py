# Copyright 2018 valentin.vinagre@qubiq.es
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models, api, fields, _
from odoo.addons import decimal_precision as dp
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import bisect
import calendar


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    limit_purchase_bool = fields.Boolean(
        string=_('Limit Purchase'),
        default=False
    )
    limit_purchase_range = fields.Selection([
        ('month', 'Monthly'),
        ('quarter', 'Quarterly'),
        ('anual', 'Annually'),
        ('custom', 'Custom')
        ], default='month',
        string=_('Date Range Limit'),
        help=_('* Monthly: from the first day of the current month until the'
               ' last day of the current month.\n * Quarterly: from the first'
               'day of the current quarter until the last day of the'
               'current quarter. Quarters are defined like 01/01/YYYY - '
               '31/03/YYYY, etc.\n * Annually: From the first day of the year'
               'until the last day of the current year.\n'
               '* Custom: Custom range.')
    )
    limit_purchase_quantity = fields.Float(
        string=_('Quantity Limit'),
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0
    )
    limit_purchase_actual = fields.Float(
        string=_('Quantity actual'),
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_get_limit_purchase_actual',
        compute_sudo=True,
    )
    limit_purchase_purchase_line_warn = fields.Selection([
            ('none', _('None')),
            ('warm', _('Warning')),
            ('block', _('Blocking'))
        ], string=_("Warning In Lines"),
        default='warm'
    )
    date_range_init = fields.Date(
        string=_('Date from'),
        default=fields.datetime.now().date()
    )
    date_range_end = fields.Date(
        string=_('Date to'),
        default=fields.datetime.now().date()+timedelta(days=30)
    )

    @api.multi
    @api.depends('limit_purchase_bool', 'limit_purchase_range')
    def _get_limit_purchase_actual(self):
        dates_range = {
            'month': {},
            'quarter': {},
            'anual': {},
        }
        today = fields.datetime.now().date()
        # Month
        dates_range['month']['init'] =\
            datetime.combine(
                date(today.year, today.month, 1),
                datetime.min.time()
            )
        dates_range['month']['end'] =\
            datetime.combine(
                date(
                    today.year,
                    today.month,
                    calendar.monthrange(today.year, today.month)[1]
                ),
                datetime.max.time()
            )
        # Quarter
        qbegins = [date(today.year, month, 1) for month in (1, 4, 7, 10)]
        idx = bisect.bisect(qbegins, today)
        dates_range['quarter']['init'] =\
            datetime.combine(
                qbegins[idx-1],
                datetime.min.time()
            )
        dates_range['quarter']['end'] =\
            datetime.combine(
                qbegins[idx-1] + relativedelta(months=3) - timedelta(days=1),
                datetime.max.time()
            )
        # Anual
        dates_range['anual']['init'] =\
            datetime.combine(
                date(today.year, 1, 1),
                datetime.min.time()
            )
        dates_range['anual']['end'] =\
            datetime.combine(
                date(today.year, 12, 31),
                datetime.max.time()
            )
        for sel in self.filtered(lambda x: x.limit_purchase_bool):
            if sel.limit_purchase_range != 'custom':
                date_init = dates_range[sel.limit_purchase_range]['init']
                date_end = dates_range[sel.limit_purchase_range]['end']
            else:
                date_init = fields.Date.from_string(
                    sel.date_range_init)
                date_end = fields.Date.from_string(
                    sel.date_range_end)
            domain = [
                ('partner_id', 'child_of', sel.name.id),
                ('state', 'in', ('open', 'paid')),
                ('date_invoice', '>=', fields.Date.to_string(date_init)),
                ('date_invoice', '<=', fields.Date.to_string(date_end))
            ]
            if sel.company_id:
                domain.append(
                    ('company_id', '=', sel.company_id.id)
                )
            in_invoice_lines = self.env['account.invoice'].search(
                    domain + [('type', '=', 'in_invoice')]
                ).mapped('invoice_line_ids')
            out_invoice_lines = self.env['account.invoice'].search(
                    domain + [('type', '=', 'in_refund')]
                ).mapped('invoice_line_ids')
            in_qty_total = 0.0
            out_qty_total = 0.0
            if sel.product_id:  # Variants
                in_qty_total =\
                    sum(in_invoice_lines.filtered(
                        lambda x: x.product_id.id == sel.product_id.id
                    ).mapped('quantity'))
                out_qty_total =\
                    sum(out_invoice_lines.filtered(
                        lambda x: x.product_id.id == sel.product_id.id
                    ).mapped('quantity'))
            else:  # Template
                in_qty_total =\
                    sum(in_invoice_lines.filtered(
                        lambda x: x.product_id.product_tmpl_id.id ==
                        sel.product_tmpl_id.id
                    ).mapped('quantity'))
                out_qty_total =\
                    sum(out_invoice_lines.filtered(
                        lambda x: x.product_id.product_tmpl_id.id ==
                        sel.product_tmpl_id.id
                    ).mapped('quantity'))
            sel.limit_purchase_actual = in_qty_total - out_qty_total
