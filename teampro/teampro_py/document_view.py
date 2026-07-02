import frappe
@frappe.whitelist()
def get_document_manager_data():
    
    docs = frappe.get_single('Document Manager')
    
    
    document_manager_data = []

    for doc in docs.document_manager:  
        document_manager_data.append({
            'name':doc.name,
            'document_type': doc.type,
            'document_title': doc.document_title,
            'department': doc.department,
            'category': doc.category,
            'expiry_date': doc.expiry_date,
            'document':doc.document
            
        })
    
    
    return document_manager_data