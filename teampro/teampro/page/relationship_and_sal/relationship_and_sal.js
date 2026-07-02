frappe.pages['relationship-and-sal'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Relationship & Sales Dashboard',
		single_column: true
	});

	frappe.breadcrumbs.add('Teampro');
    if (!document.getElementById('tabler-icons-css')) {
        const link = document.createElement('link');
        link.id = 'tabler-icons-css';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css';
        document.head.appendChild(link);
    }
	const style=document.createElement('style');
	style.innerHTML=`
	.dashboard-wrapper {
	backround-color : #f5f5f5;
	backround-image : none;
	}

		@keyframes blink-border {
		0% {border-color:rgb(151, 158, 153);}
		50% {border-color:transparent ;}
		100% {border-color:rgb(151, 158, 153);}
		}

		.blink-border{
		animation: blink-border 2s infinite;
		border: 2px solid rgb(151, 158, 153);
		}

		@keyframs blink-order-booking{
		0%, 100% {border-color: #3fbab6;}
		50% {border-color: #70d3d1;}
		}

		@keyframes blink-turnover {
		0%, 100% { border-color: #4cb174; }
		50% { border-color: #6ccf94; }
		}

		@keyframes blink-collection {
		0%, 100% { border-color: #d4a017; }
		50% { border-color: #f4c037; }
		}

		@keyframes blink-receivable {
		0%, 100% { border-color: #6a0dad; }
		50% { border-color: #8e3ddf; }
		}

		@keyframes blink-tobill {
		0%, 100% { border-color: #b22222; }
		50% { border-color: #dc3c3c; }
		}

		@keyframes blink-todeliverbill {
		0%, 100% { border-color: #4682b4; }
		50% { border-color: #4682b4;}
		}

		.dashboard-cards{
		display:flex;
		gap:30px;
		flex-wrop:wrop;
		justify-content: space-between;
		}

		.top-actions{
		position:absolute;
		right:10px;
		top:10px;
		display:flex;
		align-item:center;
		gap:10px;
		}

		.top-actions2{
		position:absolute;
		right:10px;
		top:10px;
		display:flex;
		align-item:center;
		gap:10px;
		}

		

		

		.order-booking-card {
			background-color: #0a9396; /* Teal Blue - calm and modern */
			}
		
		.turnover-card {
		background-color: #2e8b57; /* Sea Green */
		}
	
		

		.receivable-card {
		background-color: #4b0082; /* Indigo - strong but professional */
		}

		.tobill-card {
		background-color: #8b0000; /* Dark Red */
		}


		.opp-count-card {
		background-color: #693967; /* Dark Red */
        width: 150px;
        height: 120px;
        min-width: 220px;
        max-width: 130px;
        flex: 0 0 220px;
		}

		.opp-amount-card {
		background-color: #746337; /* Dark Red */
        width: 150px;
        height: 120px;
        min-width: 220px;
        max-width: 130px;
        flex: 0 0 220px;
		}
.fup-card {
    width: 140px;
    height: 70px;
    border-radius: 8px;
    padding: 8px;
    text-align: center;
    font-size: 12px;
    border: 2px solid;   /* bold border */
}

/* count text */
.fup-card .count {
    font-size: 18px;
    font-weight: bold;
    margin-top: 5px;
}


/* 1. Active - Green */
#card-active {
    border-color: #28a745;
    background: #eaf7ee;
}

/* 2. Inactive - Red */
#card-inactive {
    border-color: #dc3545;
    background: #fdeaea;
}

/* 3. Opportunity - Blue */
#card-opportunity {
    border-color: #007bff;
    background: #eaf2ff;
}

/* 4. Replied - Orange */
#card-replied {
    border-color: #fd7e14;
    background: #fff3e8;
}

/* 5. Open - Purple */
#card-open {
    border-color: #6f42c1;
    background: #f3efff;
}


/* 6. Closed - Grey */
#card-closed {
    border-color: #6c757d;
    background: #f1f1f1;
}

/* 7. Pending - Teal */
#card-pending {
    border-color: #20c997;
    background: #e8f9f5;
}

#meetlog-table {
    overflow: visible !important;
}

#meetlog_employee {
    position: relative;
    z-index: 99999;
}

.awesomplete {
    z-index: 999999 !important;
}




.rs-status-card {
    width: 175px;
    height: 82px;
    border-radius: 16px;
    background: #fff;
    border: 1px solid #ebebeb;
    border-right: 4px solid;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 0 16px;
    box-sizing: border-box;
    cursor: pointer;
    transition: transform 0.18s;
}

.rs-status-card:hover {
    transform: translateY(-3px);
}

.rs-icon-circle {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.rs-text-group {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.rs-card-title {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #999;
}

.rs-card-value {
    font-size: 26px;
    font-weight: 700;
    line-height: 1;
    color: #222;
}

/* Active */
.rs-card-active { border-right-color: #28a745; }
.rs-card-active .rs-icon-circle { background: #eaf7ee; color: #28a745; }

/* Inactive */
.rs-card-inactive { border-right-color: #dc3545; }
.rs-card-inactive .rs-icon-circle { background: #fdeaea; color: #dc3545; }

/* Interested */
.rs-card-interested { border-right-color: #007bff; }
.rs-card-interested .rs-icon-circle { background: #e6f0ff; color: #007bff; }

/* Replied */
.rs-card-replied { border-right-color: #fd7e14; }
.rs-card-replied .rs-icon-circle { background: #fff3e6; color: #fd7e14; }

/* Open */
.rs-card-open { border-right-color: #6f42c1; }
.rs-card-open .rs-icon-circle { background: #f0ebfa; color: #6f42c1; }

/* Lead */
.rs-card-lead { border-right-color: #17a2b8; }
.rs-card-lead .rs-icon-circle { background: #e5f6f9; color: #17a2b8; }



/* ========================================= */
/* CARD TEXT */
/* ========================================= */

.rs-card-title{
    font-size:13px;
    text-align:center;
    margin-bottom:6px;
}

.rs-card-value{
    font-size:24px;
    font-weight:700;
}




.dashboard-card{
    position:relative;
    width:200px;
    height:170px;
    background:#fff;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 2px 8px rgba(0,0,0,.12);
}

.card-top-line{
    height:4px;
    width:100%;
    margin:0px;
}

.card-body{
    height:calc(100% - 4px);
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

.card-icon{
    font-size:24px;
    margin-bottom:8px;
}

.card-title{
    font-size:15px;
    font-weight:700;
    color:#000;
}

.card-value{
    font-size:24px;
    font-weight:bold;
    color:green;
    margin-top:10px;
}

.card-sub{
    font-size:12px;
    color:red;
    font-weight:bold;
    margin-top:6px;
}

.card-sub-title{
    font-size:11px;
    color:#555;
}

		<style>

}

	`;
	document.head.appendChild(style);


	$(wrapper).html(`
	
		<div class="dashboard-wrapper">

    <div style="
        padding:10px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:2px;
    ">

        <!-- HEADING -->

        <div style="text-align:center;">

            <h2 style="
                font-weight:bold;
                margin:0;
            ">
                R & S Dashboard
            </h2>

            <div id="current-datetime"
                style="
                    font-size:16px;
                    color:#666;
                    margin-top:5px;
                ">
            </div>

        </div>

        <!-- FILTERS -->

        <div style="
            display:flex;
            gap:20px;
            align-items:center;
            justify-content:center;
            flex-wrap:wrap;
            padding:10px 12px;
            border-radius:8px;
            background:#fff;
            display:none;
            
        ">

            <div class="top-actions-emp"></div>

            <div class="top-actions-service"></div>

            <div class="top-actions-date"></div>

        </div>

    </div>

</div>
			
		
			<div class="active-customer-wrapper" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
			<div class="dashboard-cards-rs" style="display:flex; gap:60px;  overflow-x:auto; morgin-bottom:30px;justify-content:center;">
				<div class="dashboard-card order-booking-card"> </div>
                <div class="dashboard-card tobill-card"></div>
				<div class="dashboard-card turnover-card"></div>
				<div class="dashboard-card receivable-card"></div>
				

			</div>	 
		</div>
        <br>
        <div style="
        background-color:#f5f5f5;
        border:1px solid #ddd;
        border-radius:8px;
        margin:15px;
        padding:10px;
        
    ">

        <!-- HEADER -->
        <div style="
            position:sticky;
            top:0;
            background:#fff;
            z-index:10;
            padding:10px;
            border-bottom:1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
        ">

            <h4 style="
                margin:0;
                text-align:left;
                font-weight:600;
                white-space:nowrap;
                flex-shrink:0;
            ">
                OPPORTUNITY COUNT
            </h4>

        </div>

        <!-- CARDS -->
        <div id="dynamic-service-cards"
            style="
                display:flex;
                gap:35px;
                flex-wrap:nowrap;
                padding:10px;
                overflow-x:auto;
                justify-content:center;
                
            ">
            
            <div class="dashboard-card opp-count-card"></div>

            <div class="dashboard-card opp-amount-card"></div>

        </div>

</div>
    <div class="active-customer-wrapper"
    style="
        background-color:#f5f5f5;
        border:1px solid #ddd;
        border-radius:8px;
        padding:10px;
        box-sizing:border-box;
        margin-left:15px;
        margin-right:15px;
        margin-top:15px;
        
    ">

    <div id="sfp-status-cards"
        style="
            display:flex;
            gap:30px;
            flex-wrap:wrap;
            align-items:center;
            justify-content:center;
            
        ">
    </div>

</div>



   <div style="background-color: #f5f5f5;display: flex; gap: 20px; margin-top: 30px; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 15px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd; border-radius: 8px;">

    <div id="opportunity-table"
        style="
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            box-sizing: border-box;
            margin: 15px 15px 0 15px;
        ">

        <!-- SINGLE LINE HEADER -->

        <div style="
            position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            overflow-x:auto;
        ">

            <!-- HEADING -->

            <h4 style="
                margin: 0;
                text-align: left;
                font-weight: 600;
                white-space:nowrap;
                flex-shrink:0;
            ">
                OPPORTUNITY DETAILS
            </h4>

            <!-- FILTERS -->

            <div id="opportunity-filters"
                style="
                    display:flex;
                    gap:15px;
                    align-items:right;
                    justify-content:right;

                    flex:1;
                    flex-wrap:nowrap;
                    min-width:max-content;
                ">

                <select id="opportunity-filter-owner"
                    class="form-control"
                    style="width: 250px; border: 1px solid #ccc; border-radius: 4px;">

                    <option value="">Select Owner</option>

                </select>

                <select id="opportunity-filter-service"
                    class="form-control"
                    style="width: 180px; border: 1px solid #ccc; border-radius: 4px;">

                    <option value="">Select Service</option>

                </select>

                <select id="opportunity-filter-expweek"
                    class="form-control"
                    style="width: 180px; border: 1px solid #ccc; border-radius: 4px; display:none;">

                    <option value="">Select Exp.Week</option>

                </select>

                    <select id="opportunity-filter-type"
                    class="form-control"
                    style="width: 250px; border: 1px solid #ccc; border-radius: 4px;">

                    <option value="">Select Type</option>

                </select>

            </div>

            <!-- DOWNLOAD -->

            <button
                onclick="download_opportunity_excel()"
                style="
                    background: transparent;
                    border: none;
                    padding: 0;
                    cursor:pointer;
                    flex-shrink:0;
                ">

                <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                    style="width:24px;height:24px;">

            </button>

        </div>

        <!-- TABLE -->

        <div id="opportunity-table-content"
            style="margin-top: 0px; width: 100%; overflow-x: auto;">
        </div>

    </div>

</div>

<div style="background-color: #f5f5f5; display: flex; gap: 10px; margin-top: 30px; 
overflow-x: auto; flex-wrap: nowrap; padding-bottom: 15px; margin-left: 10px; 
margin-right: 10px; border: 1px solid #ddd; border-radius: 8px;">

    <!-- QUOTATION DETAILS (HIDDEN) -->
    <div id="rs-quotation-table" style="display:none; flex:1; min-width:0px; border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box; margin:15px;">
        <h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 5px; text-align: center;">
            QUOTATION DETAILS
        </h4>

        <div id="quotation-filters" style="margin-top: 10px; margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap; justify-content: flex-end;">    
            <select id="quotation-filter-owner" class="form-control" style="width: 250px; border: 1px solid #ccc; border-radius: 4px;">
                <option value="">Select Owner</option>
            </select>

            <select id="quotation-filter-service" class="form-control" style="width: 180px; border: 1px solid #ccc; border-radius: 4px;">
                <option value="">Select Service</option>
            </select>
        </div>

        <div id="quotation-table-content" style="margin-top: 10px; max-height: 300px; overflow-x: auto;"></div>
    </div>


   <!-- APPOINTMENT DETAILS (LEFT SIDE) -->
<div id="appointment-table" style="flex: 1; min-width: 0px; border: 1px solid #dddd; border-radius: 8px; padding: 10px; box-sizing: border-box; margin:5px;">

    <div style="
        position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px !important;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            overflow-x:auto;
    ">
    

        <!-- HEADING -->

        <h4 style="
            margin: 0;
            text-align:left;
            font-weight:600;
            white-space:nowrap;
            
        ">
            APPOINTMENT DETAILS
        </h4>

        <!-- FILTERS -->

        <div style="
            display:flex;
            gap:5px;
            flex-wrap:wrap;
            justify-content:center;
            flex:1;
        ">

            <select id="appointment-filter-owner" class="form-control"
                style="width: 60px; border: 1px solid #ccc; border-radius: 4px;">

                <option value="">Select Owner</option>

            </select>

            <select id="appointment-filter-service" class="form-control"
                style="width: 60px; border: 1px solid #ccc; border-radius: 4px;">

                <option value="">Select Service</option>

            </select>

            <input type="text" id="rs-from-date1" class="form-control" 
                placeholder="App. On From"
                style="width: 60px; border: 1px solid #ccc; border-radius: 4px;"
                onfocus="(this.type='date')" 
                onblur="if(!this.value) this.type='text'">

            <input type="text" id="rs-to-date1" class="form-control" 
                placeholder="App. On To"
                style="width: 60px; border: 1px solid #ccc; border-radius: 4px;"
                onfocus="(this.type='date')" 
                onblur="if(!this.value) this.type='text'">

        </div>

        <!-- DOWNLOAD BUTTON -->

        <button
            onclick="download_appointment_excel()"
            style="
                background:none;
                border:none;
                padding:0;
                cursor:pointer;
            ">

            <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                style="width:24px;height:24px;display:block;">

        </button>

    </div>

    <div id="appointment-table-content"
        style="margin-top: 0px; overflow-x: auto;">
    </div>

</div>

   <!-- TODO STATUS (RIGHT SIDE) -->
<div id="rs-todo-table" style="flex: 1; min-width: 0px; border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box; margin:5px;display:none">

    <!-- HEADER ROW -->

    <div style="
        position: sticky;
        top: 0;
        background: white;
        z-index: 1;
        padding: 5px;

        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:10px;
        flex-wrap:wrap;
    ">

        <!-- HEADING -->

        <h4 style="
            margin: 0;
            padding: 5px;
            text-align: left;
            font-weight:600;
            white-space:nowrap;
        ">
            TODO STATUS
        </h4>

        <!-- FILTERS -->

        <div id="todo-filters" style="
            display:flex;
            gap:15px;
            flex-wrap:wrap;
            justify-content:center;
            flex:1;
        ">

            <select id="todo-filter-owner" class="form-control"
                style="width: 250px; border: 1px solid #ccc; border-radius: 4px;">

                <option value="">Allocated To</option>

            </select>

            <select id="todo-filter-service" class="form-control"
                style="width: 180px; border: 1px solid #ccc; border-radius: 4px;">

                <option value="">Select Service</option>

            </select>

        </div>

    </div>

    <div id="todo-table-content"
        style="margin-top: 10px; overflow-x: auto;">
    </div>

</div>

<div id="meetlog-table-wrapper"
    style="flex:1;
        min-width:0;
        border:1px solid #ddd;
        border-radius:8px;
        padding:10px;
        box-sizing:border-box;
        margin:5px;
        overflow:hidden;">

    <!-- HEADER -->

    <div style="
        position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            height:55px;
    ">

        <!-- HEADING -->

        <h4 style="
            margin: 0;
            text-align:left;
            font-weight:600;
            white-space:nowrap;
        ">
            MEETLOG TABLE
        </h4>

        <!-- FILTERS -->

        <div style="
            display:flex;
            gap:15px;
            flex-wrap:wrap;
            justify-content:center;
            flex:1;
        ">

            <div id="meetlog_from_date" style="width:100px;"></div>

            <div id="meetlog_to_date" style="width:100px;"></div>

            <div id="meetlog_employee" style="width:100px;"></div>

        </div>

        <!-- DOWNLOAD BUTTON -->

        <button
            onclick="download_appointment_excel()"
            style="
                background:none;
                border:none;
                padding:0;
                cursor:pointer;
                marign-right:10px;
            ">

            <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                style="width:24px;height:24px;display:block;">

        </button>

    </div>

    <!-- TABLE -->

    <div id="meetlog-table"
        style="margin-top:20px;overflow-y: auto;height: 100px;overflow-x: auto;">
    </div>

</div>
</div>

<!-- Active / Inactive Customer Report Wrapper -->

<div style="
    display:flex;
    gap:20px;
    margin:15px;
    margin-bottom:25px;
    flex-wrap:nowrap;
">
<!-- Active Customer Report -->

<div style="
    flex:1;
    border:1px solid #ddd;
    border-radius:8px;
    background:#f5f5f5;
    padding:10px;
    min-width:0;
">

    <div style="
        position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            height:55px;
    ">

        <!-- Heading -->

        <h4 style="
            margin: 0;
            text-align:left;
            font-weight:600;
            white-space:nowrap;
        ">
           ACTIVE CUSTOMER REPORT
        </h4>
<button
    onclick="window.download_active_customer_report()"
    style="
        position:absolute;right:10px;background:none;border:none;padding:0;cursor:pointer;
    ">

    <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:24px;height:24px;display:block;">

</button>

    </div>

    <div id="active-customer-report-table"
        style="
            overflow:auto;
            max-height:450px;
            min-height:450px;
            background:white;
            border:1px solid #f8f8f8;
            margin-top:10px;
        ">
    </div>

</div>


<!-- Inactive Customer Report -->

<div style="
    flex:1;
    border:1px solid #ddd;
    border-radius:8px;
    background:#f5f5f5;
    padding:10px;
    min-width:0;
">

    <div style="
        position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            height:55px;
    ">

        <!-- Heading -->

        <h4 style="
            margin: 0;
            text-align:left;
            font-weight:600;
            white-space:nowrap;
        ">
            IN-ACTIVE CUSTOMER REPORT
        </h4>

        <!-- Button -->
<button
    onclick="window.download_inactive_customer_report()"
    style="
        position:absolute;right:10px;top:;background:none;border:none;padding:0;cursor:pointer;
    ">

    <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:24px;height:24px;display:block;">

</button>

    </div>

    <div id="inactive-customer-report-table"
        style="
            overflow:auto;
            max-height:450px;
            min-height:450px;
            background:white;
            border:1px solid #ccc;
            margin-top:10px;
        ">
    </div>

</div>

</div>


<div style="display: flex; gap: 20px; margin-top: 30px; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 15x;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd; border-radius: 8px;">
<div id="fup-table" style="
    width:100%;
    border:1px solid #ffffff;
    border-radius:8px;
    padding:10px;
    box-sizing:border-box;
    margin:15px 0;
     background:#f5f5f5;
">

    <!-- HEADER -->

    <div style="
        position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
            padding: 10px;
            border-bottom: 1px solid #eee;

            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;

            flex-wrap:nowrap;
            height:55px;
        
    ">

        <!-- LEFT -->

        <h4 style="
            margin:0;
            color:black;
            font-weight:600;
            white-space:nowrap;
        ">
            SALES FOLLOW UP DETAILS
        </h4>

        <!-- CENTER FILTERS -->

        <div style="
            display:flex;
            gap:10px;
            flex:1;
            justify-content:center;
            align-items:center;
            flex-wrap:wrap;
        ">

            <select id="fup-filter-call-status"
                class="form-control"
                style="width:180px;border:1px solid #ccc;border-radius:4px;">

                <option value="">Select Call Status</option>

            </select>

            <input type="text"
                id="fup-last-fdate"
                class="form-control"
                placeholder="Last Contaced From"
                style="width:160px;border:1px solid #ccc;border-radius:4px;"
                onfocus="(this.type='date')"
                onblur="if(!this.value) this.type='text'">

            <input type="text"
                id="fup-last-tdate"
                class="form-control"
                placeholder="Last Contaced To"
                style="width:140px;border:1px solid #ccc;border-radius:4px;"
                onfocus="(this.type='date')"
                onblur="if(!this.value) this.type='text'">

            <input type="text"
                id="fup-next-fdate"
                class="form-control"
                placeholder="Next Contaced From"
                style="width:160px;border:1px solid #ccc;border-radius:4px;"
                onfocus="(this.type='date')"
                onblur="if(!this.value) this.type='text'">

            <input type="text"
                id="fup-next-tdate"
                class="form-control"
                placeholder="Next Contaced To"
                style="width:140px;border:1px solid #ccc;border-radius:4px;"
                onfocus="(this.type='date')"
                onblur="if(!this.value) this.type='text'">

        </div>

        <!-- RIGHT BUTTONS -->

        <div style="
            display:flex;
            gap:30px;
            align-items:center;
            white-space:nowrap;
        ">

            <button
                onclick="window.download_fup_excel()"
                style="
                    background:none;
                    border:none;
                    padding:0;
                    cursor:pointer;
                ">

                <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                    style="width:22px;height:22px;">

            </button>

            <button
                onclick="window.download_fup_terr_excel()"
                style="
                    background:none;
                    border:none;
                    padding:0;
                    cursor:pointer;
                ">

                <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                    style="width:22px;height:22px;">

            </button>

        </div>

    </div>

    <!-- TABLE -->

    <div id="fup-table-content"
        style="margin-top:5px;width:100%;overflow-x:auto;">
    </div>

    <div id="fup-table-terr-content"
        style="margin-top:5px;width:100%;overflow-x:auto;">
    </div>

</div>
		`)
		
	//Datetime
	function updateDateTime() {
	const now = new Date();
	const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
	const timeStr = now.toLocaleTimeString();
	document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
	}
	updateDateTime();
	setInterval(updateDateTime, 1000);

	// Refresh
	// $(wrapper).on('click','#refresh-dashboard',() => location.reload());


