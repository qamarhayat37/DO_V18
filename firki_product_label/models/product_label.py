from odoo import models, fields

class ProductLabel(models.Model):
    _name = 'product.label'
    _description = 'Product Label'

    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Integer(default=1)

    def action_print_labels(self):
        return self.env.ref('firki_product_label.product_label_report').report_action(self)
