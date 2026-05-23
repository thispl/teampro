// frappe.ready(function () {
//     frappe.call({
//         method: "teampro.api.get_user_target",
//         callback: function (r) {
//             let targetValue = r.message?.target_value;
//             let defaultLogo = document.querySelector(".default-logo");
//             let userTargetLogo = document.querySelector(".user-target-logo");

//             if (targetValue) {
//                 if (userTargetLogo) userTargetLogo.style.display = "flex";  // flex to keep centering
//                 if (defaultLogo) defaultLogo.style.display = "none";

//                 let targetValueSpan = userTargetLogo.querySelector(".custom-target-value");
//                 if (targetValueSpan) targetValueSpan.textContent = targetValue;
//             } else {
//                 if (userTargetLogo) userTargetLogo.style.display = "none";
//                 if (defaultLogo) defaultLogo.style.display = "block";
//             }
//         }
//     });
// });