let rs_multi_filter = frappe.ui.form.make_control({
    df: {
        fieldname: "rs_multi_filter",
        fieldtype: "MultiSelect",
        options:[],
        placeholder: "Select Employees",
        
    },
    parent: $('.top-actions-emp'),
    render_input: true
});

let ser_filter = frappe.ui.form.make_control({
    df: {
        fieldname: "ser_filter",
        fieldtype: "MultiSelect",
        options:[],
        placeholder: "Select Services",

		
        
    },
    parent: $('.top-actions-service'),
    render_input: true
});


frappe.call({

    method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_service_card_data",

    callback: function (r) {

        let data = r.message || [];

        let colors = [
            {
                border: "#dc3545",
                bg: "#fdeaea",
                text: "#dc3545"
            },
            {
                border: "#007bff",
                bg: "#eaf2ff",
                text: "#007bff"
            },
            {
                border: "#28a745",
                bg: "#eaf7ee",
                text: "#28a745"
            },
            {
                border: "#fd7e14",
                bg: "#fff3e8",
                text: "#fd7e14"
            },
            {
                border: "#6f42c1",
                bg: "#f3efff",
                text: "#6f42c1"
            },
            {
                border: "#56fd14",
                bg: "#f6ffe8",
                text: "#56fd14"
            },
            {
                border: "#ce14fd",
                bg: "#f8e8ff",
                text: "#ce14fd"
            },
        ];

        // let html = "";
    let html = `
    </div>
        <div class="dashboard-card opp-count-card" style="
        min-width:50px;
        height:180px;
        border-radius:20px;
        position:relative;
        overflow:hidden;

        justify-content:center;   /* Vertical Center */
        align-items:center;       /* Horizontal Center */
        flex-direction:column;    /* Icon, Title, Value one below another */
    ">
    </div>
    
    <div class="dashboard-card opp-amount-card" style="
        min-width:50px;
        height:180px;
        border-radius:20px;
        position:relative;
        overflow:hidden;
    ">
        <div style="
            position:absolute;
            top:-25px;
            width:80px;
            height:80px;
            border-radius:50%;
            background:#fff7ed;
        "></div>
    </div>
`;



        data.forEach((row, idx) => {

    let clr = colors[idx % colors.length];

    // html += `

    //     <div style="
    //         min-width:100px;
    //         height:100px;
    //         background:#fff;
    //         border-radius:18px;
    //         padding:18px;
    //         position:relative;
    //         overflow:hidden;
    //         border-top:5px solid ${clr.border};
    //         box-shadow:0 4px 14px rgba(0,0,0,0.08);
    //         transition:all .3s ease;
    //     ">

    //         <div style="
    //             position:absolute;
    //             top:-18px;
    //             right:-18px;
    //             width:70px;
    //             height:70px;
    //             border-radius:50%;
    //             background:${clr.bg};
    //             opacity:.5;
    //         "></div>

    //         <!-- SERVICE -->
    //         <div style="
    //             font-size:14px;
    //             font-weight:600;
    //             color:#6b7280;
    //             text-transform:uppercase;
    //             letter-spacing:.8px;
    //             margin-bottom:18px;
    //             position:relative;
    //             z-index:1;
    //         ">
    //             ${row.service}
    //         </div>

    //         <!-- COUNT -->
    //         <div style="
    //             font-size:16px;
    //             font-weight:700;
    //             color:${clr.text};
    //             line-height:1;
    //             position:relative;
    //             z-index:1;
    //         ">
    //             ${row.total}
    //         </div>

    //     </div>
    // `;

    html += `
<div class="dashboard-card">

    <div class="card-top-line"
         style="background:${clr.border}">
    </div>

    <div class="card-body">

        <div class="card-icon">
            📂
        </div>

        <div class="card-title">
            ${row.service}
        </div>

        <div class="card-value"
             style="color:${clr.text}">
            ${row.total}
        </div>

    </div>

</div>
`;
});

$("#dynamic-service-cards").html(html);

    }

});


