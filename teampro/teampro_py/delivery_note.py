import frappe
from frappe.utils import formatdate, format_time
from frappe.utils.pdf import get_pdf
import base64

@frappe.whitelist()
def print_delivery_label(parent, child, sticker_type="box"):
    """
    Unified sticker generator with tailored layout scaling per print variant button.
    sticker_type inputs: 'box', 'cover', 'material'
    """
    parent_doc = frappe.get_doc("Delivery Note", parent)
    row = frappe.get_doc("Delivery Note Item", child)

    # Only loop multiple times for the Box Sticker layout. 
    # Cover and Material layouts will only print 1 copy.
    if sticker_type == "box":
        total_box = int(row.custom_box or 1)
        if total_box <= 0:
            total_box = 1
    else:
        total_box = 1

    doc_name = parent_doc.name or ""
    item_name = row.item_name or ""
    wrd_rate = row.custom_wrd_rate or ""
    sales_order = parent_doc.sales_order or ""
    
    # Fetching directly from your Tamil field in Item Master
    item_tamil_name = ""
    if row.item_code:
        item_tamil_name = frappe.db.get_value("Item", row.item_code, "custom_item_name_tamil_") or ""

    # Fetching actual item names from item codes for packaging items with safety fallback
    pp_name = ""
    if hasattr(row, "custom_cover_type") and row.custom_cover_type:
        pp_name = frappe.db.get_value("Item", row.custom_cover_type, "item_name") or row.custom_cover_type

    sp_name = ""
    if hasattr(row, "custom_packing_type") and row.custom_packing_type:
        sp_name = frappe.db.get_value("Item", row.custom_packing_type, "item_name") or row.custom_packing_type

    tp_name = ""
    if hasattr(row, "custom_tertiary_packingbox") and row.custom_tertiary_packingbox:
        tp_name = frappe.db.get_value("Item", row.custom_tertiary_packingbox, "item_name") or row.custom_tertiary_packingbox

    # Fetching names for the custom fields safely
    print_cover_name = ""
    if hasattr(row, "custom_print_cover") and row.custom_print_cover:
        print_cover_name = frappe.db.get_value("Item", row.custom_print_cover, "item_name") or row.custom_print_cover

    print_mat_name = ""
    if hasattr(row, "custom_print_material") and row.custom_print_material:
        print_mat_name = frappe.db.get_value("Item", row.custom_print_material, "item_name") or row.custom_print_material

    # Dynamic Header Banner Title matching
    title_lookup = {
        "box": "BOX STICKER",
        "cover": "COVER STICKER",
        "material": "MATERIAL STICKER"
    }
    main_title = title_lookup.get(sticker_type, "MATERIAL STICKER")

    # DYNAMIC SIZING ENGINE DEFAULT RULES DECLARATION
    box_title_fontsize = "13px"
    box_counter_fontsize = "22px"
    box_panel_padding = "4px"
    wdr_row_style = ""
    pp_row_style = ""
    pp_text_style = ""
    item_eng_size = "20px"  
    item_tam_size = "18px"  
    qty_spec_size = "16px"  
    
    # Defaults for Box & Cover stickers
    box_hero_margin = "2px auto 4px auto"
    footer_padding_style = "margin-top: 10px;" 
    footer_label_padding = "2px 0;"
    content_push_style = ""
    pp_push_style = "" 
    
    # Border overrides based on context
    box_hero_border = "none"
    identity_border = "none"
    cover_merged_border = "none"  

    # 1. Custom Sizing Rules for the 'custom_print' (BOX Layout variant)
    if sticker_type == "box":
        box_panel_padding = "10px"          
        box_title_fontsize = "32px"        
        box_counter_fontsize = "78px"      
        item_eng_size = "16px"            
        item_tam_size = "14px"            
        box_hero_border = "1px dotted #000" 
        footer_padding_style = "margin-top: 15px;" 

    # 2. Custom Sizing Rules for the 'custom_print_cover' (COVER Layout variant)
    elif sticker_type == "cover":
        cover_merged_border = "1px dotted #000; padding: 6px; margin-top: 6px;"
        wdr_row_style = "font-size: 40px !important; font-weight: bold !important; padding: 2px 0;"
        pp_row_style = "font-size: 30px !important; font-weight: bold !important; border: none !important; padding: 2px 0; margin-top: 2px; line-height: 1.1;"
        pp_text_style = "font-size: 30px !important; font-weight: 900 !important; text-transform: uppercase;" 
        item_eng_size = "18px"
        item_tam_size = "16px"
        box_panel_padding = "4px"
        box_title_fontsize = "22px"
        box_counter_fontsize = "24px"
        footer_padding_style = "margin-top: 10px;" 

    # 3. Custom Sizing Rules SPECIFICALLY for the MATERIAL variant
    elif sticker_type == "material":
        item_eng_size = "42px"            
        item_tam_size = "38px"            
        qty_spec_size = "26px"            
        box_panel_padding = "4px"
        box_title_fontsize = "22px"
        box_counter_fontsize = "24px"
        identity_border = "1px dotted #000" 
        
        # Match Box Sticker style (no custom overrides)
        pp_row_style = ""
        pp_text_style = ""
        
        footer_label_padding = "0px 0;"
        
        # 1. Moves the WRD block down from the identity area
        content_push_style = "margin-top: 8px;"
        
        # 2. Moves the PP block down from the WRD block line
        pp_push_style = "margin-top: 6px;"
        
        # 3. Moves the BOX block down slightly
        box_hero_margin = "6px auto 2px auto"  
        
        # 4. ADDED PUSH VALUE ISOLATED HERE: Shifts the Footer (Scan, TP, SP) down from the BOX block line
        footer_padding_style = "margin-top: 10px;" 

    html = f"""
<html>
<head>
<style>
    * {{
        box-sizing: border-box;
    }}
    @page {{ 
        size: A6 portrait; 
        margin: 4mm; 
    }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 11px;
        color: #000;
        margin: 0;
        padding: 0;
        background-color: #fff;
    }}
    .page-wrapper {{
        page-break-inside: avoid;
        page-break-after: always;
        width: 100%;
    }}
    .page-wrapper:last-child {{
        page-break-after: avoid !important;
    }}
    .label {{
        border: none;
        padding: 0;
        box-sizing: border-box;
        width: 100%;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    
    .sticker-main-title {{
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        text-align: center;
        letter-spacing: 1px;
        padding-bottom: 4px;
    }}
    
    .meta-table {{
        margin-top: 2px;
    }}
    .meta-table td {{
        font-size: 9px;
        padding-bottom: 3px;
        border-bottom: 1px solid #000;
        vertical-align: top;
    }}
    
    .customer-block {{
        font-size: 11px;
        padding-top: 4px;
        padding-bottom: 4px; 
        word-wrap: break-word;
    }}
    
    .identity-container {{
        text-align: center;
        margin-bottom: 4px; 
        border: {identity_border};
        padding: 4px;
    }}
    .item-tamil {{
        font-size: {item_tam_size}; 
        color: #000;
        font-weight: normal;
        margin-bottom: 2px;
    }}
    .item-english {{
        font-size: {item_eng_size};
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 2px;
    }}
    .qty-spec {{
        font-size: {qty_spec_size}; 
        font-weight: bold;
        color: #000;
    }}
    
    .cover-merged-container {{
        border: {cover_merged_border};
        {content_push_style}
    }}
    
    .wdr-full-line {{
        width: 100%;
        padding: 4px 0;
        font-size: 12px;
        font-weight: bold;
        border-bottom: 1px solid #000; 
        {wdr_row_style}
    }}
    .wdr-full-line table td {{
        width: 33.33%;
    }}

    .pp-section-row {{
        font-size: 11px;
        padding: 4px 0;
        font-weight: bold;
        color: #000;
        {pp_row_style}
        {pp_push_style}
    }}
    
    .pp-highlight-text {{
        {pp_text_style}
    }}

    .center-box-hero {{
        text-align: center;
        border: {box_hero_border}; 
        padding: {box_panel_padding}; 
        margin: {box_hero_margin}; 
        width: 100%;
    }}
    .box-title-text {{
        font-size: {box_title_fontsize};
        font-weight: bold;
        text-transform: uppercase;
        display: block;
        margin-bottom: 1px;
    }}
    .box-counter-large {{
        font-size: {box_counter_fontsize}; 
        font-weight: bold;
        color: #000;
        text-transform: uppercase;
        line-height: 1;
    }}
    
    .footer-wrapper-div {{
        width: 100%;
    }}
    .footer-layout-table {{
        width: 100%;
    }}
    .footer-layout-table td {{
        vertical-align: middle;
    }}
    .footer-labels td {{
        padding: {footer_label_padding};
        font-size: 11px;
    }}
    .sp-unbold-text {{
        font-weight: normal !important;
        font-style: normal !important;
    }}
    .so-title-block {{
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 2px;
        text-align: center;
    }}
    .so-qr-code {{
        width: 65px; 
        height: 65px;
        display: block;
        margin: 0 auto;
    }}
</style>
</head>
<body>
"""
    for i in range(1, total_box + 1):
        packed_date = formatdate(parent_doc.custom_packing_on, "dd-MM-yyyy") if parent_doc.custom_packing_on else ""
        packed_time = str(parent_doc.posting_time).split('.')[0] if parent_doc.posting_time else ""
        customer_name = parent_doc.customer or ""
        mfg_date = formatdate(row.custom_mfg_on, "dd-MM-yyyy") if row.custom_mfg_on else ""
        ref_no = formatdate(parent_doc.custom_delivery_date, "yyMMdd") if parent_doc.custom_delivery_date else ""

        qty_covers = int(row.custom_covers or 0)
        primary_uom = row.custom_primary_uom or "Nos"
        wrd_uom = row.custom_wrd_uom or ""
        qty_string = f"{qty_covers} {primary_uom} / {wrd_uom}"
        
        # Calculate final values to test if they exist
        final_pp_value = pp_name or print_cover_name or ""
        final_sp_value = sp_name or print_mat_name or ""
        final_tp_value = tp_name or ""
        
        # Format HTML rows cleanly based on text availability
        pp_html_row = ""
        if final_pp_value:
            pp_html_row = f"""
            <div class="pp-section-row">
                <b>PP:</b> {final_pp_value} <span class="pp-highlight-text">{qty_covers} COVERS</span>
            </div>
            """
            
        sp_html_row = ""
        if final_sp_value:
            sp_html_row = f"""
            <tr>
                <td style="font-weight: normal !important;">
                    <b>SP:</b> <span class="sp-unbold-text" style="font-weight: normal !important;">{final_sp_value}</span>
                </td>
            </tr>
            """
            
        tp_html_row = ""
        if final_tp_value:
            tp_html_row = f"""<tr><td style="padding-top: 1px;"><b>TP:</b> {final_tp_value}</td></tr>"""

        sp_style = "font-weight: normal !important;"

        html += f"""
<div class="page-wrapper">
    <div class="label">
        <div class="sticker-main-title">{main_title}</div>

        <table class="meta-table">
            <tr>
                <td style="width: 35%;"><b>Packed:</b> {packed_date}</td>
                <td style="width: 30%; text-align: center;"><b>Time:</b> {packed_time}</td>
                <td style="width: 35%; text-align: right;"><b>Ref No:</b> {ref_no}</td>
            </tr>
        </table>

        <div class="customer-block">
            <b>Cust:</b> {customer_name}
        </div>

        <div class="identity-container">
            <div class="item-tamil">{item_tamil_name}</div>
            <div class="item-english">{item_name}</div>
            <div class="qty-spec">{qty_string}</div>
        </div>

        <div class="cover-merged-container">
            <div class="wdr-full-line" style="{'' if sticker_type == 'cover' else 'margin-top: 4px;'}">
                <table>
                    <tr>
                        <td><b>W:</b> {wrd_uom}</td>
                        <td style="text-align: center;"><b>R:</b> ₹ {wrd_rate}</td>
                        <td style="text-align: right;"><b>D:</b> {mfg_date}</td>
                    </tr>
                </table>
            </div>
            {pp_html_row}
        </div>

        <div class="center-box-hero">
            <span class="box-title-text">BOX</span>
            <span class="box-counter-large">{i}/{total_box if sticker_type == "box" else 1}</span>
        </div>
        
        <div class="footer-wrapper-div" style="{footer_padding_style}">
            <table class="footer-layout-table">
                <tr>
                    <td style="width: 60%; text-align: left;">
                        <table class="footer-labels">
                            {sp_html_row}
                            {tp_html_row}
                        </table>
                    </td>
                    <td style="width: 40%; text-align: center;">
                        <div class="so-title-block">{sales_order}</div>
                        <img class="so-qr-code" alt="SO QR" src="https://api.qrserver.com/v1/create-qr-code/?data={sales_order}&amp;size=100x100">
                    </td>
                </tr>
            </table>
        </div>
    </div>
</div>
"""
            
    html += "</body></html>"

    pdf = get_pdf(html, options={
        "page-size": "A6",
        "orientation": "Portrait",
        "margin-top": "4mm",
        "margin-bottom": "4mm",
        "margin-left": "4mm",
        "margin-right": "4mm"
    })

    return base64.b64encode(pdf).decode("utf-8")
