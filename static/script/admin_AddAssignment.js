
let unassigned = [];
let assigned = [];
const MAX_LIMIT = 14; // change limit if needed

// HTML elements
const facultySelect = document.getElementById("facultySelect");
const batchSelect = document.getElementById("batchSelect");
const unassignedList = document.getElementById("unassignedList");
const assignedList = document.getElementById("assignedList");

// Load students via backend (AJAX optional)
document.getElementById("loadStudentsBtn").addEventListener("click", () => {
  if (!facultySelect.value || !batchSelect.value) {
    alert("Select faculty and batch first");
    return;
  }

  fetch(`/get_batch_students/${batchSelect.value}/${facultySelect.value}`)
    .then(response => response.json())
    .then(data => {
      unassigned = data.unassigned;
      assigned = data.assigned;
      renderLists();
    });
});

// Render lists
function renderLists() {
  unassignedList.innerHTML = unassigned
    .map(s => `<li>${s.name} (${s.reg_no}) 
      <button onclick="assignStudent('${s.reg_no}')"><i class="fas fa-plus"></i></button>
    </li>`).join("");

  assignedList.innerHTML = assigned
    .map(s => `<li>${s.name} (${s.reg_no}) 
      <button onclick="removeStudent('${s.reg_no}')"><i class="fas fa-minus"></i></button>
    </li>`).join("");
}

// Assign student
function assignStudent(reg) {
  const index = unassigned.findIndex(s => s.reg_no === reg);
  if (index > -1 && assigned.length < MAX_LIMIT) {
    assigned.push(unassigned[index]);
    unassigned.splice(index, 1);
    renderLists();
  }
}

// Remove student
function removeStudent(reg) {
  const index = assigned.findIndex(s => s.reg_no === reg);
  if (index > -1) {
    unassigned.push(assigned[index]);
    assigned.splice(index, 1);
    renderLists();
  }
}

// Random assignment
document.getElementById("randomAssignBtn").addEventListener("click", () => {
  while (assigned.length < MAX_LIMIT && unassigned.length > 0) {
    const rand = Math.floor(Math.random() * unassigned.length);
    assigned.push(unassigned[rand]);
    unassigned.splice(rand, 1);
  }
  renderLists();
});

// Save to backend
document.getElementById("saveAssignmentsBtn").addEventListener("click", () => {
  fetch("/save_assignments/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token }}"
    },
    body: JSON.stringify({
      faculty: facultySelect.value,
      students: assigned.map(s => s.reg_no)
    })
  })
  .then(() => alert("Assignments saved successfully! ✅"));
});