function load_sfp_status_cards() {

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_sfp_status_cards",
        callback: function(r) {

            let data = r.message || {};

            let html = "";

            html += getStatusCard("#22c55e","🟢","Active",data.active_customer || 0);

            html += getStatusCard("#ef4444","🔴","Inactive",data.inactive_customer || 0);

            html += getStatusCard("#3b82f6","⭐","Interested",data.interested || 0);

            html += getStatusCard("#f97316","💬","Replied",data.replied || 0);

            html += getStatusCard("#8b5cf6","📂","Open",data.open || 0);

            html += getStatusCard("#06b6d4","📊","Lead",data.lead || 0);

            $("#sfp-status-cards").html(html);
        }
    });
}


function getStatusCard(topColor, icon, title, value, valueColor="#16a34a") {
    return `
        <div class="dashboard-card" style="height:180px;width:140px;">
            <div class="card-top-line" style="background:${topColor}"></div>

            <div class="card-body" style="
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                height:calc(100% - 4px);
            ">

                <div class="card-icon">${icon}</div>

                <div class="card-title">
                    ${title}
                </div>

                <div class="card-value" style="color:${valueColor};">
                    ${value}
                </div>

            </div>
        </div>
    `;
}

// =========================================
// PAGE LOAD
// =========================================

setTimeout(() => {

    load_sfp_status_cards();

}, 500);

frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Services",
        filters: {
            custom_eligible_for_dashboard: 1
        },
        fields: ["name"]
    },
    callback: function(r) {
        if (r.message) {
            const service_names = r.message.map(d => d.name);

            ser_filter.set_data(service_names);
        }
    }
});

let date_filter = frappe.ui.form.make_control({
    parent: $('.top-actions-date'),

    df: {
        fieldtype: "Date",
        fieldname: "filter_date",
        placeholder: "Select Date"
    },

    render_input: true
});


setTimeout(() => {
    rs_multi_filter.$wrapper.css("width", "300px");

    rs_multi_filter.$wrapper.find('.taggle').css({
        "min-height": "70px",   
        "padding":    "8px 10px"
    });

    rs_multi_filter.$wrapper.find('.taggle_input').css({
        "height":     "32px",   
        "line-height":"32px",
        "padding":    "4px 6px",
        "font-size":  "14px"
    });
    rs_multi_filter.$wrapper.find('.control-input').css({
        "min-height": "48px"
    });

}, 200);  


setTimeout(() => {
    ser_filter.$wrapper.css("width", "250px");

    ser_filter.$wrapper.find('.taggle').css({
        "min-height": "70px",   
        "padding":    "8px 10px"
    });

    ser_filter.$wrapper.find('.taggle_input').css({
        "height":     "32px",   
        "line-height":"32px",
        "padding":    "4px 6px",
        "font-size":  "14px"
    });
    ser_filter.$wrapper.find('.control-input').css({
        "min-height": "48px"
    });

}, 200);


setTimeout(() => {
    date_filter.$wrapper.css("width", "250px");

    date_filter.$wrapper.find('.taggle').css({
        "min-height": "70px",   
        "padding":    "8px 10px"
    });

    date_filter.$wrapper.find('.taggle_input').css({
        "height":     "32px",   
        "line-height":"32px",
        "padding":    "4px 6px",
        "font-size":  "14px"
    });
    date_filter.$wrapper.find('.control-input').css({
        "min-height": "48px"
    });

}, 200);



$("#active-customer-report-table").html(`
    <div style="padding:20px; text-align:center; font-weight:bold;">
        Loading Data...
    </div>
`);

$("#inactive-customer-report-table").html(`
    <div style="padding:20px; text-align:center; font-weight:bold;">
        Loading Data...
    </div>
`);

frappe.call({
    method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_active_inactive_customer_report",
    callback: function(r) {

        if (r.message) {

            $("#active-customer-report-table").html(
                r.message.active_html
            );

            $("#inactive-customer-report-table").html(
                r.message.inactive_html
            );

        }
    }
});


window.download_active_customer_report = function () {

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_active_customer_report"
    );

};

window.download_inactive_customer_report = function () {

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_inactive_customer_report"
    );

};

const ownerSelect = document.getElementById("opportunity-filter-owner");
const serviceSelect = document.getElementById("opportunity-filter-service"); 

let user_ids = [];  
frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Employee",
        filters: {
            department: ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            status: "Active"
        },
        fields: ["name", "employee_name", "user_id"],
        limit_page_length: 1000
    },
    callback: function (r) {
        if (r.message) {
            const emp_names = r.message.map(emp => emp.employee_name);
            // rs_multi_filter.set_data(emp_names);

            ownerSelect.innerHTML = `<option value="">Select Owner</option>`;
            user_ids = r.message.map(emp => emp.user_id).filter(Boolean);
			rs_multi_filter.set_data(user_ids); 

            r.message.forEach(emp => {
                if (emp.user_id) {
                    const option = document.createElement("option");
                    option.value = emp.user_id;
                    option.textContent = emp.user_id;
                    ownerSelect.appendChild(option);
                }
            });

            loadoppServices(); 
        }
    }
});


function loadoppServices(owner = null) {
    let filters = {
		docstatus: ["!=", 2],
        status: ["not in", ["Lost", "Closed","Converted"]]
	};

    if (owner) {
        filters["owner"] = owner;
    } else {
        filters["owner"] = ["in", user_ids];
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Opportunity",
            filters: filters,
            fields: ["service","expected_week"],
            limit_page_length: 1000
        },
        callback: function (res) {
			if (res.message) {
				const services = [...new Set(res.message.map(row => row.service).filter(Boolean))];

				serviceSelect.innerHTML = `<option value="">Select Service</option>`;
				services.forEach(service => {
					const option = document.createElement("option");
					option.value = service;
					option.textContent = service;
					serviceSelect.appendChild(option);
				});

				const expectedWeekSelect = document.getElementById("opportunity-filter-expweek");
				const weeks = [...new Set(res.message.map(row => row.expected_week).filter(Boolean))];

				expectedWeekSelect.innerHTML = `<option value="">Select Exp.Week</option>`;
				weeks.sort().forEach(week => {
					const option = document.createElement("option");
					option.value = week;
					option.textContent = week;
					expectedWeekSelect.appendChild(option);
				});
			}
		}

    });
}

ownerSelect.addEventListener("change", function () {
    const selected_owner = this.value;
    loadoppServices(selected_owner); 
});

const quoownerSelect = document.getElementById("quotation-filter-owner");
const quoserviceSelect = document.getElementById("quotation-filter-service"); 

let quouser_ids = [];  
frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Employee",
        filters: {
            department: ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            status: "Active"
        },
        fields: ["name", "employee_name", "user_id"],
        limit_page_length: 1000
    },
    callback: function (r) {
        if (r.message) {
            const emp_names = r.message.map(emp => emp.employee_name);
            // rs_multi_filter.set_data(emp_names);

            quoownerSelect.innerHTML = `<option value="">Select Owner</option>`;
            quouser_ids = r.message.map(emp => emp.user_id).filter(Boolean); 
            rs_multi_filter.set_data(quouser_ids);


            r.message.forEach(emp => {
                if (emp.user_id) {
                    const option = document.createElement("option");
                    option.value = emp.user_id;
                    option.textContent = emp.user_id;
                    quoownerSelect.appendChild(option);
                }
            });

            loadquoServices(); 
        }
    }
});

// Step 2: Load services based on selected owner or all users
function loadquoServices(owner = null) {
    let filters = {
		docstatus: ["!=", 2],
        status: ["not in", ["Lost", "Cancelled"]]
	};

    if (owner) {
        filters["owner"] = owner;
    } else {
        filters["owner"] = ["in", quouser_ids];
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Quotation",
            filters: filters,
            fields: ["service_name"],
            limit_page_length: 1000
        },
        callback: function (res) {
            if (res.message) {
                const services = [...new Set(res.message.map(row => row.service_name).filter(Boolean))];

                quoserviceSelect.innerHTML = `<option value="">Select Service</option>`;
                services.forEach(service_name => {
                    const option = document.createElement("option");
                    option.value = service_name;
                    option.textContent = service_name;
                    quoserviceSelect.appendChild(option);
                });
            }
        }
    });
}

// Step 3: On owner change, re-fetch services
quoownerSelect.addEventListener("change", function () {
    const selected_owner = this.value;
    loadquoServices(selected_owner); 
});


const appownerSelect = document.getElementById("appointment-filter-owner");
const appserviceSelect = document.getElementById("appointment-filter-service"); 

let appuser_ids = [];  
frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Employee",
        filters: {
            department: ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            status: "Active"
        },
        fields: ["name", "employee_name", "user_id"],
        limit_page_length: 1000
    },
    callback: function (r) {
        if (r.message) {
            const emp_names = r.message.map(emp => emp.employee_name);
            rs_multi_filter.set_data(emp_names);

            appownerSelect.innerHTML = `<option value="">Select Owner</option>`;
            appuser_ids = r.message.map(emp => emp.user_id).filter(Boolean);
			rs_multi_filter.set_data(appuser_ids); 

            r.message.forEach(emp => {
                if (emp.user_id) {
                    const option = document.createElement("option");
                    option.value = emp.user_id;
                    option.textContent = emp.user_id;
                    appownerSelect.appendChild(option);
                }
            });

            loadappServices(); 
        }
    }
});

// Step 2: Load services based on selected owner or all users
function loadappServices(owner = null) {
    let filters = {
		docstatus: ["!=", 2],
        app_status: ["in", ["Scheduled"]]
	};

    if (owner) {
        filters["account_manager_lead_owner"] = owner;
    } else {
        filters["account_manager_lead_owner"] = ["in", appuser_ids];
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Sales Follow Up",
            filters: filters,
            fields: ["service"],
            limit_page_length: 1000
        },
        callback: function (res) {
            if (res.message) {
                const services = [...new Set(res.message.map(row => row.service).filter(Boolean))];

                appserviceSelect.innerHTML = `<option value="">Select Service</option>`;
                services.forEach(service => {
                    const option = document.createElement("option");
                    option.value = service;
                    option.textContent = service;
                    appserviceSelect.appendChild(option);
                });
            }
        }
    });
}

