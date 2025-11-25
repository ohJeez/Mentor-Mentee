const facultySelect = document.getElementById("facultySelect");
const batchSelect = document.getElementById("batchSelect");
const searchInput = document.getElementById("searchInput");
const tableBody = document.getElementById("studentsTableBody");

let loadedStudents = [];

// ✅ Load Assigned Students
document.getElementById("loadBtn").addEventListener("click", () => {
  if (!facultySelect.value) {
    alert("Select a faculty ✅");
    return;
  }

  fetch(`${window.getAssignedURL}?faculty=${facultySelect.value}&batch=${batchSelect.value}`)
    .then(res => res.json())
    .then(data => {
      loadedStudents = data.students;
      renderTable(loadedStudents);
    })
    .catch(() => alert("Failed to load data ❌"));
});

// ✅ Render Table
function renderTable(list) {
  tableBody.innerHTML = list
    .map(s => `
      <tr>
        <td><img src="../static/student_images/${s.student_image}" class="student-photo" /></td>
        <td>${s.name}</td>
        <td>${s.reg_no}</td>
        <td>${s.course_name}</td>
        <td>${s.batch_name}</td>
      </tr>
    `)
    .join("");
}

// ✅ Search
searchInput.addEventListener("input", e => {
  const value = e.target.value.toLowerCase();
  const filtered = loadedStudents.filter(
    s =>
      s.name.toLowerCase().includes(value) ||
      s.reg_no.toLowerCase().includes(value)
  );
  renderTable(filtered);
});
