import frappe
import json
import requests
from frappe.utils import cint, now_datetime
PASSPORT_LIST = [
  "C8905894",
  "S5727068",
  "V7296146",
  "U9581556",
  "AK698619",
  "C5337888",
  "T3270074",
  "C2899566",
  "C7385329",
  "I0251259",
  "X4509223",
  "V3858070",
  "B8576972",
  "Y6055708",
  "V1022645",
  "AS142325",
  "AS917607",
  "S7158963",
  "V1471837",
  "AW083139",
  "C3339650",
  "B6725235",
  "B9837736",
  "V5134622",
  "W3425795",
  "AP954826",
  "I0210175",
  "C1732052",
  "AM058094",
  "B7497707",
  "R5717465",
  "R7753020",
  "C0546097",
  "B9467862",
  "C3223850",
  "Y5759055",
  "AU175170",
  "B6737844",
  "U7362334",
  "R4934124",
  "X7050965",
  "U0624107",
  "X9171950",
  "W0481993",
  "Y5854298",
  "AB342277",
  "B9043695",
  "R8016735",
  "B6733862",
  "I0617033",
  "R3397847",
  "Y9721760",
  "AP331085",
  "AI858877",
  "C0198159",
  "T6722108",
  "C3595102",
  "W8152323",
  "S9747736",
  "V5305036",
  "R8248059",
  "V0275299",
  "B9839243",
  "R5716094",
  "B7846331",
  "C9162993",
  "B7262171",
  "C8529232",
  "AA704840",
  "W6406365",
  "AM063386",
  "Y1662492",
  "AJ707288",
  "W5497381",
  "AI563113",
  "X9864208",
  "T3160212",
  "V4780214",
  "AV193991",
  "AH135169",
  "V1482898",
  "T2872126",
  "V0141934",
  "C7239314",
  "V8385037",
  "AP519340",
  "C7389383",
  "C6788869",
  "X6719138",
  "T7692842",
  "AI352504",
  "R7749761",
  "V8333418",
  "AG082767",
  "AB271303",
  "Y4630838",
  "W7446222",
  "B7512425",
  "S2180732",
  "C7476477",
  "C6790064",
  "AL183758",
  "AI909410",
  "X5837796",
  "AR080274",
  "C8894825",
  "S2320184",
  "AP525477",
  "AA704822",
  "AL680876",
  "V0421418",
  "R3837642",
  "AB245420",
  "AR687449",
  "W7949562",
  "V0322111",
  "W7141141",
  "S8596555",
  "R7752321",
  "R6422428",
  "AU391738",
  "T8289362",
  "C0185831",
  "U9300980",
  "X8124938",
  "I0545329",
  "Y1551891",
  "T6791440",
  "U9598194",
  "T2542832",
  "W5419858",
  "AU058182",
  "R2441990",
  "S3616225",
  "X3992950",
  "AM035357",
  "W8772916",
  "AW441540",
  "V8812298",
  "Y3409517",
  "S2067873",
  "B8980875",
  "W7473106",
  "C7378185",
  "C7190174",
  "AN467129",
  "B8155277",
  "T2863235",
  "AD846549",
  "Y4877940",
  "T0690758",
  "AB372211",
  "W0483301",
  "B6563270",
  "C8907035",
  "S8606406",
  "Y4150737",
  "R8174653",
  "V4781470",
  "T2061284",
  "C4392789",
  "W1961848",
  "AM163289",
  "W8775021",
  "S9816982",
  "V7500915",
  "W8775021",
  "V0760687",
  "W6274416",
  "C8595412",
  "C0204483",
  "V0323587",
  "V1571056",
  "V1409462",
  "AP939374",
  "C4251415",
  "V0419784",
  "U2268453",
  "Y1356503",
  "R0980245",
  "R8107376",
  "S6969887",
  "C5550373",
  "V8870030",
  "Y4142582",
  "C5554223",
  "Y4146896",
  "I0814361",
  "I0307612",
  "C2722467",
  "V1895230",
  "AU801141",
  "V8877584",
  "AL581414",
  "Y6121238",
  "C8984278",
  "U6885206",
  "AI571571",
  "W4565616",
  "T2153716",
  "T0472194",
  "W0824760",
  "C5076086",
  "BB238648",
  "X5336007",
  "AA934710",
  "W4146372",
  "V7560269",
  "C4234583",
  "AP336572",
  "S9157304",
  "X4709305",
  "Y8800289",
  "C6990134",
  "C0221354",
  "U5359040",
  "U3143954",
  "AT750159",
  "B8952068",
  "S3055662",
  "T7130150",
  "Y8717774",
  "V0499260",
  "S6778023",
  "V6483445",
  "Aw610000",
  "Y4570633",
  "W7963895",
  "C6404711",
  "V0038005",
  "BA330123",
  "C6079394",
  "R7749571",
  "Y8748722",
  "Y2055277",
  "AB246205",
  "V0118855",
  "C5105827",
  "Ai582416",
  "AR820962",
  "Ak381524",
  "Y5776526",
  "R7761559",
  "W4754818",
  "Y3385960",
  "Ap311942",
  "C7241694",
  "BD498718",
  "AI472567",
  "V1471655",
  "B9049022",
  "Ab380861",
  "AH162355",
  "S6770296",
  "W0134713",
  "AF925583",
  "T9038037",
  "Y6213184",
  "AB263877",
  "R7719627",
  "AT758778",
  "AP926629",
  "C4238690",
  "Al167609",
  "V0253912",
  "V0376912",
  "R4323403",
  "AB384560",
  "AK391904",
  "C4815133",
  "AI351641",
  "AF998977",
  "X5611358",
  "V0256681",
  "AG785749",
  "C7554827",
  "AT654041",
  "AK343277",
  "B8591642",
  "AM063488",
  "C4593842",
  "V2677895",
  "Y6191274",
  "AU536039",
  "X6462265",
  "V0399612",
  "V1666120",
  "U8566044",
  "V0349585",
  "C4601044",
  "AB340220",
  "C0555862",
  "AU956412",
  "V0251152",
  "C4160912",
  "AS088774",
  "V9050650",
  "AM321940",
  "BD154295",
  "Y2773921",
  "AA278021",
  "Y2628008",
  "AR839229",
  "Y1869082",
  "Y7560990",
  "AW746741",
  "Y5340004",
  "C6681093",
  "AN622890",
  "AB088274",
  "W9051904",
  "P7130276",
  "V9096763",
  "R0840308",
  "AI904415",
  "R2010699",
  "U9531434",
  "AB686411",
  "X7425441",
  "X7421000",
  "T8844023",
  "AP156671"
]