// Step 3: On owner change, re-fetch services
appownerSelect.addEventListener("change", function () {
    const selected_owner = this.value;
    loadappServices(selected_owner); 
});

const todoownerSelect = document.getElementById("todo-filter-owner");
const todoserviceSelect = document.getElementById("todo-filter-service"); 

let todouser_ids = []; 
frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Employee",
        filters: {
            department: ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            status: "Active"
        },
        fields: ["name", "employee_name", "user_id"],
        limit_page_length: 1000
    },
    callback: function (r) {
        if (r.message) {
            // const emp_names = r.message.map(emp => emp.employee_name);
			
            // rs_multi_filter.set_data(emp_names);

			// const emp_options = r.message.map(emp => ({
			// 	label: emp.employee_name,
			// 	value: emp.user_id
			// }));

			// rs_multi_filter.set_data(emp_options);

            todoownerSelect.innerHTML = `<option value="">Select Owner</option>`;
            todouser_ids = r.message.map(emp => emp.user_id).filter(Boolean); 
			rs_multi_filter.set_data(todouser_ids);

            r.message.forEach(emp => {
                if (emp.user_id) {
                    const option = document.createElement("option");
                    option.value = emp.user_id;
                    option.textContent = emp.user_id;
                    todoownerSelect.appendChild(option);
                }
            });

            loadtodoServices(); 
        }
    }
});

// Step 2: Load services based on selected owner or all users
function loadtodoServices(owner = null) {
    let filters = {
		docstatus: ["!=", 2],
        status: ["not in", ["Cancelled","Closed"]]
	};

    if (owner) {
        filters["owner"] = owner;
    } else {
        filters["owner"] = ["in", todouser_ids];
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "ToDo",
            filters: filters,
            fields: ["custom_todo_type"],
            limit_page_length: 1000
        },
        callback: function (res) {
            if (res.message) {
                const custom_todo_type = [...new Set(res.message.map(row => row.custom_todo_type).filter(Boolean))];

                todoserviceSelect.innerHTML = `<option value="">Select Service</option>`;
                custom_todo_type.forEach(custom_todo_type => {
                    const option = document.createElement("option");
                    option.value = custom_todo_type;
                    option.textContent = custom_todo_type;
                    todoserviceSelect.appendChild(option);
                });
            }
        }
    });
}

// Step 3: On owner change, re-fetch services
todoownerSelect.addEventListener("change", function () {
    const selected_owner = this.value;
    loadtodoServices(selected_owner); 
});

let fupuser_ids = [];

// Step 1: Get user IDs from Employee in required departments
frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Employee",
        filters: {
            department: ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            status: "Active"
        },
        fields: ["user_id"],
        limit_page_length: 1000
    },
    callback: function (r) {
        if (r.message) {
            fupuser_ids = r.message.map(emp => emp.user_id).filter(Boolean);
            loadCallStatuses();  // Call status load after getting user_ids
        }
    }
});


// Step 2: Fetch unique call_status from Sales Follow Up
function loadCallStatuses() {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Sales Follow Up",
            filters: {
                docstatus: ["!=", 2],
                owner: ["in", fupuser_ids]
            },
            fields: ["call_status"],
            limit_page_length: 1000
        },
        callback: function (res) {
            if (res.message) {
                const callStatuses = [...new Set(res.message.map(row => row.call_status).filter(Boolean))];

                const callStatusSelect = document.getElementById("fup-filter-call-status");
                callStatusSelect.innerHTML = `<option value="">Select Call Status</option>`;

                callStatuses.forEach(status => {
                    const option = document.createElement("option");
                    option.value = status;
                    option.textContent = status;
                    callStatusSelect.appendChild(option);
                });
            }
        }
    });
}



// Add these lines right before calling loadopportunityfilter() to build your options layout matrix
const typeSelectElement = document.getElementById("opportunity-filter-type");
if (typeSelectElement) {
    typeSelectElement.innerHTML = `
        <option value="">Select Type</option>
        <option value="Regular">Regular</option>
        <option value="Recurring">Recurring</option>
    `;
}

loadopportunityfilter();
loadquotationfilter();
loadappointmentfilter();
loadtodofilter();
loadfupfilter();
loadfupterr();
loadopportunitylogo();

// Opportunity filter

   // Opportunity filter event listener block (Including Type selection metrics tracking)
$(wrapper).on('change', 
    '#opportunity-filter-owner, #opportunity-filter-service, #opportunity-filter-expweek, #opportunity-filter-type', 
    function () {

        const owner = $('#opportunity-filter-owner').val();
        const service = $('#opportunity-filter-service').val();
        const expweek = $('#opportunity-filter-expweek').val();
        const selectedType = $('#opportunity-filter-type').val(); // Captures "Regular" or "Recurring"

        const owner_list = owner ? [owner] : [];
        const service_list = service ? [service] : [];
        const expweek_list = expweek ? [expweek] : [];

        // 1. Fetch data from your working, original python endpoint signature safely
        frappe.call({
            method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.opportunity_details",
            args: {
                owner: owner_list.length ? JSON.stringify(owner_list) : null,
                services: service_list.length ? JSON.stringify(service_list) : null,
                weeks: expweek_list.length ? JSON.stringify(expweek_list) : null
            },
            callback: function (r) {
                if (r.message) {
                    // Create a virtual DOM container to hold the returned HTML table string safely
                    let $tempHtml = $('<div>').html(r.message);
                    
                    // 2. If a Type filter option is selected, loop through rows and sort
                    if (selectedType) {
                        let serialCounter = 1;
                        
                        // Finds every row inside the table body
                        $tempHtml.find('table tbody tr').each(function () {
                            // Grabs the text inside the Type column cell (14th column is eq(13) index)
                            let rowType = $(this).find('td:eq(13)').text().trim();
                            
                            if (rowType === selectedType) {
                                $(this).show();
                                $(this).find('td:eq(0)').text(serialCounter); // Updates the 'Sr' column to be sequential
                                serialCounter++;
                            } else {
                                $(this).remove(); // Drops the row out of the DOM structure if it mismatch
                            }
                        });
                    }

                    // 3. Inject the clean filtered layout block into your dashboard container canvas
                    $("#opportunity-table-content").html($tempHtml.html());
                }
            }
        });
});
// Quotation filter
	$(wrapper).on('change', 
        '#quotation-filter-owner, #quotation-filter-service', 
        function () {

            const owner = $('#quotation-filter-owner').val();
            const service = $('#quotation-filter-service').val();

            const owner_list = owner ? [owner] : [];
            const service_list = service ? [service] : [];

            loadquotationfilter(owner_list, service_list);
    });

// Appoinment filter
	$(wrapper).on('change', 
        '#appointment-filter-owner, #appointment-filter-service, #rs-from-date1, #rs-to-date1', 
        function () {

            const from_date = $('#rs-from-date1').val();
            const to_date = $('#rs-to-date1').val();
            const owner = $('#appointment-filter-owner').val();
            const service = $('#appointment-filter-service').val();

            const owner_list = owner ? [owner] : [];
            const service_list = service ? [service] : [];

            loadappointmentfilter(owner_list, service_list, from_date, to_date);
    });	

// ToDo filter
	$(wrapper).on('change', 
        '#todo-filter-owner, #todo-filter-service', 
        function () {

            const owner = $('#todo-filter-owner').val();
            const service = $('#todo-filter-service').val();

            const owner_list = owner ? [owner] : [];
            const service_list = service ? [service] : [];

            loadtodofilter(owner_list, service_list);
    });
	
// Follow Up filter
	$(wrapper).on('change', 
        '#fup-filter-call-status, #fup-last-fdate, #fup-last-tdate, #fup-next-fdate, #fup-next-tdate', 
        function () {

            const call_status = $('#fup-filter-call-status').val();
            const Lfrom_date = $('#fup-last-fdate').val();
            const Lto_date = $('#fup-last-tdate').val();
            const Nfrom_date = $('#fup-next-fdate').val();
            const Nto_date = $('#fup-next-tdate').val();

            if (
                (Lfrom_date && !Lto_date) || (!Lfrom_date && Lto_date) ||
                (Nfrom_date && !Nto_date) || (!Nfrom_date && Nto_date)
            ) {
                return;
            }

            loadfupfilter(call_status, Lfrom_date, Lto_date, Nfrom_date, Nto_date);
            loadfupterr(call_status, Lfrom_date, Lto_date, Nfrom_date, Nto_date);
    });	

    

let filter_timer;

function triggerFilter() {
    clearTimeout(filter_timer);

    filter_timer = setTimeout(() => {
        loadopportunityfilter();
		loadquotationfilter();
		loadtodofilter();
		loadappointmentfilter();
		loadfupfilter();
        loadfupterr();
		loadOrderBooking();
		loadTurnover();
		loadReceivable();
		loadToBill();
		loadOppCount();
		loadFupCards();
		

    }, 300);
}

loadOrderBooking();
loadTurnover();
loadReceivable();
loadToBill();
loadOppCount();
loadFupCards();

