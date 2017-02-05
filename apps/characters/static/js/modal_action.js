function getSum(total, num) {

    if (total) {
        total.count += num.count;
    }
    total = total || num;

    return total;
}

var data = [];
var ac_option = 'all';

function makeOption() {
    if (ac_option == 'all') {
        $("span.accuracy_option").text('全部');
        $("#classify-mothod").parent().addClass("hidden");
    } else {
        $("span.accuracy_option").text('指定个数');
        $("#classify-mothod").parent().removeClass("hidden");
        if (ac_option == 'random') {
            $("span.method_option").text('随机');
        } else {
            $("span.method_option").text('正序');
        }
    }
    var time_left = Math.round(charListContainer.total / 40);
    var diff = Math.round(time_left / 3)
    if (time_left == 0)
        time_left = 1
    if (diff == 0)
        diff = 1
    $("#estimate").text(time_left);
    $("#diff-scope").text(diff);
}
$(function() {
    $('#accuracyModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        modal.find('#accuracy_char').text(charListContainer.char);
        makeOption();
    });

    $('#detectModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        char_list.detecting = true;
        modal.find('#chart_char').text(charListContainer.char);
        char_list.fetch_detect_items()
    });

    $('#detectModal').on('hide.bs.modal', function(event) {
        char_list.detecting = false;
    });

    $("#classify-grade .dropdown-menu a").click(function() {
        var li = $(this);
        ac_option = li.data('value');
        makeOption();
    })

    $("#classify-mothod .dropdown-menu a").click(function() {
        var li = $(this);
        ac_option = li.data('value');
        makeOption();
    })

    $("button.cal").click(function() {
        var count = $(".modal_ac_input").val();
        var url = "/characters/classify?char=" + $('#accuracy_char').text();
        if (ac_option == 'all') {
            url = url + "&positive_sample_count=0&random_sample=1"
        } else if (ac_option == 'random' && count != 0) {
            url = url + "&positive_sample_count=" + count + "&random_sample=1";
        } else if (ac_option == 'postive' && count != 0) {
            url = url + "&positive_sample_count=" + count;
        } else {
            $(".modal_ac_input").addClass("error-input");
            return;
        }
        url += "&auto_apply=" + $("#auto-apply").prop("checked");
        $.ajax({
            url: url,
            method: 'get',
            cache: false,
            success: function(data) {

            },
            error: function(xhr, status, err) {
                console.log(err);
            }
        });
        charListContainer.startWaitingAnimate(charListContainer.char, parseInt($("#estimate").text()));
        $("#accuracyModal").modal('hide');
    });


});


function estimateCount() {
    var url = "/characters/accuracy_count";
    var data = {
        char: $("#mark_char").text(),
        min_value: $('.mark_input_l').val() || 100000,
        max_value: $('.mark_input_r').val() || 0,
    };
    $.ajax({
        url: url,
        method: 'post',
        cache: false,
        data: data,
        success: function(res) {
            $('.marking_count').text(res.count);
            if (res.count > 0) {
                $('.mark').removeClass('disabled');
            } else {
                $('.mark').addClass('disabled');
            }
        },
        error: function(xhr, status, err) {
            console.log(err);
        }
    });
}

$("input.mark_input").on('input', function() {
    estimateCount();
});


function getSum(total, num) {
    if (total) {
        total.count += num.count;
    }
    total = total || num;

    return total;
}

var data = [];
var chunk = 50;
var current_char;

function loadSvg() {
    d3.json('/api/datapoint?char=' + current_char, function(res) {
        data = [];
        var i, j, temparray;
        for (i = 0, j = res.length; i < j; i += chunk) {
            temparray = res.slice(i, i + chunk);
            data.push(temparray.reduce(getSum));
            // do whatever
        }


        data.map(function(d) { d.range_idx = d.range_idx / 1000;
            return d });
        new_data = []
        data.forEach(function(element, index, array) {
            if (index == 0) {
                new_data.push({ range_idx: data[index].range_idx, count: data[index].count + data[index + 1].count / 2 });
            } else if (index < data.length - 2) {
                new_data.push({ range_idx: data[index].range_idx, count: data[index].count / 2 + data[index + 1].count / 2 })
            } else if (index == data.length - 2) {
                new_data.push({ range_idx: data[index].range_idx, count: data[index].count / 2 + data[index + 1].count })
            }

        })
        data = new_data
        data.push({ range_idx: 1, count: 0 });

        $.getScript("/static/js/charts_app.js");
    });
}

