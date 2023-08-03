$(document).ready(function() {
    var table = $('#mydatatable').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json",
            "infoEmpty": "",      
            "infoFiltered": ""
        },
        "info":false,
        "lengthChange": false,
        "searching": false,
        "pageLength": 6,
        "order": [[ 0, "asc" ]]
    });
});