rs_multi_filter.$wrapper.on("change", triggerFilter);
ser_filter.$wrapper.on("change", triggerFilter);
date_filter.$input.on("change", triggerFilter);

// 		frappe.call({
// 			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_order_booking",
// 			callback: function(r) {
// 				const total = r.message?.total || 0;
// 				const avg = r.message?.average || 0;

// 				const formattedTotal = parseFloat(total).toLocaleString('en-IN', {
// 					style: 'currency',
// 					currency: 'INR',
// 					maximumFractionDigits: 0
// 				});

// 				const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
// 					maximumFractionDigits: 0
// 				});
// 				let arrowSvg = `
// <svg width="70" height="20" viewBox="0 0 60 40">
//     <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
//           stroke="black" stroke-width="2" fill="none" 
//           stroke-linecap="round" stroke-linejoin="round" 
//           style="stroke-dasharray: 4,1;" />
//     <polygon points="57,10 52,0 58,0" fill="black"/>
// </svg>`;
// 				$(wrapper).find('.order-booking-card').html(`
// 					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
// 						<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">Order Booking</h3>
// 						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
// 						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg}]
//                 </div>
// 				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
//             </div>
// 					</div>
// 				`);

// 			}
// 		});


function loadOrderBooking() {

	let owners = normalize(rs_multi_filter.get_value());
	let services = normalize(ser_filter.get_value());

	frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_order_booking",
		args: {
			employee_ids: JSON.stringify(owners),
			services: JSON.stringify(services)
		},
		callback: function(r) {

			const total = r.message?.total || 0;
			const avg = r.message?.average || 0;

			const formattedTotal = parseFloat(total).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});

			const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
				maximumFractionDigits: 0
			});

			// $(wrapper).find('.order-booking-card').html(`
			// 	<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
			// 		<h3 style="margin: 0;text-align:center;font-size:17px;">Order Booking</h3>
			// 		<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
			// 			${formattedTotal}
			// 		</div>
			// 		<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">
			// 			[${formattedAvg}]
			// 		</div>
			// 		<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">
			// 		[Avg]
			// 	</div>
			// 	</div>
			// `);
            $(wrapper).find('.order-booking-card').html(`
            <div class="dashboard-card">

                <div class="card-top-line" style="background:#0a9396"></div>

                <div class="card-body">

                    <div class="card-icon">📦</div>

                    <div class="card-title">
                        Order Booking
                    </div>

                    <div class="card-value">
                        ${formattedTotal}
                    </div>

                    <div class="card-sub">
                        ${formattedAvg}
                    </div>


                </div>

            </div>
            `);
        }
	});
}

function loadTurnover() {

    let owners = normalize(rs_multi_filter.get_value());
    let services = normalize(ser_filter.get_value());

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_turnover",
        args: {
            employee_ids: JSON.stringify(owners),
            services: JSON.stringify(services)
        },
        callback: function(r) {

            const total1 = r.message?.total || 0;
            const avg1 = r.message?.average || 0;

            const formatted = parseFloat(total1).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });

            const formattedAvg1 = parseFloat(avg1).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });

            // $(wrapper).find('.turnover-card').html(`
            //     <div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
            //         <h3 style="margin: 0;text-align:center;font-size:17px;">Turnover</h3>
            //         <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
            //             ${formatted}
            //         </div>
            //         <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">
            //             [${formattedAvg1}]
            //         </div>
            //         <div style="font-size: 10px;color:black;text-align: center;font-weight:bold">
            //             [Avg]
            //         </div>
            //     </div>
            // `);
        
            $(wrapper).find('.turnover-card').html(`
<div class="dashboard-card">

    <div class="card-top-line" style="background:#2e8b57"></div>

    <div class="card-body">

        <div class="card-icon">💰</div>

        <div class="card-title">
            Turnover
        </div>

        <div class="card-value">
            ${formatted}
        </div>

        <div class="card-sub">
            ${formattedAvg1}
        </div>


    </div>

</div>
`);
        }
    });
}

function loadReceivable() {

    let owners = normalize(rs_multi_filter.get_value());
    let services = normalize(ser_filter.get_value());  

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_receivable",
        args: {
            employee_ids: JSON.stringify(owners),
            services: JSON.stringify(services)   
        },
        callback: function(r) {

            const total3 = r.message?.total || 0;
            const avg3 = r.message?.average || 0;

            const formattedtotal3 = parseFloat(total3).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });

            const formattedAvg3 = parseFloat(avg3).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });

            // $(wrapper).find('.receivable-card').html(`
            //     <div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
            //         <h3 style="margin: 0;text-align:center;font-size:17px;">Receivable</h3>

            //         <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
            //             ${formattedtotal3}
            //         </div>

            //         <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">
            //             [${formattedAvg3}]
            //         </div>

            //         <div style="font-size: 10px;color:black;text-align: center;font-weight:bold">
            //             [Avg]
            //         </div>
            //     </div>
            // `);
       
            $(wrapper).find('.receivable-card').html(`
<div class="dashboard-card">

    <div class="card-top-line" style="background:#4b0082"></div>

    <div class="card-body">

        <div class="card-icon">💳</div>

        <div class="card-title">
            Receivable
        </div>

        <div class="card-value">
            ${formattedtotal3}
        </div>

        <div class="card-sub">
            ${formattedAvg3}
        </div>


    </div>

</div>
`);
        }
    });
}
function loadToBill() {

    let owners = normalize(rs_multi_filter.get_value());
    let services = normalize(ser_filter.get_value());

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_bill_value",
        args: {
            employee_ids: JSON.stringify(owners),
            services: JSON.stringify(services)
        },
        callback: function(r) {

            const total4 = r.message?.total || 0;
            const avg4 = r.message?.average || 0;

            const formattedtotal4 = parseFloat(total4).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });

            const formattedAvg4 = parseFloat(avg4).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });

            // $(wrapper).find('.tobill-card').html(`
            //     <div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">

            //         <h3 style="margin: 0;text-align:center;font-size:17px;">
            //             To Bill
            //         </h3>

            //         <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
            //             ${formattedtotal4}
            //         </div>

            //         <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">
            //             [${formattedAvg4}]
            //         </div>

            //         <div style="font-size: 10px;color:black;text-align: center;font-weight:bold">
            //             [Avg]
            //         </div>

            //     </div>
            // `);
        
            $(wrapper).find('.tobill-card').html(`
<div class="dashboard-card">

    <div class="card-top-line" style="background:#8b0000"></div>

    <div class="card-body">

        <div class="card-icon">🧾</div>

        <div class="card-title">
            To Bill
        </div>

        <div class="card-value">
            ${formattedtotal4}
        </div>

        <div class="card-sub">
            ${formattedAvg4}
        </div>


    </div>

</div>
`);
        }
    });
}



// 	frappe.call({
// 		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_deliver_bill_value",
// 		callback: function(r) {
// 			const total5 = r.message?.total || 0;
// 			const average5 = r.message?.average || 0;

// 			const formattedTotal5 = parseFloat(total5).toLocaleString('en-IN', {
// 				style: 'currency',
// 				currency: 'INR',
// 				maximumFractionDigits: 0 
// 			});

// 			const formattedAvg5 = parseFloat(average5).toLocaleString('en-IN', {
// 				maximumFractionDigits: 0
// 			});
// 			let arrowSvg = `
// <svg width="70" height="20" viewBox="0 0 60 40">
//     <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
//           stroke="black" stroke-width="2" fill="none" 
//           stroke-linecap="round" stroke-linejoin="round" 
//           style="stroke-dasharray: 4,1;" />
//     <polygon points="57,10 52,0 58,0" fill="black"/>
// </svg>`;
// 				// const count = r.message || 0;
// 			$(wrapper).find('.todeliverbill-card').html(`
// 				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
// 					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">To Deliver and Bill</h3>
// 					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal5}</div>
// 					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg5}]
//                 </div>
// 				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
//             </div>
// 					</div>
// 			`);
// 		}
// 	});

// function loadToDeliverBill() {

//     let owners = normalize(rs_multi_filter.get_value());
//     let services = normalize(ser_filter.get_value());

//     frappe.call({
//         method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_deliver_bill_value",
//         args: {
//             employee_ids: JSON.stringify(owners),
//             services: JSON.stringify(services)
//         },
//         callback: function(r) {

//             const total5 = r.message?.total || 0;
//             const avg5 = r.message?.average || 0;

//             const formattedTotal5 = parseFloat(total5).toLocaleString('en-IN', {
//                 style: 'currency',
//                 currency: 'INR',
//                 maximumFractionDigits: 0
//             });

//             const formattedAvg5 = parseFloat(avg5).toLocaleString('en-IN', {
//                 maximumFractionDigits: 0
//             });

//             $(wrapper).find('.todeliverbill-card').html(`
//                 <div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">

//                     <h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">
//                         To Deliver and Bill
//                     </h3>

//                     <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
//                         ${formattedTotal5}
//                     </div>

//                     <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">
//                         [${formattedAvg5}]
//                     </div>

//                     <div style="font-size: 10px;color:black;text-align: center;font-weight:bold">
//                         [Avg]
//                     </div>

//                 </div>
//             `);
//         }
//     });
// }

