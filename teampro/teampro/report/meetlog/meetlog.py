import frappe
from frappe import _
import requests

DISTANCE_CACHE = {}

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
        _("Time") + ":Time:140",
        _("Party") + ":Data:200",
        _("Contact Person") + ":Data:200",
        _("Address") + ":Data:250",
        _("Sequence") + ":Int:90",
        _("Distance (km)") + ":Data:150",
    ]

def get_data(filters):
    data = []
    docs = get_docs(filters)

    previous_location = {}  

    for doc in docs:
        doc_date = doc.date_and_time.date()
        doc_time = doc.date_and_time.time()
        key = (doc.employee, doc_date)
        
        curr_lat, curr_lon = 0.0, 0.0
        if doc.latitude and doc.longitude:
            curr_lat, curr_lon = float(doc.latitude), float(doc.longitude)
        elif doc.gprs_location:
            try:
                curr_lat, curr_lon = map(float, doc.gprs_location.split("/"))
            except (ValueError, AttributeError):
                pass

        distance = 0
        if key in previous_location and curr_lat != 0:
            prev_lat, prev_lon = previous_location[key]
            if prev_lat != 0:
                distance = get_graphhopper_distance(prev_lat, prev_lon, curr_lat, curr_lon)

        # Update last known location for this employee/date
        previous_location[key] = (curr_lat, curr_lon)

        party = doc.party_name if doc.visit_type == "Cold call" else doc.sales_follow_up

        row = [
            doc.name, doc.visit_type, doc.employee, doc.employee_name,
            doc.department, doc_date,doc_time, party, doc.person_to_meet,
            doc.address, doc.day_sequence, str(distance)
        ]
        data.append(row)

    return data

def get_docs(filters):
    conditions = ""
    params = []

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND DATE(date_and_time) BETWEEN %s AND %s"
        params.extend([filters.from_date, filters.to_date])

    if filters.get("department"):
        conditions += " AND department = %s"
        params.append(filters.department)

    if filters.get("employee"):
        conditions += " AND employee = %s"
        params.append(filters.employee)

    # Optimized Query: Only selecting required fields
    query = f"""
        SELECT 
            name, visit_type, employee, employee_name, department, 
            date_and_time, party_name, sales_follow_up, person_to_meet, 
            address, day_sequence, latitude, longitude, gprs_location
        FROM `tabMeetLog`
        WHERE docstatus != 2 {conditions}
        ORDER BY employee ASC, date_and_time ASC, day_sequence ASC
    """

    return frappe.db.sql(query, params, as_dict=True)

def get_graphhopper_distance(prev_lat, prev_lon, curr_lat, curr_lon):
    # Skip if coordinates are invalid or haven't moved
    if not all([prev_lat, prev_lon, curr_lat, curr_lon]) or (prev_lat == curr_lat and prev_lon == curr_lon):
        return 0

    # Create a unique key for this pair
    cache_key = (prev_lat, prev_lon, curr_lat, curr_lon)
    if cache_key in DISTANCE_CACHE:
        return DISTANCE_CACHE[cache_key]

    GRAPHOPPER_API_KEY = "f0aec91c-0a94-48c6-9956-0f8915015a21"
    url = "https://graphhopper.com/api/1/route"
    
    params = {
        "point": [f"{prev_lat},{prev_lon}", f"{curr_lat},{curr_lon}"],
        "vehicle": "bike",  # Changed to bike for more accurate road routing
        "key": GRAPHOPPER_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            distance_m = data['paths'][0]['distance']
            distance_km = round(distance_m / 1000, 2)
            
            # Save to cache
            DISTANCE_CACHE[cache_key] = distance_km
            return distance_km
    except Exception as e:
        frappe.log_error(f"GraphHopper Error: {e}")
    
    return 0