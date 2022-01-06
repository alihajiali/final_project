$('#status_btn').click(function () {


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });



var cart_id = $('#status_btn').attr('data-id')
var text = $('#status_btn').text()


if (text == 'در دست بررسی -> تایید نکردن') {
    var url = '/pay/status_n/'
    var btn_text = 'تایید نکردن -> تایید کردن'
    var btn_class = 'btn btn-warning'
} else if (text == 'تایید نکردن -> تایید کردن') {
    var url = '/pay/status_a/'
    var btn_text = 'تایید کردن -> پرداخت کردن'
    var btn_class = 'btn btn-primary'
} else if (text == 'تایید کردن -> پرداخت کردن') {
    var url = '/pay/status_s/'
    var btn_text = 'پرداخت شده است'
    var btn_class = 'btn btn-success'
} else {
    var url = '/pay/status_s/'
    var btn_text = 'پرداخت شده است'
    var btn_class = 'btn btn-success'
}

$.ajax({
    url: url,
    method: 'POST',
    data: {
        'cart_id': cart_id,
    },
    success: function (data) {
        if (data['status'] == 'ok'){
            $('#status_btn').text(btn_text)
            $('#status_btn').attr({ 'class': btn_class })
        }
    }
})

});