CANDIDATE_PASSPORT_LIST = [
    "U2268453",
    "Y1356503",
    "R0980245",
    "R8107376",
    "S6969887",
    "C5550373",
    "V8870030",
    "Y4142582",
    "C5554223",
    "Y4146896",
    "I0814361",
    "I0307612",
    "C2722467",
    "V1895230",
    "AU801141",
    "V8877584",
    "AL581414",
    "Y6121238",
    "C8984278",
    "U6885206",
    "AI571571",
    "W4565616",
    "T2153716",
    "T0472194",
    "W0824760",
    "C5076086",
    "BB238648",
    "X5336007",
    "AA934710",
    "W4146372",
    "V7560269",
    "C4234583",
    "AP336572",
    "S9157304",
    "X4709305",
    "Y8800289",
    "C6990134",
    "C0221354",
    "U5359040",
    "U3143954",
    "AT750159",
    "B8952068",
    "S3055662",
    "T7130150",
    "Y8717774",
    "V0499260",
    "S6778023",
    "V6483445",
    "Aw610000",
    "Y4570633",
    "W7963895",
    "C6404711",
    "V0038005",
    "BA330123",
    "C6079394",
    "R7749571",
    "Y8748722",
    "Y2055277",
    "AB246205",
    "V0118855",
    "C5105827",
    "Ai582416",
    "AR820962",
    "Ak381524",
    "Y5776526",
    "R7761559",
    "W4754818",
    "Y3385960",
    "Ap311942",
    "C7241694",
    "BD498718",
    "AI472567",
    "V1471655",
    "B9049022",
    "Ab380861",
    "AH162355",
    "S6770296",
    "W0134713",
    "AF925583",
    "T9038037",
    "Y6213184",
    "AB263877",
    "R7719627",
    "AT758778",
    "AP926629",
    "C4238690",
    "Al167609",
    "V0253912",
    "V0376912",
    "R4323403",
    "AB384560",
    "AK391904",
    "C4815133",
    "AI351641",
    "AF998977",
    "X5611358",
    "V0256681",
    "AG785749",
    "C7554827",
    "AT654041",
    "AK343277",
    "B8591642",
    "AM063488",
    "C4593842",
    "V2677895",
    "Y6191274",
    "AU536039",
    "X6462265",
    "V0399612",
    "V1666120",
    "U8566044",
    "V0349585",
    "C4601044",
    "AB340220",
    "C0555862",
    "AU956412",
    "V0251152",
    "C4160912",
    "AS088774",
    "V9050650",
    "AM321940",
    "BD154295",
    "Y2773921",
    "AA278021",
    "Y2628008",
    "AR839229",
    "Y1869082",
    "Y7560990",
    "AW746741",
    "Y5340004",
    "C6681093",
    "AN622890",
    "AB088274",
    "W9051904",
    "P7130276",
    "V9096763",
    "R0840308",
    "AI904415",
    "R2010699",
    "U9531434",
    "AB686411",
    "X7425441",
    "X7421000",
    "T8844023",
    "AP156671"
]

