import frappe
from frappe.utils import formatdate, format_time, escape_html
from frappe.utils.pdf import get_pdf
import base64
import re

@frappe.whitelist()
def print_delivery_label(parent, child, sticker_type="box"):
    """
    Unified sticker generator with tailored layout scaling per print variant button.
    sticker_type inputs: 'box', 'cover', 'material'
    """
    # Determine the parent doctype dynamically based on parent name prefix or database lookup
    parent_doctype = "Delivery Note"
    child_doctype = "Delivery Note Item"
    if parent.startswith("SAL-ORD-") or (not frappe.db.exists("Delivery Note", parent) and frappe.db.exists("Sales Order", parent)):
        parent_doctype = "Sales Order"
        child_doctype = "Sales Order Item"

    parent_doc = frappe.get_doc(parent_doctype, parent)
    row = frappe.get_doc(child_doctype, child)

    boxes = int(row.custom_box or 0)
    bags = int(row.custom_bag or 0)
    if boxes == 0 and bags == 0:
        boxes = 1

    # Auto-switch to bag loop if sticker_type is "box" but custom_box is 0 and custom_bag is specified
    is_box_to_bag_fallback = False
    if sticker_type == "box" and not boxes and bags > 0:
        is_box_to_bag_fallback = True

    # Set loop count and variables based on sticker type and fallback
    if sticker_type == "box":
        total_box = max(boxes, bags)
        box_title = "BOX"
    else:
        total_box = 1
        box_title = "BOX"

    if total_box <= 0:
        total_box = 1

    doc_name = parent_doc.name or ""
    item_name = row.item_name or ""
    wrd_rate = row.custom_wrd_rate or ""
    
    if parent_doctype == "Sales Order":
        sales_order = parent_doc.name or ""
        delivery_date = parent_doc.delivery_date
        posting_time = None
    else:
        sales_order = parent_doc.sales_order or ""
        delivery_date = parent_doc.custom_delivery_date
        posting_time = parent_doc.posting_time
    
    # Fetching directly from your Tamil field in Item Master
    item_tamil_name = ""
    if row.item_code:
        item_tamil_name = frappe.db.get_value("Item", row.item_code, "custom_item_name_tamil_") or ""

    # Dynamic styling for Tamil item name to prevent layout overflow when it is long
    tamil_fontsize = "12px"
    tamil_line_height = "1.2"
    tamil_margin_bottom = "4px"
    if item_tamil_name:
        # Strip any HTML tags that might contain inline styles overriding our dynamic font size
        item_tamil_name = re.sub(r'<[^>]*>', '', item_tamil_name).strip()
        # Split on any common separator (periods, commas, semicolons, newlines, slashes, hyphens, bullets, or spaces)
        tamil_sentences = [s.strip() for s in re.split(r'[.!?\n,;/|•\s]', item_tamil_name) if s.strip()]
        num_sentences = len(tamil_sentences)
        length = len(item_tamil_name)

        if num_sentences >= 3 or length > 30:
            tamil_fontsize = "9.2px"
            tamil_line_height = "1.0"
            tamil_margin_bottom = "1px"
        elif num_sentences == 2 or length > 18:
            tamil_fontsize = "9.5px"
            tamil_line_height = "1.05"
            tamil_margin_bottom = "2px"
        elif length > 12:
            tamil_fontsize = "9.5px"
            tamil_line_height = "1.1"
            tamil_margin_bottom = "2.5px"

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
        "box": "BOX & BAG",
        "cover": "CS",
        "material": "MS"
    }
    main_title = title_lookup.get(sticker_type, "MS")
    if is_box_to_bag_fallback:
        main_title = "BOX & BAG"

    dot_html = ""
    if not is_box_to_bag_fallback:
        if sticker_type == "cover":
            dot_html = '<span class="dot-box">●</span><span class="dot-box">●</span>'
        elif sticker_type == "material":
            dot_html = '<span class="dot-box">●</span>'
    box_title_fontsize = "12px"
    box_counter_fontsize = "22.5px"
    box_qty_fontsize = "19.5px"
    box_panel_padding = "1px"
    wrd_row_style = "font-size: 12px; line-height: 1.45;"
    pp_row_style = ""
    pp_text_style = ""
    item_eng_size = "12px"  
    item_tam_size = "12px"  
    qty_spec_size = "10px"  
    item_col_width = "60%"
    box_col_width = "40%"
    pp_font_size = "12px"
    pp_font_weight = "bold"
    
    # Defaults for Box & Cover stickers
    box_hero_margin = "1px auto"
    footer_padding_style = "margin-top: 1px;" 
    footer_label_padding = "1px 0;"
    content_push_style = ""
    pp_push_style = "" 
    covers_text_style = "font-size: 10px; font-weight: bold; text-transform: uppercase; display: block; margin-top: 1px;" 
    
    # Border overrides based on context
    box_hero_border = "none"
    identity_border = "none"
    cover_merged_border = "none"  

    # 1. Custom Sizing Rules for the 'custom_print' (BOX Layout variant)
    if sticker_type == "box":
        box_panel_padding = "1px"          
        box_title_fontsize = "12px"        
        box_counter_fontsize = "44px"      
        box_qty_fontsize = "30px"
        covers_text_style = "font-size: 13px; font-weight: bold; text-transform: uppercase; display: block; margin-top: 2px;"
        item_eng_size = "11px"            
        item_tam_size = "12px"            
        qty_spec_size = "9px"
        item_col_width = "55%"
        box_col_width = "45%"
        box_hero_border = "none" 
        footer_padding_style = "margin-top: 1px;" 
        wrd_row_style = "font-size: 11px; line-height: 1.3;" 

    # 2. Custom Sizing Rules for the 'custom_print_cover' (COVER Layout variant)
    elif sticker_type == "cover":
        cover_merged_border = "none"
        wrd_row_style = "font-size: 13px; font-weight: bold;"
        pp_font_size = "13px"
        pp_font_weight = "bold"
        covers_text_style = "font-size: 9px !important; font-weight: bold !important; text-transform: uppercase; display: block; margin-top: 1px;"
        item_eng_size = "11px"
        item_tam_size = "15px"
        box_panel_padding = "1px"
        box_title_fontsize = "11px"
        box_counter_fontsize = "18px"
        footer_padding_style = "margin-top: 1px;" 

    # 3. Custom Sizing Rules SPECIFICALLY for the MATERIAL variant
    elif sticker_type == "material":
        item_eng_size = "18px"            
        item_tam_size = "15px"            
        qty_spec_size = "11px"            
        box_panel_padding = "1px"
        box_title_fontsize = "11px"
        box_counter_fontsize = "18px"
        identity_border = "none" 
        
        # Match Box Sticker style (no custom overrides)
        pp_row_style = ""
        pp_text_style = ""
        
        footer_label_padding = "0px 0;"
        
        # Moves elements/margins slightly to adjust spacing
        content_push_style = "margin-top: 1px;"
        pp_push_style = "margin-top: 1px;"
        box_hero_margin = "1px auto"  
        footer_padding_style = "margin-top: 1px;" 

    html = f"""
<html>
<head>
<style>
    .print-format {{
        margin-top: 0mm;
        margin-bottom: 0mm;
        margin-left: 0mm;
        margin-right: 0mm;
    }}
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    @page {{
        size: 4in 2in;
        margin: 0;
    }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 9.5px;
        color: #000;
        background-color: #fff;
        padding: 0;
        margin: 0;
    }}
    .page-wrapper {{
        page-break-inside: avoid;
        width: 100%;
    }}
    .label {{
        width: 100%;
        position: relative;
        height: 1.90in;
        overflow: hidden;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        page-break-inside: avoid !important;
    }}
    tr, td {{
        page-break-inside: avoid !important;
    }}
    .header-layout-table {{
        width: 100%;
        border-bottom: none;
        padding-bottom: 1px;
        margin-bottom: 1px;
        margin-top: 1px;
    }}
    .header-layout-table td {{
        font-size: 8.5px;
        vertical-align: middle;
        line-height: 1.1;
    }}
    .sticker-main-title {{
        font-size: 8.5px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        vertical-align: middle;
    }}
    .striped-icon {{
        display: inline-block;
        width: 13px;
        height: 13px;
        background: -webkit-repeating-linear-gradient(-45deg, #000, #000 1.5px, #fff 1.5px, #fff 3px);
        background: repeating-linear-gradient(-45deg, #000, #000 1.5px, #fff 1.5px, #fff 3px);
        border: 1px solid #000;
        margin-right: 5px;
        vertical-align: middle;
    }}
    .black-box {{
        display: inline-block;
        width: 13px;
        height: 13px;
        background-color: #000;
        border: 1px solid #000;
        margin-right: 5px;
        vertical-align: middle;
    }}

    .dot-box {{
        display: inline-block;
        width: 11px;
        height: 11px;
        background-color: #000;
        color: #fff;
        margin-left: 5px;
        vertical-align: middle;
        text-align: center;
        line-height: 10px;
        font-size: 8px;
    }}
    .middle-table {{
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
        border: 1px solid #000;
        margin-bottom: 2px;
    }}
    .item-column {{
        width: {item_col_width};
        vertical-align: top;
        padding-right: 4px;
        border-right: 1px solid #000;
    }}
    .item-label {{
        font-size: 7.5px;
        font-weight: bold;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1px;
    }}
    .item-tamil {{
        font-size: {item_tam_size}; 
        color: #000;
        font-weight: normal;
        margin-bottom: 1px;
        line-height: 1.1;
    }}
    .item-english {{
        font-size: {item_eng_size};
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 1px;
        line-height: 1.2;
    }}
    .qty-spec {{
        font-size: {qty_spec_size}; 
        font-weight: bold;
        color: #000;
        margin-top: 1px;
    }}
    .box-column {{
        width: {box_col_width};
        vertical-align: middle;
        text-align: center;
        padding-left: 4px;
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
        line-height: 1.0;
        display: block;
    }}
    .box-covers-text {{
        {covers_text_style}
    }}
    .bottom-table {{
        width: 100%;
        table-layout: fixed;
    }}
    .wrd-column {{
        width: 72%;
        vertical-align: top;
        font-size: 8.5px;
        line-height: 1.2;
    }}
    .qr-column {{
        width: 28%;
        vertical-align: middle;
        text-align: center;
    }}
    .dn-title-block {{
        font-size: 8px;
        font-weight: bold;
        margin-bottom: 1px;
        text-align: right;
    }}
    .dn-qrcode {{
        width: 32px; 
        height: 32px;
        display: inline-block;
        margin: 0;
        object-fit: contain;

    }}

</style>
</head>
<body>
"""
    for i in range(1, total_box + 1):
        page_break_style = "page-break-after: always;" if i < total_box else ""
        packed_date_clean = formatdate(delivery_date, "ddMMyyyy") if delivery_date else ""
        if posting_time:
            packed_time_clean = re.sub(r'[^0-9]', '', str(posting_time).split('.')[0])
            packed_id_val = f"{packed_date_clean}{packed_time_clean}"
        else:
            packed_id_val = f"{packed_date_clean}"
            
        customer_name = parent_doc.customer or ""
        mfg_date = formatdate(row.custom_mfg_on, "dd-MM-yyyy") if row.custom_mfg_on else ""
        ref_no = formatdate(delivery_date, "yyMMdd") if delivery_date else ""

        # Remove year (e.g. "-2026-") and add print count suffix
        dn_display = re.sub(r'^(SO\d{2}|.*?-20\d{2}-)', '', doc_name) + f"/{row.idx}" if doc_name else f"-{i}"
        batch = re.sub(r'^(SO\d{2}|.*?-20\d{2}-)', '', doc_name) if doc_name else ""

        # Resolve covers in last box/bag dynamically
        last_box_covers = getattr(row, "custom_last_box", None) or getattr(row, "custom_covers_in_last_box", None) or row.custom_covers or 0
        last_bag_covers = getattr(row, "custom_last_bag", None) or getattr(row, "custom_covers_in_last_bag", None) or row.custom_covers or 0

        # Dynamically set cover quantity per print page
        if sticker_type == "box":
            if int(row.custom_bag or 0) > 0:
                if i < total_box:
                    qty_covers = int(row.custom_per_2p or 0)
                else:
                    qty_covers = int(last_bag_covers)
            else:
                if i < total_box:
                    qty_covers = int(row.custom_per_3p or 0)
                else:
                    qty_covers = int(last_box_covers)
        else:
            qty_covers = int(row.custom_covers or 0)

        primary_uom = row.custom_primary_uom or "Nos"
        wrd_uom = row.custom_wrd_uom or ""
        stock_uom_qty = f"{row.stock_qty} {row.stock_uom}" if getattr(row, "stock_qty", None) and getattr(row, "stock_uom", None) else ""
        qty_string = f"{qty_covers} {primary_uom} / {wrd_uom} / {stock_uom_qty}"
        
        remarks = escape_html((row.custom_remarks or "").strip())

        # Calculate final values to test if they exist
        final_pp_value = pp_name or print_cover_name or ""
        final_sp_value = sp_name or print_mat_name or ""
        final_tp_value = tp_name or ""
        
        covers_html = ""
        if sticker_type == "box":
            covers_html = f'<span class="box-covers-text">{qty_covers} COVERS</span>'
            
        has_box_col = (boxes > 0)
        has_bag_col = (bags > 0)

        # Fallback if both are 0
        if not has_box_col and not has_bag_col:
            has_box_col = True

        display_boxes = boxes if boxes > 0 else 1
        display_bags = bags if bags > 0 else 1

        # Effective font sizes: smaller when remarks present so content fits reduced row heights
        if has_box_col or has_bag_col:
            if remarks:
                eff_counter_fontsize = "34px"
                eff_qty_fontsize = "26px"
            else:
                eff_counter_fontsize = "40px"
                eff_qty_fontsize = "30px"
        else:
            eff_counter_fontsize = box_counter_fontsize
            eff_qty_fontsize = box_qty_fontsize

        num_cols = (1 if has_box_col else 0) + (1 if has_bag_col else 0) + 1

        row1_cells = ""
        row2_cells = ""
        row3_cells = ""
        row4_cells = ""
        row5_cells = ""

        num_box_bag_cols = (1 if has_box_col else 0) + (1 if has_bag_col else 0)

        if sticker_type == "box" or is_box_to_bag_fallback:
            if has_box_col and has_bag_col:
                box_bag_col_width = "20%"
                item_col_width = "40%"
                qr_col_width = "23%"
            else:
                box_bag_col_width = "40%"
                item_col_width = "40%"
                qr_col_width = "23%"
        else:
            box_bag_col_width = "25%"
            qr_col_width = "23%"
            item_col_width = "55%"

        # Distinct box and bag quantities for the columns
        if i < display_boxes:
            box_qty = int(row.custom_per_3p or 0)
        else:
            box_qty = int(last_box_covers)

        bag_index = min(i, display_bags)
        if bag_index < display_bags:
            bag_qty = int(row.custom_per_2p or 0)
        else:
            bag_qty = int(last_bag_covers)

        if has_box_col:
            if i <= boxes:
                box_counter = f"{i if sticker_type == 'box' else 1}/{display_boxes}"
                box_qty_val = str(box_qty)
            else:
                box_counter = "NA"
                box_qty_val = "NA"
            row1_cells += f'<td style="width: {box_bag_col_width}; background-color: #000; color: #fff; padding: 2px 2px; font-weight: bold; font-size: {box_title_fontsize}; border-bottom: 1px solid #000; border-right: 1px solid #000; text-align: center; vertical-align: middle; height: 18px;">BOX</td>'
            row2_cells += f'<td style="padding: 2px 2px; vertical-align: middle; border-bottom: 1px solid #000; border-right: 1px solid #000; text-align: center;" class="box-counter-large"><span style="font-size: {eff_counter_fontsize}; font-weight: bold; color: #000;">{box_counter}</span><span style="font-size: 7px; font-weight: bold; color: #000;"> Nos</span></td>'
            row3_cells += f'<td style="padding: 2px 2px; vertical-align: middle; border-right: 1px solid #000; text-align: center;"><div style="font-size: 8px; font-weight: bold; color: #000; text-align: left;">C/Box</div><span style="font-size: {eff_qty_fontsize}; font-weight: bold; color: #000;">{box_qty_val}</span><span style="font-size: 7px; font-weight: bold; color: #000;"> Nos</span></td>'

        if has_bag_col:
            if i <= bags:
                bag_counter = f"{min(i, display_bags)}/{display_bags}"
                bag_qty_val = str(bag_qty)
            else:
                bag_counter = "NA"
                bag_qty_val = "NA"
            row1_cells += f'<td style="width: {box_bag_col_width}; background-color: #000; color: #fff; padding: 2px 2px; font-weight: bold; font-size: {box_title_fontsize}; border-bottom: 1px solid #000; border-right: 1px solid #000; text-align: center; vertical-align: middle; height: 18px;">BAG</td>'
            row2_cells += f'<td style="padding: 2px 2px; vertical-align: middle; border-bottom: 1px solid #000; border-right: 1px solid #000; text-align: center;" class="box-counter-large"><span style="font-size: {eff_counter_fontsize}; font-weight: bold; color: #000;">{bag_counter}</span><span style="font-size: 7px; font-weight: bold; color: #000;"> Nos</span></td>'
            row3_cells += f'<td style="padding: 2px 2px; vertical-align: middle; border-right: 1px solid #000; text-align: center;"><div style="font-size: 8px; font-weight: bold; color: #000; text-align: right;">C/Bag</div><span style="font-size: {eff_qty_fontsize}; font-weight: bold; color: #000;">{bag_qty_val}</span><span style="font-size: 7px; font-weight: bold; color: #000;"> Nos</span></td>'

        url_doctype = "sales-order" if parent_doctype == "Sales Order" else "delivery-note"
        qr_img_src = f"https://bwipjs-api.metafloor.com/?bcid=qrcode&amp;text=https%3A%2F%2Ferp.teamproit.com%2Fdesk%2F{url_doctype}%2F{doc_name}"
        del_date_val = formatdate(delivery_date, "dd.MM.yy") if delivery_date else ""

        # Keep table height at 135px. Remarks sit in a thin row under 1/1, above qty.
        table_total_height = 135
        if remarks:
            table_rowspan = "4"
            row2_height = 52
            row3_height = 49
            row4_height = 16
            row4_cells = (
                f'<td colspan="{num_box_bag_cols}" style="padding: 1px 3px; vertical-align: middle; '
                f'border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; '
                f'text-align: left; word-wrap: break-word; word-break: break-word; white-space: normal; overflow: hidden; '
                f'height: {row4_height}px; line-height: 1.1;">'
                f'<span style="font-size: 7px; font-weight: bold; color: #000;">Remarks: {remarks}</span></td>'
            )
        else:
            table_rowspan = "3"
            row2_height = 70
            row3_height = 39
            row4_height = 0
            row4_cells = ""

        # QR column cells - using rowspan nested table layout to customize rows
        row1_cells += f"""<td style="width: {qr_col_width}; vertical-align: top; padding: 0; border-left: 1px solid #000; height: {table_total_height}px;" rowspan="{table_rowspan}">
            <table style="width: 100%; height: {table_total_height}px; border-collapse: collapse; border: none; table-layout: fixed;">
                <tr style="height: 18px;">
                    <td style="background-color: #000; color: #fff; padding: 2px 2px; font-weight: bold; font-size: {box_title_fontsize}; border-bottom: 1px solid #000; text-align: center; vertical-align: middle; white-space: nowrap; height: 18px;">
                        {dn_display}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 0; vertical-align: middle; text-align: center; height: 86px;line-height: 0;">
                        <img src="{qr_img_src}" style="width: 80px; height: 80px; display: inline-block; vertical-align: middle; margin: 0;" alt="QR">
                    </td>
                </tr>
                <tr>
                    <td style="vertical-align: middle; font-size: 16px; font-weight: bold; color: #000; line-height: 1.0; text-align: center; white-space: nowrap; border-top: 1px solid #000; height: 18px;">
                        {del_date_val}
                    </td>
                </tr>
            </table>
        </td>"""
        
        header_row_height = 18
        # row1_cells += f"""<td style="width: {qr_col_width}; vertical-align: top; padding: 0; border-left: 1px solid #000; position: relative; height: {table_total_height}px;" rowspan="{table_rowspan}">
        # <table style="width: 100%; height: {table_total_height}px; border-collapse: collapse; border: none; table-layout: fixed;">
        #     <tr style="height: 18px;">
        #     <td style="position: absolute; top: 0; left: 0; right: 0; background-color: #000; color: #fff; padding: 2px 2px; font-weight: bold; font-size: {box_title_fontsize}; text-align: center; height: {header_row_height}px; line-height: {header_row_height}px; white-space: nowrap; border-bottom: 1px solid #000;">
        #         {dn_display}
        #     </td>
        #     </tr>
        #     <tr>
        #     <td style="position: absolute; top: 18px; bottom: 18px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; padding: 3px;">
        #         <img src="{qr_img_src}" style="width: 100%; height: 100%; object-fit: contain; display: block;" alt="QR">
        #     </td></tr>
        #     <tr>
        #     <td style="position: absolute; bottom: 0; left: 0; right: 0; font-size: 16px; font-weight: bold; color: #000; text-align: center; white-space: nowrap; border-top: 1px solid #000;">
        #         {del_date_val}
        #     </td>
        #     </tr>
        # </table>
        # </td>"""

        # Format HTML rows cleanly based on text availability
        pp_html_row = ""
        if final_pp_value:
            pp_html_row = f"""
            <div style="font-size: 11px; font-weight: normal; position: absolute; bottom: 2px; left: 3px; right: 3px; word-wrap: break-word; text-align: left; display: block; box-sizing: border-box;">
                <b>PP:</b> {final_pp_value}
            </div>
            """
            
        sp_html_row = ""
        if final_sp_value:
            sp_html_row = f"""
            <div style="font-size: 8px; margin-bottom: 4px; width: 100%; word-wrap: break-word;">
                <b>SP:</b> {final_sp_value}
            </div>
            """
            
        tp_html_row = ""
        if final_tp_value:
            tp_html_row = f"""
            <div style="font-size: 8px; margin-bottom: 4px; width: 100%; word-wrap: break-word;">
                <b>TP:</b> {final_tp_value}
            </div>
            """
            
        # Determine what to display on Row 2 (TP) and Row 3 (below TP)
        header_tp_val = final_tp_value
        header_sp_val = final_sp_value

        tp_sp_combined = ""
        if header_tp_val and header_sp_val:
            tp_sp_combined = f"{header_tp_val}<br>{header_sp_val}"
        elif header_tp_val:
            tp_sp_combined = header_tp_val
        elif header_sp_val:
            tp_sp_combined = header_sp_val

        is_box_variant = (sticker_type == "box" or is_box_to_bag_fallback)

        if is_box_variant:
            box_marker_html = ""
            if (sticker_type == "box" or is_box_to_bag_fallback):
                box_marker_html = '<span class="black-box" style="width: 11px; height: 11px; margin-right: 5px; margin-left: 0; vertical-align: middle; display: inline-block;"></span>'

            header_html = f"""
            <style>
                .print-format {{
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                body {{
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                .page-wrapper {{
                    padding: 5px 4px 5px 4px !important;
                }}
            </style>
            <table class="header-layout-table" style="width: 100%; border-collapse: collapse; border: none; margin-bottom: 2px;">
                <tr>
                    <td style="width: 22%; text-align: left; vertical-align: middle; white-space: nowrap; font-weight: bold; font-size: 12px;">
                        {box_marker_html}<span class="sticker-main-title" style="vertical-align: middle;">{main_title}</span>{dot_html}
                    </td>
                    <td style="width: 38%; text-align: center; vertical-align: middle; white-space: nowrap; font-size: 8px;">
                        Packed ID :{packed_id_val}
                    </td>
                    <td style="width: 40%; text-align: left; vertical-align: middle; white-space: nowrap; font-size: 8px;">
                        SO : {sales_order}
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: left; vertical-align: top; font-size: 13px; font-weight: bold; padding-top: 1px; padding-bottom: 0px; line-height: 1.1;">
                        {customer_name}
                    </td>
                    <td style="text-align: left; vertical-align: top; font-size: 9.2px; font-weight: bold; padding-top: 1px; padding-bottom: 0px; white-space: nowrap; line-height: 1.2;">
                        {tp_sp_combined}
                    </td>
                </tr>
            </table>
            """

            item_display_name_box = f"{item_tamil_name} / {item_name}" if item_tamil_name else item_name

            html += f"""
<div class="page-wrapper" style="{page_break_style}">
    <div class="label" style="border: none; padding: 0; height: 1.90in; box-sizing: border-box; overflow: hidden;">
        {header_html}

        <table class="middle-table" style="height: {table_total_height}px;">
            <tr style="height: 18px;">
                <td class="item-column" rowspan="{table_rowspan}" style="width: {item_col_width}; vertical-align: top; padding: 2px 4px; border-right: 1px solid #000;">
                    <div style="font-size: 13px; font-weight: bold; text-transform: uppercase; line-height: 1.2; margin-bottom: 4px;">{item_name}</div>
                    {f'<div style="font-size: {tamil_fontsize}; font-weight: bold; line-height: {tamil_line_height}; margin-bottom: {tamil_margin_bottom};">{item_tamil_name}</div>' if item_tamil_name else ''}
                    <div class="qty-spec" style="margin-bottom: 4px; margin-top: 2px;">{qty_string}</div>
                    <div style="margin-top: 4px; line-height: 1.1; {wrd_row_style}">
                        <b>W:</b> {wrd_uom}<br>
                        <b>R:</b> Rs. {wrd_rate}<br>
                        <b>D:</b> {mfg_date}<br>
                        <b>B:</b> {batch}<br>
                        <b>PP:</b> {final_pp_value}
                    </div>
                </td>
                {row1_cells}
            </tr>
            <tr style="height: {row2_height}px;">
                {row2_cells}
            </tr>
            {f'<tr style="height: {row4_height}px;">{row4_cells}</tr>' if remarks else ''}
            <tr style="height: {row3_height}px;">
                {row3_cells}
            </tr>
            
        </table>
    </div>
</div>
"""
        else:
            dynamic_title = "COVER & ITEM"
            tp_name_display = f"{final_tp_value} : {boxes}" if final_tp_value else ""
            sp_name_display = f"{final_sp_value} : {bags}" if final_sp_value else ""
            
            tp_sp_display_combined = ""
            if tp_name_display and sp_name_display:
                tp_sp_display_combined = f"{tp_name_display}<br>{sp_name_display}"
            elif tp_name_display:
                tp_sp_display_combined = tp_name_display
            elif sp_name_display:
                tp_sp_display_combined = sp_name_display
            
            # Format Tamil and English names separated by a slash
            if item_tamil_name:
                item_display_name = f"{item_tamil_name} <br> {item_name}"
            else:
                item_display_name = item_name
                
            # Calculate dynamic font size and padding based on length of item display name to prevent layout stretching
            item_display_len = len(item_tamil_name + item_name)
            item_padding = "4px 5px"
            if item_display_len <= 12:
                item_font_size = "26px"
            elif item_display_len <= 20:
                item_font_size = "26px"
                item_padding = "3px 4px"
            elif item_display_len <= 30:
                item_font_size = "20px"
                item_padding = "2px 3px"
            else:
                item_font_size = "15px"
                item_padding = "2px 2px"

            mfg_date_short = formatdate(row.custom_mfg_on, "dd.MM.yy") if row.custom_mfg_on else ""

            header_html = f"""
            <style>
                .print-format {{
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                body {{
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                .page-wrapper {{
                    padding: 4px 4px 4px 4px !important;
                }}
            </style>
            <table class="header-layout-table" style="width: 100%; border-collapse: collapse; border: none; margin-bottom: 2px;">
                <tr>
                    <td style="width: 55%; text-align: left; vertical-align: middle; white-space: nowrap; font-size: 8.5px; padding: 2px 3px;">
                        <span class="striped-icon"></span><strong>{dynamic_title}</strong> <span style="margin-left: 8px; font-weight: normal; font-size: 8px;">Packed ID :{packed_id_val}</span>
                    </td>
                    <td style="width: 45%; text-align: left; vertical-align: middle; white-space: nowrap; font-size: 8.5px; padding: 2px 3px;">
                        SO : {sales_order}
                    </td>
                </tr>
                <tr>
                    <td style="text-align: left; vertical-align: top; font-size: 12px; font-weight: bold; padding: 2px 3px 0px 3px; line-height: 1.1;">
                        {customer_name}
                    </td>
                    <td style="text-align: left; vertical-align: top; font-size: 8.5px; padding: 2px 3px 0px 3px; font-weight: bold; white-space: nowrap; line-height: 1.2;">
                        {tp_sp_display_combined}
                    </td>
                </tr>
            </table>
            """

            html += f"""
<div class="page-wrapper" style="{page_break_style}">
    <div class="label" style="border: none; padding: 0; height: 1.90in; box-sizing: border-box; overflow: hidden;">
        {header_html}

        <table style="width: 100%; border-collapse: collapse; border: 1px solid #000; border-bottom: none; table-layout: fixed; margin-bottom: 0px; height: 102px;">
            <tr>
                <!-- Left Side: Item Name and WRD -->
                <td style="width: 77%; vertical-align: top; padding: 0; border: none;">
                    <table style="width: 100%; height: 102px; border-collapse: collapse; border: none; table-layout: fixed;">
                        <tr style="height: 50px;">
                            <td colspan="4" style="background-color: #000; color: #fff; padding: {item_padding}; font-weight: bold; font-size: {item_font_size}; text-align: center; vertical-align: middle; border-bottom: 1px solid #000; height: 50px;">
                                {item_display_name}
                            </td>
                        </tr>
                        <tr style="height: 20px;">
                            <td colspan="4" style="background-color: #fff; white-space: nowrap;color: #000; padding: 2px 2px; font-weight: bold; font-size: 13px; text-align: center; vertical-align: middle; border-bottom: 1px solid #000; height: 20px;">
                                {qty_covers} {primary_uom} / {wrd_uom} / {stock_uom_qty}
                            </td>
                        </tr>
                        <tr style="height: 32px;">
                            <td style="border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center; width: 5%; vertical-align: middle; height: 32px;">
                                <div style="font-size: 12px; font-weight: bold; line-height: 1.1; white-space: nowrap;">(W) {wrd_uom}</div>
                            </td>
                            <td style="border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center; width: 32.73%; vertical-align: middle; height: 32px;">
                                <div style="font-size: 12px; font-weight: bold; line-height: 1.1; white-space: nowrap;">(R) Rs. {wrd_rate}</div>
                            </td>
                            <td style="border-right: 1px solid #000;border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center; width: 34.27%; vertical-align: middle; height: 32px;">
                                <div style="font-size: 12px; font-weight: bold; line-height: 1.1; white-space: nowrap;">(D) {mfg_date_short}</div>
                            </td>
                            <td style="border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center; width: 5%; vertical-align: middle; height: 32px;">
                                <div style="font-size: 12px; font-weight: bold; line-height: 1.1; white-space: nowrap;">(B) {batch}</div>
                            </td>
                    </tr>
                    </table>
                </td>
                <!-- Right Side: dn_display and QR Code -->
                <td style="width: 23%; vertical-align: top; padding: 0; border-left: 1px solid #000;">
                    <table style="width: 100%; height: 102px; border-collapse: collapse; border: none; table-layout: fixed;">
                        <tr style="height: 18px;">
                            <td style="background-color: #000; color: #fff; padding: 2px; font-weight: bold; font-size: 15px; text-align: center; border-bottom: 1px solid #000; vertical-align: middle; white-space: nowrap; height: 24px;">
                                {dn_display}
                            </td>
                        </tr>
                        <tr style="height: 84px;">
                            <td style="text-align: center; vertical-align: middle; padding: 0; height: 84px; border-bottom: 1px solid #000; line-height: 0;">
                                <img src="{qr_img_src}" style="width: 78px; height: 78px; display: inline-block; vertical-align: middle; margin: 0; object-fit: contain;" alt="QR Code">
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <table style="width: 100%; border-collapse: collapse; border: 1px solid #000; border-top: none; background-color: #fff; height: 22px; table-layout: fixed; box-sizing: border-box; margin-top: 0px;">
            <tr>
                <td style="font-size: 11px; font-weight: bold; padding: 2px 4px; text-align: left; vertical-align: top; word-wrap: break-word; border: none; width: 77%; height: 22px; line-height: 1.2;">
                    <b>PP :</b> {final_pp_value}
                </td>
                <td style="font-weight: bold; font-size: 16px; padding: 2px 4px; text-align: center; vertical-align: top; width: 23%; height: 22px; border-left: 1px solid #000; border-top: none; border-bottom: none; border-right: none; white-space: nowrap;">
                    {del_date_val}
                </td>
            </tr>
        </table>
    </div>
</div>
"""
            
    html += "</body></html>"

    pdf = get_pdf(html, options={
        "page-size": "Custom",
        "page-width": "4in",
        "page-height": "2in",
        "margin-top": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "margin-right": "0mm",
        "disable-smart-shrinking": ""
    })

    return base64.b64encode(pdf).decode("utf-8")
