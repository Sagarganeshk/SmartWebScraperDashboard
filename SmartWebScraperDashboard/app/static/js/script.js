document.addEventListener("DOMContentLoaded", function () {
    const darkToggle = document.getElementById("darkModeToggle");
    const body = document.body;

    // Dark mode
    if (localStorage.getItem("dark-mode") === "enabled") {
        body.classList.add("dark-mode");
        darkToggle.checked = true;
    }

    darkToggle.addEventListener("change", () => {
        body.classList.toggle("dark-mode");
        localStorage.setItem("dark-mode", body.classList.contains("dark-mode") ? "enabled" : "disabled");
    });

    // Pagination init
    ["jobs", "news", "products"].forEach(section => paginateTable(section));

    // Metrics
    updateMetrics();
});

function searchTable(section) {
    const input = document.getElementById(`${section}Search`).value.toLowerCase();
    const rows = document.querySelectorAll(`#${section}Table tbody tr`);
    rows.forEach(row => {
        const match = Array.from(row.cells).some(cell =>
            cell.textContent.toLowerCase().includes(input)
        );
        row.style.display = match ? "" : "none";
    });
    updateMetrics();
}

function sortTable(section, key) {
    const index = key === 'title' ? 0 : 1;
    const rows = Array.from(document.querySelectorAll(`#${section}Table tbody tr`));
    rows.sort((a, b) =>
        a.cells[index].textContent.localeCompare(b.cells[index].textContent)
    );
    const tbody = document.querySelector(`#${section}Table tbody`);
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
}

function paginateTable(section, rowsPerPage = 5) {
    const table = document.getElementById(`${section}Table`);
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    const pagination = document.getElementById(`${section}Pagination`);

    function showPage(page) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rows.forEach((row, i) => {
            row.style.display = i >= start && i < end ? "" : "none";
        });

        pagination.innerHTML = "";
        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            if (i === page) btn.classList.add("active");
            btn.onclick = () => showPage(i);
            pagination.appendChild(btn);
        }
    }

    showPage(1);
}

function exportToCSV(section) {
    const rows = document.querySelectorAll(`#${section}Table tr`);
    let csv = "";
    rows.forEach(row => {
        const cells = row.querySelectorAll("td, th");
        csv += Array.from(cells).map(cell => `"${cell.textContent}"`).join(",") + "\n";
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${section}.csv`;
    link.click();
}

function updateMetrics() {
    ["jobs", "news", "products"].forEach(section => {
        const visibleRows = Array.from(document.querySelectorAll(`#${section}Table tbody tr`))
            .filter(row => row.style.display !== "none");
        const countSpan = document.getElementById(`${section}Count`);
        if (countSpan) countSpan.textContent = visibleRows.length;
    });
}

// JOB FILTER
document.getElementById("jobFilter").addEventListener("change", function () {
  const selected = this.value.toLowerCase();
  document.querySelectorAll(".job-item").forEach(item => {
    const company = item.getAttribute("data-company").toLowerCase();
    item.style.display = selected === "all" || company === selected ? "block" : "none";
  });
});

// NEWS FILTER
document.getElementById("newsFilter").addEventListener("change", function () {
  const selected = this.value.toLowerCase();
  document.querySelectorAll(".news-item").forEach(item => {
    const source = item.getAttribute("data-source").toLowerCase();
    item.style.display = selected === "all" || source === selected ? "block" : "none";
  });
});

// PRODUCT FILTER
document.getElementById("productFilter").addEventListener("input", function () {
  const keyword = this.value.toLowerCase();
  document.querySelectorAll(".product-item").forEach(item => {
    const name = item.getAttribute("data-name").toLowerCase();
    item.style.display = name.includes(keyword) ? "block" : "none";
  });
});
