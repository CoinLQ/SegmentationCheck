$(function() {
    var page_size = $.cookie('charcheck_page_size');
    if (page_size == 30) {
        $.cookie('charcheck_page_size', 20);
        page_size = 20;
    }
    $("#LineControler button span:first-of-type").text(page_size);
})
$("#LineControler li a").click(function() {
    var page_size = $(this).text();
    $("#LineControler button span:first-of-type").text($(this).text());
    $.cookie('charcheck_page_size', page_size, { expires: 20 });
    render_char_area();
})

function render_char_area() {
    var _char = $('#checkchar').text();
    var page_size = $.cookie('charcheck_page_size');
    if (page_size == null) {
        page_size = 20;
        $.cookie('charcheck_page_size', page_size, { expires: 20 });
    }
    $.getJSON("/api/character?page_size=" + page_size + "&is_correct=0&char=" + _char, function(result) {
        if (result.models.length == 0) {
            // location.reload();
        }
        renderCharArea("#charlistArea", result.models);
        binding_char_check('#charlistArea');
        $('.progress .progress-bar').progressbar({ display_text: 'center', use_percentage: false });
        $('.progress .progress-bar').progressbar({
            update: function(current_percentage, $this) {
                $this.css('background-color', 'rgb(175,' + Math.round(current_percentage / 100 * 255) + ', 120)');
            }
        });
    });
}
$(render_char_area())

function binding_char_check(area) {
    var selector = area + ' .char-image';
    $(selector).click(function() {
        var data = { 'id': this.id };
        data['char'] = $('#checkchar').text();
        if (!$(this).hasClass('error-char')) {
            $(this).removeClass('correct-char');
            $(this).addClass('error-char');
        } else {
            $(this).removeClass('error-char');
            $(this).addClass('correct-char');
        }
        validButton();
    });
    $(selector).dblclick(function() {
        var data = { 'id': this.id };
        data['char'] = $('#checkchar').text();
        if ($(this).hasClass('error-char')) {
            $(this).removeClass('error-char');
            $(this).addClass('correct-char');
        }
        validButton();
    });

}

function renderCharArea(area, charArr) {
    $(area).empty();
    var char_div = '';
    $.each(charArr, function(i, field) {
        char_div = "<div id=" + field.id + " class='flow char-image' title='" + field.id + "'><img src='" + field.image_url + "' alt='加载中'></div>"
        $(area).append(char_div);
    });
}
$(function() {
    $('.batch-check-correct').click(handler);
    $('.batch-check-error').click(handler_default_error);
    $('.step-next').click(step);
})

function validButton() {
    if ($('.char-image').length == ($('.correct-char').length + $('.error-char').length)) {
        $('.step-next').removeClass('disabled');
        $('.step-next .fa').text('下一步');
        $('.step-next .tooltiptext').text('继续后面的任务');
    }
}

function step() {
    var correct_arr = $('.correct-char').map(function() {
        return this.id }).get();
    var error_arr = $('.error-char').map(function() {
        return this.id }).get();
    if (correct_arr.length + error_arr.length == 0) {
        return;
    }
    validButton();
    if ($('.char-image').length != (correct_arr.length + error_arr.length)) {
        return;
    }
    var data = { 'e_charArr': error_arr };
    data['char'] = $('#checkchar').text();
    data['e_updateNum'] = error_arr.length;
    data['c_charArr'] = correct_arr;
    data['c_updateNum'] = correct_arr.length;
    $('.step-next').addClass('btn-warning');
    $('.step-next').off('click');
    $.post('/characters/set_correct', data, function() {
        $('.step-next').removeClass('btn-warning');
        location.reload();
    });
}

function handler() {
    $('.char-image').toArray().forEach(function(item, i) {
        if (!$(item).hasClass('correct-char') && !$(item).hasClass('error-char')) {
            $(item).addClass('correct-char');
        }
    })
    validButton();
}

function handler_default_error() {

    $('.char-image').toArray().forEach(function(item, i) {
        if (!$(item).hasClass('correct-char') && !$(item).hasClass('error-char')) {
            $(item).addClass('error-char');
        }
    })
    validButton();
}
