$(document).ready(function() {

    $('.item-row').on('click', '.reenvio_item', function(event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.data('href');
        var param = [];
        param['url'] = url;
        param['btn'] = btn;

        console.log(param)

        $.confirm({
            title: 'Warning!',
            content: 'Are you sure ? ',
            type: 'blue',
            buttons: {
                yes: function() {
                    AjaxRenviaItem(param);
                },
                no: function() {}
            }
        }, );
    });

    function AjaxRenviaItem(param) {
        $.ajax({
            url: param['url'],
            type: 'POST',
            data: param['query'],
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function(data) {
                if (data.valid !== 'success')
                    notification[data.valid](data.message);



                if (data.valid === 'success') {
                    if (data.redirect_url) {

                        console.log(data.redirect_url);

                        window.location.replace(data.redirect_url);

                    } else {
                        notification[data.valid](data.message);
                        var item_row = param['btn'].closest('.item-row');

                        item_row.hide('slow', function() {
                            /*item_row.replace();*/
                        });
                    }
                }
            },
            error: function() {
                console.log("not done")

            }
        });
    }

})