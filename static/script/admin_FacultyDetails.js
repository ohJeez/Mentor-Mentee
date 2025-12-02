
  document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      const dropdown = this.closest('.dropdown');
      dropdown.classList.toggle('open');
    });
  });

function applyFilter() {
  const searchValue = document.getElementById('studentSearch').value.toLowerCase();
  const batchValue = document.getElementById('batchFilter').value.toLowerCase();
  const rows = document.querySelectorAll('.students-table tbody tr');

  rows.forEach(row => {
    if (row.innerText.includes('No students assigned')) return;

    const name = row.cells[1].textContent.toLowerCase();
    const reg = row.cells[2].textContent.toLowerCase();
    const batch = row.cells[4].textContent.toLowerCase();

    const matchesSearch = !searchValue || name.includes(searchValue) || reg.includes(searchValue);
    const matchesBatch = !batchValue || batch.includes(batchValue);

    row.style.display = (matchesSearch && matchesBatch) ? '' : 'none';
  });
}

document.getElementById('applyFilterBtn').addEventListener('click', applyFilter);

document.getElementById('studentSearch').addEventListener('keyup', applyFilter);