@frappe.whitelist()
def get_candidate_settings():
    """Returns saved JobPro connection settings."""
    settings = frappe.get_single("Candidate Settings")
    return {
        "jobpro_server_url": settings.get("jobpro_server_url") or "https://jobpro.in",
        "jobpro_api_key": settings.get("jobpro_api_key") or "",
        "has_api_secret": bool(settings.get("jobpro_api_secret")),
        "last_migration_date": str(settings.get("last_migration_date") or "")
    }

@frappe.whitelist()
def start_candidate_migration_to_jobpro(limit=10):
    """
    Enqueues candidate migration for a specified batch limit (default: latest 10).
    """
    settings = frappe.get_single("Candidate Settings")
    server_url = (settings.get("jobpro_server_url") or "https://jobpro.in").strip().rstrip("/")
    if not server_url:
        frappe.throw("JobPro Server URL is not configured. Please configure it in Candidate Settings.")

    limit = cint(limit)
    if limit is None:
        limit = 10

    unmigrated_count = frappe.db.count("Candidate", filters={"migrated": ["in", [0, None]]})
    if unmigrated_count == 0:
        return {
            "status": "completed",
            "message": "All candidates are already marked as Migrated (Migrated ? = 1)."
        }

    target_count = min(limit, unmigrated_count) if limit > 0 else unmigrated_count

    # Enqueue background worker with limit
    frappe.enqueue(
        "teampro.api.jobpro_migration.run_migration_background_worker",
        queue="long",
        timeout=7200,
        limit=limit,
        user=frappe.session.user
    )

    return {
        "status": "queued",
        "total": target_count,
        "message": f"Started migration of latest {target_count} candidate(s) in the background."
    }


