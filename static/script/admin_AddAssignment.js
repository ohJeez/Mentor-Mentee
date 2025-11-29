let unassigned = [];
let assigned = [];
let MAX_LIMIT = 20;

// Elements
const facultySelect = document.getElementById("facultySelect");
const batchSelect = document.getElementById("batchSelect");
const unassignedList = document.getElementById("unassignedList");
const assignedList = document.getElementById("assignedList");
const assignCountInput = document.getElementById("assignCount");   // 👈 FIXED
const csrftoken = document.getElementById("csrfToken").value;

// ✅ Load students
document.getElementById("loadStudentsBtn").addEventListener("click", () => {
  if (!facultySelect.value || !batchSelect.value) {
    alert("Please select BOTH faculty & batch ✅");
    return;
  }

  fetch(`${window.getStudentsURL}${batchSelect.value}/${facultySelect.value}`)
    .then(res => {
      if (!res.ok) throw new Error("Bad response");
      return res.json();
    })
    .then(data => {
      unassigned = data.unassigned || [];
      assigned = data.assigned || [];
      renderLists();
    })
    .catch(err => {
      console.error("Error loading students:", err);
      alert("Unable to load students ❌");
    });
});

// ✅ Render lists
function renderLists() {
  unassignedList.innerHTML = unassigned
    .map(
      s => `
      <li data-search="${s.name.toLowerCase()} ${s.reg_no.toLowerCase()}">
        ${s.name} (${s.reg_no})
        <button onclick="assignStudent(${s.student_id})">
          <i class="fas fa-plus"></i>
        </button>
      </li>`
    )
    .join("");

  assignedList.innerHTML = assigned
    .map(
      s => `
      <li data-search="${s.name.toLowerCase()} ${s.reg_no.toLowerCase()}">
        ${s.name} (${s.reg_no})
        <button onclick="removeStudent(${s.student_id})">
          <i class="fas fa-minus"></i>
        </button>
      </li>`
    )
    .join("");
}

// ✅ Assign student (single)
window.assignStudent = id => {
  const index = unassigned.findIndex(s => s.student_id === id);
  if (index > -1) {
    if (assigned.length >= MAX_LIMIT) {
      alert(`Assignment limit reached (${MAX_LIMIT})`);
      return;
    }
    assigned.push(unassigned[index]);
    unassigned.splice(index, 1);
    renderLists();
  }
};

// ✅ Remove student (single)
window.removeStudent = id => {
  const index = assigned.findIndex(s => s.student_id === id);
  if (index > -1) {
    unassigned.push(assigned[index]);
    assigned.splice(index, 1);
    renderLists();
  }
};

// ✅ Search filters
document.getElementById("unassignedSearch").addEventListener("input", e => {
  filterList(unassignedList, e.target.value);
});

document.getElementById("assignedSearch").addEventListener("input", e => {
  filterList(assignedList, e.target.value);
});

function filterList(list, text) {
  text = text.toLowerCase();
  Array.from(list.children).forEach(li => {
    li.style.display = li.dataset.search.includes(text) ? "" : "none";
  });
}

// ✅ Auto assign based on entered count
document.getElementById("randomAssignBtn").addEventListener("click", () => {
  let count = parseInt(assignCountInput.value);

  if (!count || count <= 0) {
    alert("Please enter a valid number ✅");
    return;
  }

  if (count > unassigned.length) {
    alert(`Only ${unassigned.length} students available to assign`);
    count = unassigned.length;
  }

  if (assigned.length + count > MAX_LIMIT) {
    alert(`Max assignment capacity reached (${MAX_LIMIT})`);
    return;
  }

  for (let i = 0; i < count; i++) {
    const r = Math.floor(Math.random() * unassigned.length);
    assigned.push(unassigned[r]);
    unassigned.splice(r, 1);
  }

  renderLists();
});

// ✅ Save assignments
document.getElementById("saveAssignmentsBtn").addEventListener("click", () => {
  if (!facultySelect.value) {
    alert("Select faculty before saving ✅");
    return;
  }

  fetch(window.saveAssignmentsURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      faculty: facultySelect.value,
      students: assigned.map(s => s.student_id),
    }),
  })
    .then(res => res.json())
    .then(data => alert(data.message))
    .catch(err => {
      console.error("Error saving assignments:", err);
      alert("Save failed ❌");
    });
});
