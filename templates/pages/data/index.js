
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        ajax: {
            "url": '/page/data/{{clientId}}/{{sessionId}}/datatables', "contentType": "application/json", "type": "POST",
            "data": function (d) {
                return JSON.stringify(d);
            }, 'beforeSend': function (request) { request.setRequestHeader("Authorization", api.defaults.headers['Authorization']); }
        },
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        "lengthMenu": [10, 20, 40, 60, 80, 100],
        "pageLength": 10,
        columns: [
            { "width": "5%", "data": "row_number", "title": "NO", "orderable": false },
            { "width": "10%", "data": "key", "title": "KEY", "orderable": false },
            { "width": "60%", "data": "repository", "title": "REPOSIRORY NAME", },
            { "width": "10%", "data": "count", "title": "COUNT", },
            {
                "width": "10%", "data": function (source, type, val) {
                    return filesize(source.size);
                }
                , "title": "SIZE",
            },
            { "width": "5%", "data": "key", "title": "", },
        ],
        columnDefs: [
            {
                targets: [2],
                className: 'dt-head-left'
            },
            {
                targets: [2],
                className: 'dt-body-left'
            },
            {
                targets: [0, 1, 3, 4],
                className: 'dt-head-center'
            },
            {
                targets: [0, 1, 3, 4],
                className: 'dt-body-center'
            }, {
                sClass: "right", searchable: false, orderable: false, bSortable: false, targets: -1, sWidth: "0px",
                render: function (data, type, row, meta) {
                    btnhtml = "<button type=\"button\" class=\"btn btn-outline-dark btn-sm btnOpen\"><i style='font-size:24px' class='fas'>&#xf07c;</i></button>";
                    return btnhtml;
                }
            }
        ]
    });


    $("#table_").on("dblclick", 'td', function () {
        window.location.href = '/page/folder/' + $(this).parents('tr').find('td:eq(1)').text();
    });

    $("#table_").on("click", '.btnOpen', function () {
        window.location.href = '/page/folder/' + $(this).parents('tr').find('td:eq(1)').text();
    });
});