# -*- coding: utf-8 -*-
{
    "name": "Product Label Generator",
    "version": "1.0",
    "category": "Inventory",
    "depends": ['base', 'product', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_label_views.xml",
        "views/upload_wizard_views.xml",
        "views/product_label_report.xml",
    ],
    "installable": True,
    "application": False
}
