// Function to get selected columns
function getSelectedColumns() {
    var selectedColumns = [];
    $('.column-selector.active').each(function() {
        selectedColumns.push($(this).data('column-name'));
    });
    return selectedColumns;
}

$(document).ready(function() {
    $('.column-selector').click(function() {
        var colIndex = $(this).data('column');
        var isVisible = $('#table-headers th:nth-child(' + colIndex + ')').is(':visible');
        $('#table-headers th:nth-child(' + colIndex + ')').toggle(!isVisible);
        $('#csv-table td:nth-child(' + colIndex + ')').toggle(!isVisible);
        $(this).toggleClass('active');
        var selectedColumns = getSelectedColumns();
        var fileName = $(this).data('file');

        getDuplicateRowsData(fileName, selectedColumns)
    });
});

// Function to send file name to backend API
function getDuplicateRowsData(fileName, selectedColumns) {
    // 
    $.ajax({
        url: '/file_duplicate',
        method: 'POST',
        traditional: true,
        data: {
            'file_name': fileName, // Sending the file name as data
            'selected_columns': selectedColumns,
        },
        success: function(response) {
            const tableHeader = document.querySelector('#table-header');
            const tableBody = document.querySelector('#table-body');
            tableHeader.innerHTML = ''; // Clear existing table headers
            tableBody.innerHTML = ''; // Clear existing table rows

            // Check if data is not empty
            if (response.length > 0) {
                const headers = Object.keys(response[0]);
                const headerRow = document.createElement('tr');

                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    headerRow.appendChild(th);
                });

                tableHeader.appendChild(headerRow);

                // Populate table body with data
                response.forEach(item => {
                    const row = document.createElement('tr');
                    headers.forEach(header => {
                        const cell = document.createElement('td');
                        cell.textContent = item[header];
                        row.appendChild(cell);
                    });
                    tableBody.appendChild(row);
                });
            } else {
                console.log('No data received.');
            }
        },
        error: function(xhr, status, error) {
            // Handle error response from the backend
            console.error('Error sending file name:', error);
        }
    });
}

function showSpinner() {
    var divElement = document.getElementById("spinner");
    divElement.style.display = "flex"
    $('#spinner').show(); // Show the spinner
}

// Function to hide the spinner
function hideSpinner() {
    var divElement = document.getElementById("spinner");
    divElement.style.display = "none"
    $('#spinner').hide(); // Hide the spinner
}

$('#fetch-data-link').click(function() {
    // Show spinner when the link is clicked
    showSpinner();

    setTimeout(function() {
        hideSpinner();
    }, 15000);
})
