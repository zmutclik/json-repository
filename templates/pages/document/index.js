
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        ajax: {
            "url": '/page/document/{{clientId}}/{{sessionId}}/{{repo_key}}/{{folder_key}}/datatables', "contentType": "application/json", "type": "POST",
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
            { "width": "40%", "data": "label", "title": "DOCUMENT NAME", },
            { "width": "15%", "data": "created_user", "title": "USER", },
            {
                "width": "15%", "data": function (source, type, val) {
                    return "<div class=\"row\">" + moment(source.created_at, "YYYY-MM-DDTHH:mm:ss").format("YYYY-MM-DD") + "</div><div class=\"row\">" + moment(source.created_at, "YYYY-MM-DDTHH:mm:ss").format("HH:mm:ss") + "</div>";
                }
                , "title": "CREATED",
            },
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


    $(".btnBack").on("click", function () {
        window.location.href = '/page/folder/{{repo_key}}';
    });

    $("#table_").on("dblclick", 'td', function () {
        getdata($(this).parents('tr').attr('id'));
    });

    $("#table_").on("click", '.btnOpen', function () {
        getdata($(this).parents('tr').attr('id'));
    });
});

function getdata(id_doc) {
    $('#json-renderer').html("");
    $("#json-renderer").LoadingOverlay("show");

    api.get('/' + id_doc)
        .then(function (response) {
            $('#json-renderer').jsonViewer(response.data, { collapsed: false, withQuotes: false, withLinks: false });
        })
        .catch(function (error) {
            if (error.status == 401 || error.status == 400 || error.status == 404) {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: error.response.data.detail,
                    showConfirmButton: false,
                    timer: 2000
                });
            }
            if (error.status == 500) {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: "System Applikasi Error.!",
                    showConfirmButton: false,
                    timer: 2000
                });
            }
        })
        .finally(() => {
            $("#json-renderer").LoadingOverlay("hide");
        });

}