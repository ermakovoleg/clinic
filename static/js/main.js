function next_tab(tab){
    $('.tab').addClass('hidden').removeClass('active');
    $(tab).next().removeClass('hidden').addClass('active');
}
function in_array(value, array) {
    for(var i = 0; i < array.length; i++) {
        if(array[i] == value) return true;}
    return false;
}

function upd_button(busy_time){
    html = '';
    for (var i = 9; i <= 17; i++) {
        if (in_array(i, busy_time)) {
            html += '<button type="button" class="btn btn-default" disabled="disabled">'+ i +'</button>';
        } else{
            html += '<button type="button" class="btn btn-default">'+ i +'</button>';
        }
    }
    $('#timeline').html(html);
    $('#timeline button').click(function(){
        $(this).siblings().removeClass('btn-primary');
        $(this).addClass('btn-primary')
    });
}

function upd_time(doctor_id, date){
    $.ajax({
        url: "/doctor/" + doctor_id + "/",
        type: "GET",
        data: {date: date},
        success: function(data) {
            if (data.type == 'error') {
                alert(data.message)
            } else {
                upd_button(data.busy_time);
                tab = $('#date');
                next_tab(tab);
            }
        }
    });
}

var doctor_id, date, time, fio;

$("#back").click(function() {
    var tab = $('.active');
    $('.tab').addClass('hidden').removeClass('active');
    $(tab).prev().removeClass('hidden').addClass('active');
    if ($(tab).prev().attr('id') == 'home'){
        $(this).addClass('hidden')
    }
});


$("#next").click(function() {
    var tab = $('.active');
    switch ($(tab).attr('id')) {
        case 'date':
            doctor_id = $('#id_doctor').val();
            date = $('#datepicker').val();
            if (date==''){
                alert('Укажите дату');
                break;
            }
            upd_time(doctor_id, date);
            break;

        case 'time':
            time = $("#timeline .btn-primary").text();
            if (time == ''){
                alert('Укажите время');
                break;
            }
            next_tab(tab);
            break;

        case 'confirm':
            fio = $('#fio').val();
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            if (fio == ''){
                alert('Укажите ФИО');
                break;
            }
            $.ajax({
                url: "/doctor/" + doctor_id + "/",
                type: "POST",
                data: {date: date, time:time, fio: fio, csrfmiddlewaretoken: csrf},
                success: function(data) {
                    if (data.type == 'error') {
                        alert(data.message);
                    } else if (data.type == 'timeerror'){
                        alert(data.message);
                        upd_time(doctor_id, date);
                    } else if (data.type == 'success'){
                        alert('Вы успешно записанны на прием. \n' + data.message)
                        window.location = '/'
                    }
                }
            });
            break;

        default :
            next_tab(tab);
            $("#back").removeClass('hidden');
    }
});