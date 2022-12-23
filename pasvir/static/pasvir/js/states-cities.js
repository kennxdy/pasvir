$("#id_state").change(function () {
    var url = $("#form").attr("data-cities-url");
    var stateId = $(this).val();

    $.ajax({
        url: url,
        data: {
            'state': stateId
        },
        success: function (data) {
            $("#id_city").html(data);
        }
    });

});
