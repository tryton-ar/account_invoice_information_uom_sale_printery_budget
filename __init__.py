# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool
from . import template


def register():
    Pool.register(
        template.Template,
        module='account_invoice_information_uom_sale_printery_budget',
        type_='model')
