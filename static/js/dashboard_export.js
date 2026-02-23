function exportCSV() {
    const formElement = document.getElementsByClassName('filter-grid')[0].cloneNode();
    formElement.method = 'POST';
    formElement.action = '/dashboard/export/csv';

    document.body.appendChild(formElement);
    formElement.submit();
    document.body.removeChild(formElement);
}

function printElement(elementId) {
    const element = document.getElementById(elementId);

    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);

    const iframeContent = iframe.contentWindow;
    iframeContent.document.open();
    iframeContent.document.write(`
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <!-- Alle CSS-Links kopieren -->
            ${Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
              .map(link => `<link rel="stylesheet" href="${link.href}">`).join('\n')}
            <!-- Inline-Styles des Elements kopieren -->
            <style>${getComputedStyle(element).cssText}</style>
            <!-- Temporäre Print-Styles -->
            <style>
                body * { margin: 0; }
                /* Unterelemente ausblenden */
                .no-print { display: none !important; }
            </style>
        </head>
        <body>${element.innerHTML}</body>
        </html>
    `);
    iframeContent.document.close();
    iframeContent.focus();
    iframeContent.onload = () => iframeContent.print();
    iframeContent.onafterprint = () => document.body.removeChild(iframe);
}
