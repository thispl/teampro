# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt
import frappe
from frappe import _
import requests

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns()
    return columns, data

def get_columns():
    return [
        _("ID") + ":Link/MeetLog:110",
        _("Visit Type") + ":Data:150",
        _("Employee") + ":Data:160",
        _("Employee Name") + ":Data:200",
        _("Department") + ":Link/Department:180",
        _("Date") + ":Date:140",
        _("Party") + ":Data:200",
        _("Contact Person") + ":Data:200",
        _("Address") + ":Data:250",
        _("Sequence") + ":Int:90",
        _("Distance") + ":Data:150",
        
        
    ]

def get_data(filters):
    data = []
    docs = get_docs(filters)

    docs_sorted = sorted(
        docs, 
        key=lambda x: (x.employee, x.date_and_time.date(), x.day_sequence)
    )

    previous_doc = {}  

    for doc in docs_sorted:

        doc_date = doc.date_and_time.date()
        key = (doc.employee, doc_date)

        if key not in previous_doc:
            distance = 0
        else:
            prev_doc = previous_doc[key]

            if prev_doc.latitude and prev_doc.longitude:
                prev_lat, prev_lon = float(prev_doc.latitude), float(prev_doc.longitude)
            elif prev_doc.gprs_location:
                prev_lat, prev_lon = map(float, prev_doc.gprs_location.split("/"))
            else:
                prev_lat, prev_lon = 0.0, 0.0

            if doc.latitude and doc.longitude:
                curr_lat, curr_lon = float(doc.latitude), float(doc.longitude)
            elif doc.gprs_location:
                curr_lat, curr_lon = map(float, doc.gprs_location.split("/"))
            else:
                curr_lat, curr_lon = 0.0, 0.0

            distance = get_graphhopper_distance(prev_lat, prev_lon, curr_lat, curr_lon)
            distance=str(distance)

        previous_doc[key] = doc

        party = doc.party_name if doc.visit_type == "Cold call" else doc.sales_follow_up

        row = [
            doc.name,
            doc.visit_type,
            doc.employee,
            doc.employee_name,
            doc.department,
            doc_date,
            party,
            doc.person_to_meet,
            doc.address,
            doc.day_sequence,
            distance
        ]

        data.append(row)

    return data

def get_docs(filters):
    conditions = ''
    params = []

    if filters.from_date and filters.to_date:
        conditions += "AND DATE(date_and_time) BETWEEN %s AND %s "
        params.extend([filters.from_date, filters.to_date])

    if filters.department:
        conditions += "AND department = %s "
        params.append(filters.department)

    if filters.employee:
        conditions += "AND employee = %s "
        params.append(filters.employee)

    
    query = f"""
        SELECT *
        FROM `tabMeetLog`
        WHERE docstatus != 2 {conditions}
        ORDER BY employee, day_sequence ASC
    """

    route = frappe.db.sql(query, params, as_dict=True)
    return route




def get_graphhopper_distance(prev_lat, prev_lon, curr_lat, curr_lon):
    GRAPHOPPER_API_KEY = "f0aec91c-0a94-48c6-9956-0f8915015a21"
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{prev_lat},{prev_lon}", f"{curr_lat},{curr_lon}"],
        "vehicle": "car",
        "locale": "en",
        "calc_points": "false",
        "key": GRAPHOPPER_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        distance_m = data['paths'][0]['distance']
        return round(distance_m / 1000, 2) 
    else:
        frappe.errprint(f"GraphHopper API error: {response.text}")
        return 0

import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)*2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return round(distance, 2)  