function markActive() {
    $(".grade-btn").removeClass("active");
    var btn;
    if (chunk == 50) {
        btn = $("#l-btn")
    } else if (chunk == 20) {
        btn = $("#m-btn")
    } else if (chunk == 5) {
        btn = $("#h-btn")
    }
    btn.addClass('active');
}
$(function() {
    $('#classifyChartModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var recipient = current_char = button.data('char'); // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        modal.find('.modal-title').text('');
        modal.find('#chart_char').text(recipient);
        markActive();
        d3.selectAll("svg > *").remove();
        loadSvg();
        $("#gravity_checker").prop('checked', false);
    });

    $(".grade-btn").click(function() {
        var btn = $(this);
        chunk = btn.data('value');
        markActive();
        d3.selectAll("svg > *").remove();
        loadSvg();
    })

    $("#gravity_checker").click(function() {
        if ($(this).prop('checked')) {
            $(".gravity").removeClass("hidden");
        } else {
            $(".gravity").addClass("hidden");
        }
    })


});



$(function() {
    $('#markModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        $('.marking_count').text('0');
        $('.mark').addClass('disabled');
        modal.find('#mark_char').text(button.data('char'));
        estimateCount();
    });

    $("button.mark").click(function() {
        var count = parseInt($(".marking_count").text());
        if (count === 0) {
            return;
        }

        var url = "/characters/marked_by_accuracy";
        var data = {
            char: $("#mark_char").text(),
            min_value: $('.mark_input_l').val() || 100000,
            max_value: $('.mark_input_r').val() || 0,
        };
        $.ajax({
            url: url,
            method: 'post',
            cache: false,
            data: data,
            success: function(res) {},
            error: function(xhr, status, err) {
                console.log(err);
            }
        });
        $("#markModal").modal('hide');
    });
});


function markActive() {
    $(".grade-btn").removeClass("active");
    var btn;
    if (chunk == 50) {
        btn = $("#l-btn")
    } else if (chunk == 20) {
        btn = $("#m-btn")
    } else if (chunk == 5) {
        btn = $("#h-btn")
    }
    btn.addClass('active');
}
$(function() {

    $('#compareResultModal').on('show.bs.modal', function(event) {
        var modal = $(this);
        modal.find('#result_char').text(charListContainer.char);
        $('#resultArea').DataTable().ajax.url('/characters/last_task_result?char=' + charListContainer.char).load();
    });

    $(".more-task").click(function() {
        $('#resultArea').DataTable().ajax.url('/characters/more_task_result?char=' + charListContainer.char).load();
    });

    $("#resultArea").DataTable({
        "pagingType": "input",
        "info": false,
        "borderClasses": false,
        "bSortClasses": false,
        "bProcessing": true,
        "bDeferRender": true,
        "bProcessing": true,
        "bDeferRender": true,


        // Rows and column headers stored in a "data" object:
        "aaData": [],
        "columns": [
            { "data": "id" },
            { "data": "char" }, {
                "data": "url",
                mRender: function(data, type, full) {
                    return '<img src="' + data + '" style="zoom: 30%;border:1px dashed blue">';
                }
            },
            { "data": "origin_accuracy" },
            { "data": "new_accuracy" },
            { "data": "difference" }
        ],
        ajax: {
            url: '/characters/last_task_result?char=n',
            dataSrc: function(json) {
                for (var i = 0, ien = json.data.length; i < ien; i++) {
                    json.data[i].url = json.data[i].url;
                }
                return json.data;
            }
        },
        language: {
            emptyTable: "目前没有数据",
            search: "",
            processing: "载入数据中...请稍等",
            lengthMenu: " _MENU_ 结果/页",
            loadingRecords: "载入数据中...",
            paginate: {
                first: "<span class='fa fa-step-backward'></span>",
                previous: "❮",
                next: "❯",
                last: "<span class='fa fa-step-forward'></span>"
            }
        }
    });
});

var bingo_n = 0,
    fail_n = 0;

function muted(ele) {
    var sp = $(ele).find('span');
    if (sp.hasClass('fa-volume-up')) {
        sp.removeClass('fa-volume-up');
        sp.addClass('fa-volume-off');
        document.getElementById('bingo_audio').muted = true;
        document.getElementById('bingo_audio_2').muted = true;
        document.getElementById('fail_audio').muted = true;
        document.getElementById('fail_audio_2').muted = true;
        document.getElementById('dingding').muted = true;
        document.getElementById('clean').muted = true;
    } else {
        sp.removeClass('fa-volume-off');
        sp.addClass('fa-volume-up');
        document.getElementById('bingo_audio').muted = false;
        document.getElementById('bingo_audio_2').muted = false;
        document.getElementById('fail_audio').muted = false;
        document.getElementById('fail_audio_2').muted = false;
        document.getElementById('dingding').muted = false;
        document.getElementById('clean').muted = false;
    }
};

function play_bingo() {
    bingo_n++;
    if (bingo_n % 2 == 0)
        document.getElementById('bingo_audio').play();
    else
        document.getElementById('bingo_audio_2').play();
}

function play_fail() {
    fail_n++;
    if (fail_n % 2 == 0)
        document.getElementById('fail_audio').play();
    else
        document.getElementById('fail_audio_2').play();
}

function play_batch_mark() {
    document.getElementById('dingding').play();
}

function play_clean() {
    document.getElementById('clean').play();
}
