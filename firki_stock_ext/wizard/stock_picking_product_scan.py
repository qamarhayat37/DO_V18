from odoo import models, fields, _
from odoo.exceptions import ValidationError

class StockPickingProductScan(models.TransientModel):
    _name = "stock.picking.product.scan"
    _inherit = ["barcodes.barcode_events_mixin"]
    _description = "Stock Picking Product Scan"

    product_barcode_line_ids = fields.One2many("stock.picking.product.scan.line", 'product_barcode_scann_id',
                                               string="Line")
    def on_barcode_scanned(self, barcode):
        """
            this method is handle the on-screen barcode scanning process.
            based on scanned barcode find product and then if already there in wizard then
            increase qty of product else it will add new product in wizard line.
        """
        context = dict(self._context)
        product_product_obj = self.env['product.product']
        # Find product by barcode or internal reference
        product = barcode and product_product_obj.search(
            ['|', ('barcode', '=', barcode), ('default_code', '=', barcode)], limit=1)
        if not product:
            return {'warning': {
                                'title': _('Warning'),
                                'message': _('Scanned product not found.')}}


        # Get active picking
        picking = self.env['stock.picking'].browse(context.get('active_picking_id'))
        if not picking:
            return {'warning': {'title': _('Warning'),
                                'message': _('No active picking found.')}}
        stock_moves = picking.move_ids.filtered(lambda p: p.product_id and p.product_id.id == product.id)
        if not stock_moves:
            return {'warning': {'title': _('Warning'),
                                'message': _('Scanned product is not found in the current picking.')}}
        ordered_qty = sum(stock_moves.mapped('quantity'))
        scanned_qty = sum(stock_moves.mapped('scanned_qty'))
        #product_barcode_line is a recordset of lines in the barcode scanning wizard.
        product_barcode_line = self.product_barcode_line_ids.filtered(
            lambda p: p.product_id and p.product_id.id == product.id)
        if product_barcode_line:
            last_line = product_barcode_line[-1]
            if ordered_qty > last_line.product_qty:
                # Gets the current scanned quantity.
                line_qty = last_line.product_qty
                # Increments scanned quantity by one (one more scan happened).
                qty = line_qty + 1
                # Updates the scanned quantity field with the new value.
                last_line.product_qty = qty
                count = last_line.count
                last_line.count = count + 1
            else:
                return {'warning': {
                                     'title': _('Warning'),
                                     'message': _('You cannot scan more quantity then Ordered Quantity.')}}
        else:
            if ordered_qty > scanned_qty:
                new_line = self.product_barcode_line_ids.new({
                    'product_id': product.id,
                    'product_qty': scanned_qty + 1,
                    'count': 1,
                })
                self.product_barcode_line_ids = new_line + self.product_barcode_line_ids
            else:
                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('You cannot scan more quantity then Ordered Quantity.')}}


    def import_scanned_products(self):
        picking_id = self.env.context.get('active_picking_id')
        picking = self.env['stock.picking'].browse(picking_id)

        if picking.move_ids:
            stock_moves = picking.move_ids
            for barcode_scan_line in self.product_barcode_line_ids:
                scan_qty = barcode_scan_line.product_qty
                lines = stock_moves.filtered(
                    lambda p: p.product_id.id == barcode_scan_line.product_id.id
                )
                for line in lines:
                    line.scanned_qty = scan_qty
                    break




