// =============================
// REPORT FILTERING LOGIC
// =============================

// Elements
const reportType = document.getElementById("reportType");
const studentField = document.querySelector(".student-field");
const facultyField = document.querySelector(".faculty-field");
const batchField = document.querySelector(".batch-field");

const studentSelect = document.getElementById("studentSelect");
const facultySelect = document.getElementById("facultySelect");
const batchSelect = document.getElementById("batchSelect");

const timeRange = document.getElementById("timeRange");
const customDates = document.querySelector(".custom-dates");

const viewBtn = document.getElementById("viewReportBtn");
const downloadBtn = document.getElementById("downloadPDFBtn");

const reportTableBody = document.getElementById("reportTableBody");

// Backend URLs
const viewURL = "/admin_reports/fetch/";
const pdfURL = "/admin_reports/pdf/";


// =============================
// SHOW FIELDS BASED ON TYPE
// =============================
reportType.addEventListener("change", () => {
    const type = reportType.value;

    studentField.classList.add("hidden");
    facultyField.classList.add("hidden");
    batchField.classList.add("hidden");

    if (type === "student") studentField.classList.remove("hidden");
    if (type === "faculty") facultyField.classList.remove("hidden");
    if (type === "batch") batchField.classList.remove("hidden");
});


// =============================
// SHOW CUSTOM DATES
// =============================
timeRange.addEventListener("change", () => {
    customDates.classList.toggle("hidden", timeRange.value !== "custom");
});


// =============================
// VIEW REPORT
// =============================
viewBtn.addEventListener("click", () => {

    const params = new URLSearchParams({
        type: reportType.value,
        student: studentSelect.value,
        faculty: facultySelect.value,
        batch: batchSelect.value,
        time: timeRange.value,
        start: document.getElementById("startDate").value,
        end: document.getElementById("endDate").value
    });

    fetch(`${viewURL}?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
            reportTableBody.innerHTML = "";

            if (data.sessions.length === 0) {
                reportTableBody.innerHTML = `
                    <tr><td colspan="6" style="text-align:center; color:gray;">No sessions found</td></tr>
                `;
                return;
            }

            data.sessions.forEach(s => {
                reportTableBody.innerHTML += `
                    <tr>
                        <td>${s.session_date}</td>
                        <td>${s.student}</td>
                        <td>${s.faculty}</td>
                        <td>${s.topics_discussed}</td>
                        <td>${s.remarks || "-"}</td>
                        <td>${s.action_plan || "-"}</td>
                    </tr>
                `;
            });
        })
        .catch(err => {
            alert("Error loading report!");
        });
});


// =============================
// DOWNLOAD PDF
// =============================
downloadBtn.addEventListener("click", () => {

    const params = new URLSearchParams({
        type: reportType.value,
        student: studentSelect.value,
        faculty: facultySelect.value,
        batch: batchSelect.value,
        time: timeRange.value,
        start: document.getElementById("startDate").value,
        end: document.getElementById("endDate").value
    });

    window.open(`${pdfURL}?${params.toString()}`, "_blank");
});
