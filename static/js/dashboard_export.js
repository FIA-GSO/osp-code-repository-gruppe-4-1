function exportCSV() {
    const formElement = document.getElementsByClassName('filter-grid')[0].cloneNode();
    formElement.method = 'POST';
    formElement.action = '/dashboard/export/csv';

    document.body.appendChild(formElement);
    formElement.submit();
    document.body.removeChild(formElement);
}