from odoo import models, fields
import base64
import csv
import io

class UploadSKUWizard(models.TransientModel):
    _name = 'upload.sku.wizard'
    _description = 'Upload SKU and Qty Wizard'

    file = fields.Binary("CSV File", required=True)
    filename = fields.Char("Filename")

    def action_process_file(self):
        data = base64.b64decode(self.file)
        file_io = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(file_io)
        label_model = self.env['product.label']
        for row in reader:
            sku = row.get('SKU')
            qty = int(row.get('Qty', 0))
            product = self.env['product.product'].search([('default_code', '=', sku)], limit=1)
            if product:
                label_model.create({
                    'product_id': product.id,
                    'quantity': qty,
                })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.label',
            'view_mode': 'list,form',
            'target': 'current',
        }
