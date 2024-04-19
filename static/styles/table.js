const searchInput = document.getElementById("search"); 
const table = document.querySelector('.custom-table');
const tableRows = document.querySelectorAll("tbody tr");
let dynamicMarginBottom = 0;
alternateTableColor(tableRows)


searchInput.addEventListener("keyup", function (event) {
  const inputtedValue = event.target.value.toLowerCase();
  dynamicMarginBottom = 0
  
  tableRows.forEach((row) => {
    if (row.querySelectorAll('td')[1].textContent.toLowerCase().startsWith(inputtedValue)) {
      row.style.display = ""
    } else {
      row.style.display = "none"
      dynamicMarginBottom += 4.2
    }
  });

  table.style.marginBottom = dynamicMarginBottom + "rem"
  alternateTableColor(tableRows)
});

function selectedUsername() {
  currentUser = document.getElementById("userList").value;
  table.style.marginBottom = "0rem"
  dynamicMarginBottom = 0
  if (currentUser == "All Users") {
    displayAllUsers()
  } else {
    tableRows.forEach((row) => {
      if (row.querySelector('td').textContent == currentUser) {
        row.style.display = ""
      } else {
        row.style.display = "none"
        dynamicMarginBottom += 4.2
      }
    })
    
    alternateTableColor(tableRows)
  }
}

function displayAllUsers() {
  tableRows.forEach((row) => {
    row.style.display = ""
  })
  alternateTableColor(tableRows)
}

function sortTableByColumn(table, column, asc = true){
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0]
    const rows = Array.from(tBody.querySelectorAll("tr"));

    const sortedRows = rows.sort((a,b) => {
        var aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim()
        var bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim()
        if (column == 2) {
          aColText = parseInt(aColText)
          bColText = parseInt(bColText)
        }
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier)
        
    });

    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    tBody.append(...sortedRows);

    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${column+1}`).classList.toggle("th-sort-asc", asc) 
    table.querySelector(`th:nth-child(${column+1}`).classList.toggle("th-sort-desc", !asc) 
    alternateTableColor(tableRows)
}

// third parameter = ascending - true, descending - false
sortTableByColumn(table, 2, false)

document.querySelectorAll(".custom-table th").forEach(headerCell => {
  headerCell.addEventListener("click", () => {
    const tableElement = headerCell.parentElement.parentElement.parentElement
    const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell)
    const currentIsAscending = headerCell.classList.contains("th-sort-asc")

    sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    alternateTableColor(tableRows)
  })
})

function alternateTableColor(){
  $('tbody tr:visible:even').css("background-color", "#f3f3f3")
  $('tbody tr:visible:odd').css("background-color", "white")
}


