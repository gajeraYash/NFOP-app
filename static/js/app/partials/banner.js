function getSubscribeForm() {

    $.ajax({
        url: '/subscribe',
        type: "get",
        cache: true,
        dataType: 'html',
        success: function (data) {
            $('#SubscribeForm').html(data)
        }
    });
}
