from odoo import models, fields, _
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def scan_products_one_by_one(self):
        """
        Opens a wizard for scanning products one by one.
        """
        self.ensure_one()
        form_view_id = self.env.ref('firki_stock_ext.view_stock_picking_product_scan', raise_if_not_found=False)
        ctx = dict(self.env.context or {})
        ctx.update({'active_picking_id': self.id})

        return {
            'name': _('Receive One by One Via Scanning'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.product.scan',
            'view_mode': 'form',
            'views': [(form_view_id.id, 'form')],
            'target': 'new',
            'context': ctx,
        }

class StockMove(models.Model):
    _inherit = 'stock.move'

    scanned_qty = fields.Float(string='Scanned Qty', digits='Product Unit of Measure', copy=False)