def run_migration_background_worker(limit=10, user=None):
    """Background task executing migration for the specified candidate batch."""
    settings = frappe.get_single("Candidate Settings")
    server_url = (settings.get("jobpro_server_url") or "https://jobpro.in").strip().rstrip("/")
    auth_key = settings.get("jobpro_api_key") or ""
    auth_secret = settings.get_password("jobpro_api_secret") or ""

    target_endpoint = f"{server_url}/api/method/jobpro.api.candidate_sync.receive_candidate_from_teampro"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if auth_key and auth_secret:
        headers["Authorization"] = f"token {auth_key.strip()}:{auth_secret.strip()}"

    # Fetch latest unmigrated candidates by creation DESC
    limit = cint(limit)
    limit_clause = f"LIMIT {limit}" if limit > 0 else ""

    candidate_names = frappe.db.sql_list(f"""
        SELECT name
        FROM `tabCandidate`
        WHERE IFNULL(migrated, 0) = 0
        ORDER BY creation DESC
        {limit_clause}
    """)

    total = len(candidate_names)
    migrated_count = 0
    error_count = 0
    current_site_url = (frappe.utils.get_url() or "https://erp.teamproit.com").replace("http://", "https://")

    for cand_name in candidate_names:
        try:
            doc = frappe.get_doc("Candidate", cand_name)
            cand_dict = doc.as_dict()
            cand_dict["site_url"] = current_site_url

            # Serialize child tables
            if hasattr(doc, "table_28") and doc.table_28:
                cand_dict["table_28"] = [child.as_dict() for child in doc.table_28]
            if hasattr(doc, "payment_details") and doc.payment_details:
                cand_dict["payment_details"] = [child.as_dict() for child in doc.payment_details]

            payload_data = {"candidate_data": cand_dict, "site_url": current_site_url}
            payload_json = json.dumps(payload_data, default=str).replace("http://", "https://")

            resp = requests.post(
                target_endpoint,
                headers=headers,
                data=payload_json,
                timeout=60
            )
            resp.raise_for_status()

            res_data = resp.json()
            msg = res_data.get("message") or {}
            if msg.get("status") == "success" or res_data.get("status") == "success":
                frappe.db.set_value("Candidate", cand_name, {
                    "migrated": 1,
                    "error_log": ""
                }, update_modified=False)
                frappe.db.commit()
                migrated_count += 1
            else:
                error_msg = msg.get("message") or str(res_data)
                frappe.db.set_value("Candidate", cand_name, {
                    "migrated": 0,
                    "error_log": f"JobPro Response Error: {error_msg}"
                }, update_modified=False)
                frappe.db.commit()
                frappe.log_error(title="Candidate Migration Failure", message=f"Candidate {cand_name} - JobPro Response Error: {error_msg}")
                error_count += 1

        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            frappe.log_error(title="Candidate Migration Failure", message=str(e))
            frappe.db.set_value("Candidate", cand_name, {
                "migrated": 0,
                "error_log": error_msg
            }, update_modified=False)
            frappe.db.commit()
            error_count += 1

    # Update Candidate Settings with statistics
    try:
        settings.last_migration_date = now_datetime()
        settings.last_migration_summary = f"Tested Batch: {total}, Migrated: {migrated_count}, Errors: {error_count}"
        settings.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        pass

    # Send completion popup to user
    if user:
        frappe.publish_realtime(
            event="msgprint",
            message=f"Candidate Batch Migration Complete! Migrated: {migrated_count}, Errors: {error_count} (out of {total} candidates).",
            user=user
        )


def test_check():

    # existing = set(
    #     frappe.db.sql_list("""
    #         SELECT passport_number
    #         FROM `tabCandidate`
    #         WHERE passport_number IN %(passport_list)s
    #     """, {
    #         "passport_list": tuple(PASSPORT_LIST)
    #     })
    # )

    # missing = [
    #     passport_number
    #     for passport_number in PASSPORT_LIST
    #     if passport_number not in existing
    # ]

    # for i, passport_number in enumerate(PASSPORT_LIST):
    #     if passport_number not in existing:
    #         print(i, "===>", passport_number)

    # print("Missing:", len(missing))

    # # DUPLICATES
    # duplicates = frappe.db.sql("""
    #     SELECT passport_number, COUNT(*) AS count
    #     FROM `tabCandidate`
    #     WHERE passport_number IN %(PASSPORT_LIST)s
    #     GROUP BY passport_number
    #     HAVING COUNT(*) > 1
    #     ORDER BY count DESC
    # """, {
    #     "PASSPORT_LIST": tuple(PASSPORT_LIST)
    # }, as_dict=True)

    # print("Duplicate passport numbers:")

    # for row in duplicates:
    #     print(row.passport_number, "===>", row.count)

    # print("Total duplicate passport numbers:", len(duplicates))

    duplicates = frappe.db.sql("""
        SELECT COUNT(*) AS count
        FROM `tabCandidate`
        WHERE passport_number IN %(PASSPORT_LIST)s
    """, {
        "PASSPORT_LIST": tuple(PASSPORT_LIST)
    }, as_dict=True)

    print("Total count of passport numbers:", duplicates[0].count)

def find_missing_passports():
    existing_passports = set(
        frappe.db.sql_list("""
            SELECT passport_number
            FROM `tabCandidate`
            WHERE passport_number IN %(passport_list)s
        """, {
            "passport_list": tuple(CANDIDATE_PASSPORT_LIST)
        })
    )

    return [
        passport
        for passport in CANDIDATE_PASSPORT_LIST
        if passport not in existing_passports
    ]