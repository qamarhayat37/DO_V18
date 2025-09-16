from odoo import models, fields

class StockPickingProductScanLine(models.TransientModel):
    _name = "stock.picking.product.scan.line"
    _description = "Stock Picking Product Scan Line"

    product_barcode_scann_id = fields.Many2one("stock.picking.product.scan", string="Products Scan", copy=False,
                                               required=True)
    product_id = fields.Many2one('product.product', string='Products', ondelete='restrict', required=True)
    product_qty = fields.Float(string='Scanned Qty', digits='Product Unit of Measure', required=True, default=1.0)
    count = fields.Float(string='Current Count', digits='Product Unit of Measure', default=1.0)

