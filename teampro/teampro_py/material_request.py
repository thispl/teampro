import frappe
@frappe.whitelist()
def get_po_qty(item_code, company):
    po_qty = frappe.db.sql("""
        SELECT 
            COALESCE(SUM(poi.qty - poi.received_qty), 0) AS pending_qty
        FROM `tabPurchase Order Item` poi
        INNER JOIN `tabPurchase Order` po
            ON po.name = poi.parent
        WHERE poi.item_code = %s
        AND po.company = %s
        AND po.docstatus = 1
        AND po.status NOT IN ('Closed', 'Completed', 'Cancelled')
    """, (item_code, company), as_dict=True)

    return po_qty[0].pending_qty if po_qty else 0

@frappe.whitelist()
def merge_material_request_items(material_request):
    childtab = frappe.db.sql(""" select `tabMaterial Request Item`.item_code,`tabMaterial Request Item`.warehouse,
    `tabMaterial Request Item`.item_name,`tabMaterial Request Item`.conversion_factor,`tabMaterial Request Item`.custom_po_qty,
    sum(`tabMaterial Request Item`.qty) as qty, sum(`tabMaterial Request Item`.stock_qty) as stock_qty, `tabMaterial Request Item`.actual_qty as actual_stock_qty,
    `tabMaterial Request Item`.stock_uom,
    `tabMaterial Request Item`.uom,`tabMaterial Request Item`.warehouse,
    `tabMaterial Request Item`.from_warehouse,`tabMaterial Request Item`.stb
    from `tabMaterial Request`
    left join `tabMaterial Request Item` on `tabMaterial Request`.name = `tabMaterial Request Item`.parent where `tabMaterial Request`.name = '%s' group by `tabMaterial Request Item`.item_code order by `tabMaterial Request Item`.idx """%(material_request),as_dict = 1)
    return childtab

@frappe.whitelist()
def get_salesorder_qty(item,company):
    new_so = frappe.db.sql("""select sum(`tabSales Order Item`.qty *`tabSales Order Item`.conversion_factor) as qty,sum(`tabSales Order Item`.delivered_qty *`tabSales Order Item`.conversion_factor) as d_qty from `tabSales Order` left join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent where `tabSales Order Item`.item_code = '%s' and `tabSales Order`.docstatus = 1 and `tabSales Order`.company = '%s' and status != 'Closed' """ % (item,company), as_dict=True)[0]
    if not new_so['qty']:
        new_so['qty'] = 0
    if not new_so['d_qty']:
        new_so['d_qty'] = 0
    del_total = new_so['qty'] - new_so['d_qty']
    return del_total

