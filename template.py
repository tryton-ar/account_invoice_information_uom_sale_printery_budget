# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval, Bool, And
from trytond.pool import PoolMeta

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = "product.template"

    info_list_price = fields.Numeric('Information List Price', digits=(16, 8),
        states={'required': Bool(Eval('use_info_unit'))})

    @fields.depends('use_info_unit', 'info_price', 'info_ratio', 'default_uom',
        'info_list_price')
    def on_change_info_ratio(self, name=None):
        return {
            'list_price': self.get_unit_price(self.info_list_price)
            }

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls.info_ratio.states['readonly'] = Eval('product_type_printery', 'otros') == 'papel',
        cls.list_price.states['readonly'] = And(Eval('product_type_printery', 'otros') == 'papel', Bool(Eval('use_info_unit')))

    @fields.depends('width', 'height', 'weight', 'product_type_printery')
    def on_change_with_info_ratio(self, name=None):
        # The values are set at cm and gr.
        if self.height and self.width and self.weight and self.product_type_printery == 'papel':
            height = self.height / 100
            width = self.width / 100
            return round(float(width * height * self.weight / 1000), 4)
        else:
            return float(1.0)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        for templates, values in zip(actions, actions):
            for template in templates:
                if template.product_type_printery == 'papel' and 'info_ratio' in values:
                    template.info_ratio = values['info_ratio']
                    if 'info_list_price' in values:
                        template.info_list_price = values['info_list_price']

                    values['list_price'] = template.get_unit_price(template.info_list_price)

        super(Template, cls).write(*args)
