
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        ajax: {
            "url": '/page/folder/{{clientId}}/{{sessionId}}/{{repo_key}}/datatables', "contentType": "application/json", "type": "POST",
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
        "lengthMenu": [20, 40, 60, 80, 100],
        "pageLength": 20,
        columns: [
            { "width": "8%", "data": "key", "title": "KEY", "orderable": false },
            { "width": "75%", "data": "folder", "title": "FOLDER NAME", },
            { "width": "10%", "data": "key", "title": "COUNT", },
            { "width": "10%", "data": "key", "title": "SIZE", },
        ],
        // columnDefs: [{
        //     sClass: "right", searchable: false, orderable: false, bSortable: false, targets: -1, sWidth: "0px",
        //     render: function (data, type, row, meta) {
        //         btnhtml = "<div class=\"btn-group\" role=\"group\">";
        //         btnhtml += "</div>"
        //         return btnhtml;
        //     }
        // }],
    });


    $(".btnBack").on("click", function () {
        window.location.href = '/page/data/';
    });

});