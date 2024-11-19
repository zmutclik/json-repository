
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
            { "width": "3%", "data": "row_number", "title": "NO", "orderable": false },
            { "width": "8%", "data": "key", "title": "KEY", "orderable": false },
            { "width": "75%", "data": "label", "title": "FOLDER NAME", },
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
        window.location.href = '/page/folder/{{repo_key}}';
    });

    $("#table_").on("click", 'td', function () {
        $('#json-renderer').html("");
        $("#json-renderer").LoadingOverlay("show");

        api.get('/' + $(this).parents('tr').attr('id'))
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

    });
});