function loadOppCount() {

    let owners = normalize(rs_multi_filter.get_value());
    let services = normalize(ser_filter.get_value());

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.oppcount",
        args: {
            employee_ids: JSON.stringify(owners),
            services: JSON.stringify(services)
        },
        callback: function(r) {

            const count = r.message?.count || 0;
            const amount = r.message?.amount || 0;

            const formattedAmount = parseFloat(amount).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            // OPPORTUNITY COUNT CARD
                // $(wrapper).find('.opp-count-card').html(`
                //     <div style="
                //         width:100%;
                //         height:100%;
                //         padding:18px;
                //         position:relative;
                //         overflow:hidden;
                //     ">

                //         <div style="
                //             position:absolute;
                //             top:-18px;
                //             right:-18px;
                //             width:70px;
                //             height:40px;
                //             border-radius:50%;
                //             background:#eef2ff;
                //             opacity:.8;
                //         "></div>

                //         <div style="
                //             font-size:14px;
                //             font-weight:600;
                //             color:#6b7280;
                //             text-transform:uppercase;
                //             letter-spacing:.8px;
                //             margin-bottom:20px;
                //             position:relative;
                //             z-index:1;
                //         ">
                //             OPP
                //         </div>

                //         <div style="
                //             font-size:16px;
                //             font-weight:700;
                //             color:#4338ca;
                //             line-height:1;
                //             position:relative;
                //             z-index:1;
                //         ">
                //             ${count}
                //         </div>

                //     </div>
                // `);

            $(wrapper).find('.opp-count-card').html(`
            <div class="dashboard-card" style="height:100%; width:100%;">

                <div class="card-top-line" style="background:#6366f1"></div>

                <div class="card-body" style="
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    height:calc(100% - 4px);
                    text-align:center;
                ">

                    <div class="card-icon">🎯</div>

                    <div class="card-title">Opptunity</div>

                    <div class="card-value" style="color:#4338ca;">
                        ${count}
                    </div>

                </div>

            </div>
            `);

                // OPPORTUNITY AMOUNT CARD
                // $(wrapper).find('.opp-amount-card').html(`
                //     <div style="
                //         width:100%;
                //         height:100%;
                //         padding:18px;
                //         position:relative;
                //         overflow:hidden;
                //     ">

                //         <div style="
                //             position:absolute;
                //             width:70px;
                //             height:40px;
                //             border-radius:50%;
                //             background:#fff7ed;
                //             opacity:.8;
                //         "></div>

                //         <div style="
                //             font-size:14px;
                //             font-weight:600;
                //             color:#6b7280;
                //             text-transform:uppercase;
                //             letter-spacing:.8px;
                //             margin-bottom:20px;
                //             position:relative;
                //             z-index:1;
                //         ">
                //             OPP AMT
                //         </div>

                //         <div style="
                //             font-size:16px;
                //             font-weight:700;
                //             color:#b45309;
                //             line-height:1.2;
                //             position:relative;
                //             z-index:1;
                //         ">
                //             ${formattedAmount}
                //         </div>

                //     </div>
                // `);
        
            $(wrapper).find('.opp-amount-card').html(`
                <div class="dashboard-card" style="width:100%; height:100%;">

                    <div class="card-top-line" style="background:#f59e0b"></div>

                    <div class="card-body" style="
                        height:calc(100% - 4px);
                        display:flex;
                        flex-direction:column;
                        justify-content:center;
                        align-items:center;
                        text-align:center;
                    ">

                        <div class="card-icon">💰</div>

                        <div class="card-title">
                            Opp Amount
                        </div>

                        <div class="card-value"
                            style="font-size:18px;color:#b45309;">
                            ${formattedAmount}
                        </div>

                    </div>

                </div>
            `);
            }
    });
}
	frappe.call({
		method: 'teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_tobill_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#tobill-so-table-content').html(r.message);
			}
			else {
				$('#tobill-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});

	frappe.call({
		method: 'teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_receivable_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content').html(r.message);
			}
			else {
				$('#receivable-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	
	$('#opportunity-table-content').html(`<div style="padding: 10px;text-align:center">Loading Opportuntiy details...</div>`);



function normalize(val) {
    if (!val) return [];

    if (Array.isArray(val)) return val;

    if (typeof val === "string") {
        return val.split(",").map(v => v.trim()).filter(v => v);
    }

    return [];
}


function loadopportunityfilter(owner = null, service = null, expweek = null) {

    let top_owners = normalize(rs_multi_filter.get_value());
    let top_services = normalize(ser_filter.get_value());
    let top_weeks = date_filter.get_value() ? [date_filter.get_value()] : [];

    let isTableFilterUsed =
        (owner && owner.length) ||
        (service && service.length) ||
        (expweek && expweek.length);

    let final_owner, final_service, final_week;

    if (isTableFilterUsed) {
        final_owner = owner || [];
        final_service = service || [];
        final_week = expweek || [];
    } else {
        final_owner = top_owners;
        final_service = top_services;
        final_week = top_weeks;
    }

    console.log("FINAL DATA:", final_owner, final_service, final_week);

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.opportunity_details",
        args: {
            owner: JSON.stringify(final_owner),
            services: JSON.stringify(final_service),
            weeks: JSON.stringify(final_week)
        },
        callback: function(r) {
            if (r.message) {
                $('#opportunity-table-content').html(r.message);
            } else {
                $('#opportunity-table-content').html(`<p>No data found.</p>`);
            }
        }
    });
}

window.download_opportunity_excel = function () {
    const owner = $('#opportunity-filter-owner').val();
    const service = $('#opportunity-filter-service').val();
    const expweek = $('#opportunity-filter-expweek').val();
    const opp_type = $('#opportunity-filter-type').val(); // Captures "Regular" or "Recurring"

    const owner_list = owner ? [owner] : [];
    const service_list = service ? [service] : [];
    const expweek_list = expweek ? [expweek] : [];
    const type_list = opp_type ? [opp_type] : [];

    // We pass it to the backend using a clean, safe parameter mapping string
    let url = "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_opportunity_excel"
        + "?owner=" + encodeURIComponent(JSON.stringify(owner_list))
        + "&services=" + encodeURIComponent(JSON.stringify(service_list))
        + "&weeks=" + encodeURIComponent(JSON.stringify(expweek_list))
        + "&opportunity_type=" + encodeURIComponent(JSON.stringify(type_list));

    window.open(url);
};




	$('#quotation-table-content').html(`<div style="padding: 10px;text-align:center">Loading Quotation details...</div>`);


	function loadquotationfilter(owner = null, service= null) {

    let top_owners = normalize(rs_multi_filter.get_value());
    let top_services = normalize(ser_filter.get_value());

    let isTableFilterUsed =
        (owner && owner.length) ||
        (service && service.length) ;

    let final_owner, final_service;

		if (isTableFilterUsed) {
			final_owner = owner || [];
			final_service = service || [];
		} else {
			final_owner = top_owners;
			final_service = top_services;
		}

		console.log("FINAL DATA:", final_owner, final_service);

		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.quotation_details",
			args: {
				owner: JSON.stringify(final_owner),
				services: JSON.stringify(final_service),
			},
			callback: function(r) {
				if (r.message) {
					$('#quotation-table-content').html(r.message);
				} else {
					$('#quotation-table-content').html(`<p>No data found.</p>`);
				}
			}
		});
    
	}

	$('#appointment-table-content').html(`<div style="padding: 10px;text-align:center">Loading Appointment details...</div>`);


	function loadappointmentfilter(owner, service, from_date, to_date) {

	    let top_owners = normalize(rs_multi_filter.get_value());
		let top_services = normalize(ser_filter.get_value());

		let isTableFilterUsed =
			(owner && owner.length) ||
			(service && service.length) ;

		let final_owner, final_service;

			if (isTableFilterUsed) {
				final_owner = owner || [];
				final_service = service || [];
			} else {
				final_owner = top_owners;
				final_service = top_services;
			}

			console.log("FINAL DATA:", final_owner, final_service);

			frappe.call({
				method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.appointment_details",
				args: {
					owner: JSON.stringify(final_owner),
					services: JSON.stringify(final_service),
                    from_date: from_date || null,
                    to_date: to_date || null
				},
				callback: function(r) {
					if (r.message) {
						$('#appointment-table-content').html(r.message);
					} else {
						$('#appointment-table-content').html(`<p>No data found.</p>`);
					}
				}
			});
    
	}


    window.download_appointment_excel = function () {

    let owner = $("#appointment-filter-owner").val() || "";
    let services = $("#appointment-filter-service").val() || "";
    let from_date = $("#rs-from-date1").val() || "";
    let to_date = $("#rs-to-date1").val() || "";

    let params = new URLSearchParams();

    if (owner) {
        params.append("owner", JSON.stringify([owner]));
    }

    if (services) {
        params.append("services", JSON.stringify([services]));
    }

    if (from_date) {
        params.append("from_date", from_date);
    }

    if (to_date) {
        params.append("to_date", to_date);
    }

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_appointment_excel?"
        + params.toString()
    );
}


	$('#todo-table-content').html(`<div style="padding: 10px;text-align:center">Loading ToDo details...</div>`);


	function loadtodofilter(owner, service) {

		let top_owners = normalize(rs_multi_filter.get_value());
		// let top_services = normalize(ser_filter.get_value());

		let isTableFilterUsed =
			(owner && owner.length) ||
			(service && service.length) ;

		let final_owner, final_service;

			if (isTableFilterUsed) {
				final_owner = owner || [];
				final_service = service || [];
			} else {
				final_owner = top_owners;
				// final_service = top_services;
			}

			console.log("FINAL DATA:", final_owner, final_service);

			frappe.call({
				method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.todo_details",
				args: {
					owner: JSON.stringify(final_owner),
					services: JSON.stringify(final_service),
				},
				callback: function(r) {
					if (r.message) {
						$('#todo-table-content').html(r.message);
					} else {
						$('#todo-table-content').html(`<p>No data found.</p>`);
					}
				}
			});
	   
    
	}


    // ========================================
