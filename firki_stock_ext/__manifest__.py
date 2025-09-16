# -*- coding: utf-8 -*-
{
    "name": "Stock Scan one by one",
    "version": "1.0",
    "category": "Stock",
    "depends": ['base','stock'],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_views.xml",
        "wizard/stock_picking_product_scan.xml"
    ],
    "installable": True,
    "application": False
}
