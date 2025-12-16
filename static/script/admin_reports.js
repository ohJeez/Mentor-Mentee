// ============================
// SHOW / HIDE FILTER FIELDS
// ============================

const reportType = document.getElementById("reportType");

const studentField = document.querySelector(".student-field");
const facultyField = document.querySelector(".faculty-field");
const batchField = document.querySelector(".batch-field");

const timeRange = document.getElementById("timeRange");
const customDates = document.querySelector(".custom-dates");

// Handle report-type change
reportType.addEventListener("change", function () {
    const value = this.value;

    studentField.classList.add("hidden");
    facultyField.classList.add("hidden");
    batchField.classList.add("hidden");

    if (value === "student") studentField.classList.remove("hidden");
    if (value === "faculty") facultyField.classList.remove("hidden");
    if (value === "batch") batchField.classList.remove("hidden");
});

// Handle time range logic
timeRange.addEventListener("change", function () {
    if (this.value === "custom") customDates.classList.remove("hidden");
    else customDates.classList.add("hidden");
});


// ============================
// FETCH REPORT DATA (VIEW REPORT)
// ============================

document.getElementById("viewReportBtn").addEventListener("click", function () {
    const type = document.getElementById("reportType").value;
    const time = document.getElementById("timeRange").value;

    let id = "";

    if (type === "student") {
        id = document.getElementById("studentSelect").value;
    } else if (type === "faculty") {
        id = document.getElementById("facultySelect").value;
    } else if (type === "batch") {
        id = document.getElementById("batchSelect").value;
    }

    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    if (!type) {
        alert("Please select a report type.");
        return;
    }

    if (!id) {
        alert("Please select an item for the chosen report type.");
        return;
    }

    // FIXED URL ↓↓↓
    const url = `/admin_reports_data?type=${type}&id=${id}&range=${time}&start=${start}&end=${end}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("reportTableBody");
            table.innerHTML = "";

            if (data.sessions.length === 0) {
                table.innerHTML = `<tr><td colspan="6" style="text-align:center; color:#888;">No sessions found.</td></tr>`;
                return;
            }

            data.sessions.forEach(s => {
                table.innerHTML += `
                    <tr>
                        <td>${s.date}</td>
                        <td>${s.student}</td>
                        <td>${s.faculty}</td>
                        <td>${s.batch}</td>
                        <td>${s.topics}</td>
                        <td>${s.remarks}</td>
                    </tr>
                `;
            });
        })
        .catch(err => {
            console.error("Error fetching report:", err);
            alert("Error loading report!");
        });
});


// ============================
// DOWNLOAD PDF
// ============================

document.getElementById("downloadPDFBtn").addEventListener("click", function () {
    const type = document.getElementById("reportType").value;
    const time = document.getElementById("timeRange").value;

    let id = "";
    if (type === "student") id = document.getElementById("studentSelect").value;
    if (type === "faculty") id = document.getElementById("facultySelect").value;
    if (type === "batch") id = document.getElementById("batchSelect").value;

    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    if (!type) {
        alert("Please select a report type.");
        return;
    }

    if (!id) {
        alert("Please select an item for the chosen report type.");
        return;
    }

    // FIXED URL ↓↓↓
    const pdfUrl = `/admin_reports_pdf?type=${type}&id=${id}&range=${time}&start=${start}&end=${end}`;

    window.open(pdfUrl, "_blank");
});