// FROM DATE FILTER
// ========================================

let meetlog_from_date = frappe.ui.form.make_control({

    parent: document.querySelector("#meetlog_from_date"),

    df: {
        fieldtype: "Date",
        fieldname: "from_date",
        placeholder: "From Date",
        default: frappe.datetime.get_today(),

        change: function () {

            load_meetlog_table();

        }
    },

    render_input: true
});


// ========================================
// TO DATE FILTER
// ========================================

let meetlog_to_date = frappe.ui.form.make_control({

    parent: document.querySelector("#meetlog_to_date"),

    df: {
        fieldtype: "Date",
        fieldname: "to_date",
        placeholder: "To Date",
        default: frappe.datetime.get_today(),

        change: function () {

            load_meetlog_table();

        }
    },

    render_input: true
});


// ========================================
// EMPLOYEE FILTER
// ========================================

let meetlog_employee = frappe.ui.form.make_control({

    parent: document.querySelector("#meetlog_employee"),

    df: {
        fieldtype: "Link",
        options: "Employee",
        fieldname: "employee",
        placeholder: "Employee",

        change: function () {

            load_meetlog_table();

        }
    },

    render_input: true
});


// ========================================
// LOAD TABLE
// ========================================

function load_meetlog_table() {

    let employee = meetlog_employee.get_value();

    let from_date = $("#meetlog_from_date input").val();
    let to_date = $("#meetlog_to_date input").val();

    from_date = from_date
        ? frappe.datetime.user_to_str(from_date)
        : frappe.datetime.get_today();

    to_date = to_date
        ? frappe.datetime.user_to_str(to_date)
        : frappe.datetime.get_today();

    $("#meetlog-table").html(`
        <div style="padding:20px;text-align:center;">
            Loading...
        </div>
    `);

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_meetlog_table",
        args: {
            from_date: from_date,
            to_date: to_date,
            employee: employee || ""
        },
        freeze: false,
        callback: function(r) {

            $("#meetlog-table").empty();

            $("#meetlog-table").html(
                r.message ||
                `
                <div style="
                    padding:20px;
                    text-align:center;
                    color:red;
                    font-weight:bold;
                ">
                    No Data Found
                </div>
                `
            );
        }
    });
}

window.download_meetlog_excel = function () {

    let employee = meetlog_employee.get_value();

    let from_date = $("#meetlog_from_date input").val();
    let to_date = $("#meetlog_to_date input").val();

    from_date = from_date
        ? frappe.datetime.user_to_str(from_date)
        : frappe.datetime.get_today();

    to_date = to_date
        ? frappe.datetime.user_to_str(to_date)
        : frappe.datetime.get_today();

    let params = new URLSearchParams();

    params.append("from_date", from_date);
    params.append("to_date", to_date);

    if (employee) {
        params.append("employee", employee);
    }

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_meetlog_excel?"
        + params.toString()
    );
}

setTimeout(() => {

    load_meetlog_table();

}, 500);


	$('#fup-table-content').html(`<div style="padding: 10px;text-align:center">Loading Sales Follow Up details...</div>`);


	function loadfupfilter(call_status = null, Lfrom_date = null, Lto_date = null, Nfrom_date = null, Nto_date = null) {

		let isTableFilterUsed =
			(call_status && call_status.length) ||
			(Lfrom_date || Lto_date || Nfrom_date || Nto_date);

		let final_call_status, final_Lfrom, final_Lto, final_Nfrom, final_Nto;
		let final_owner, final_service;

		if (isTableFilterUsed) {

			final_call_status = call_status || [];
			final_Lfrom = Lfrom_date || null;
			final_Lto = Lto_date || null;
			final_Nfrom = Nfrom_date || null;
			final_Nto = Nto_date || null;

			final_owner = [];
			final_service = [];

		} else {

			final_call_status = [];
			final_Lfrom = null;
			final_Lto = null;
			final_Nfrom = null;
			final_Nto = null;

			final_owner = normalize(rs_multi_filter.get_value());
			final_service = normalize(ser_filter.get_value());
		}

		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.fup_details",
			args: {
				call_status: JSON.stringify(final_call_status),
				Lfrom_date: final_Lfrom,
				Lto_date: final_Lto,
				Nfrom_date: final_Nfrom,
				Nto_date: final_Nto,
				owner: JSON.stringify(final_owner),
				service: JSON.stringify(final_service)
			},
			callback: function(r) {
				if (r.message) {
					$('#fup-table-content').html(r.message);
				} else {
					$('#fup-table-content').html(`<p>No data found.</p>`);
				}
			}
		});
	}
	

    
window.download_fup_excel = function () {

    let owner = $("#followup-filter-owner").val() || [];
    let service = $("#followup-filter-service").val() || [];

    let params = new URLSearchParams();

    params.append("owner", JSON.stringify(owner));
    params.append("service", JSON.stringify(service));

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_fup_excel?"
        + params.toString(),
        "_blank"
    );
};


window.download_fup_terr_excel = function () {

    let owner = $("#followup-filter-owner").val() || [];
    let service = $("#followup-filter-service").val() || [];

    let params = new URLSearchParams();

    params.append("owner", JSON.stringify(owner));
    params.append("service", JSON.stringify(service));

    window.open(
        "/api/method/teampro.teampro.page.relationship_and_sal.relationship_and_sal.download_fup_terr_excel?"
        + params.toString(),
        "_blank"
    );
};


    $('#fup-table-terr-content').html(`<div style="padding: 10px;text-align:center">Loading Sales Follow Up details...</div>`);


	function loadfupterr(call_status = null, Lfrom_date = null, Lto_date = null, Nfrom_date = null, Nto_date = null) {

		let isTableFilterUsed =
			(call_status && call_status.length) ||
			(Lfrom_date || Lto_date || Nfrom_date || Nto_date);

		let final_call_status, final_Lfrom, final_Lto, final_Nfrom, final_Nto;
		let final_owner, final_service;

		if (isTableFilterUsed) {

			final_call_status = call_status || [];
			final_Lfrom = Lfrom_date || null;
			final_Lto = Lto_date || null;
			final_Nfrom = Nfrom_date || null;
			final_Nto = Nto_date || null;

			final_owner = [];
			final_service = [];

		} else {

			final_call_status = [];
			final_Lfrom = null;
			final_Lto = null;
			final_Nfrom = null;
			final_Nto = null;

			final_owner = normalize(rs_multi_filter.get_value());
			final_service = normalize(ser_filter.get_value());
		}

		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.fup_details_terr",
			args: {
				call_status: JSON.stringify(final_call_status),
				Lfrom_date: final_Lfrom,
				Lto_date: final_Lto,
				Nfrom_date: final_Nfrom,
				Nto_date: final_Nto,
				owner: JSON.stringify(final_owner),
				service: JSON.stringify(final_service)
			},
			callback: function(r) {
				if (r.message) {
					$('#fup-table-terr-content').html(r.message);
				} else {
					$('#fup-table-terr-content').html(`<p>No data found.</p>`);
				}
			}
		});
	}
	

function loadFupCards() {

    let employee_ids = rs_multi_filter.get_value() || [];
    let services = ser_filter.get_value() || [];

    frappe.call({
        method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_fup_card_counts",
        args: {
            employee_ids: JSON.stringify(employee_ids),  
            services: JSON.stringify(services),          
        },
        callback: function(r) {

            let d = r.message || {};

            $('#card-active').html(
                getStatusCard("#22c55e","🟢","Active",d.active || 0)
            );

            $('#card-inactive').html(
                getStatusCard("#ef4444","🔴","Inactive",d.inactive || 0)
            );

            $('#card-opportunity').html(
                getStatusCard("#3b82f6","🎯","Opportunity",d.opportunity || 0)
            );

            $('#card-opportunity-amount').html(
                getStatusCard("#f59e0b","💰","Opp Amount",d.opportunity_amount || 0,"#b45309")
            );

            $('#card-replied').html(
                getStatusCard("#f97316","💬","Replied",d.replied || 0)
            );

            $('#card-open').html(
                getStatusCard("#8b5cf6","📂","Open",d.open || 0)
            );

            $('#card-closed').html(
                getStatusCard("#6b7280","✅","Closed",d.closed || 0)
            );
        }
    });
}


	function loadopportunitylogo() {
	frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_opportunity_logo",
	
		callback: function(r) {
			if (r.message) {
				$('#opportunity-logo').html(r.message);
			} else {
				$('#opportunity-logo').html(`<p>No data found.</p>`);
			}
		}
	});
}

}

