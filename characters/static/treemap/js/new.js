//dealing with data
var size = new Array(6);
for (i = 0; i < size.length; i++) {
    size[i] = [];
}
sortData();
//console.log(size);

var level = new Object({
    children: [],
});
for (i = 0; i < size.length; i++) {
    level.children.push({});
    level.children[i]['level'] = i;
    level.children[i]['children'] = size[i];
}
level.children.reverse();

//-------------------------------------------
//D3 stage
var width = window.innerWidth,
    height = window.innerHeight,
    //color = ["#8A8E8D", "#5BC4CF", "#395EDE", "#8541CF", "#D640A3", "#DE5131"],
    stage = d3.select('#Stage').style('position', 'relative');

var treemap = d3.treemap()
    .tile(d3.treemapSquarify.ratio(1))
    .size([width, height])
    .padding(1)
    .round(true);

var root = d3.hierarchy(level).sum(function (d) {
    //return unifySize(d);
    return Math.pow(d.total_mark_num, .6);
});

treemap(root);
//console.log(root);

var node = stage.selectAll(".node")
    .data(root.leaves())
    .enter().append("div")
    .attr("class", "node")
    .call(position)
    .attr("data-per", function (d) {
        var p = d.data.correct_mark_per;
        if (p <= .5) {
            return 0;
        } else if (p <= .6) {
            return 1;
        } else if (p <= .7) {
            return 2;
        } else if (p <= .8) {
            return 3;
        } else if (p <= .9) {
            return 4;
        } else {
            return 5;
        }

    })
    .attr("data-level", function (d) {
        return d.parent.data.level;
    });

var filter = node.filter(function (d) {
        return d.parent.data.level > 1 ? true : false;
    })
    .call(insertData);
filter.append("div")
    .attr("class", "container")
    .append("div")
    .attr("class", "detail")
    .style("height", function (d) {
        return changeToPercent(1 - d.data.man_mark_per);
    });
filter.selectAll(".container")
    .append("span")
    .attr("class", "char")
    .text(function (d) {
        return d.data.char;
    });


//-------------------------------------------
//jQuery area
var style = "";
$(document).ready(function () {
    $('body').height($(window).innerHeight());
});
$('.node:not([data-level="1"]').click(function () {
    if (!$(this).hasClass('lightbox')) {
        style = $(this).attr('style');
        $(this).removeAttr('style').addClass('lightbox')
        $(this).find('.container').append('<button class="close button hideText"><span class="fa fa-times"></span><span class="text">关闭</span></button>')
        $('.close').bind('click', function (event) {
            $('.lightbox').removeClass('lightbox').attr('style', style).find('svg,.close').remove();
            $('#Wrap').hide();
            event.stopPropagation();
        });
        $('#Wrap').show();
        drawChat(this);
    }
})

$('#LedgendBtn').click(function () {
    if ($('.ledgend').css('display') == 'none') {
        $('.ledgend').show();
        var demo = $('[data-level="5"]:nth-of-type(2)').css('z-index', '1000');
        demo[0].focus();
        demo.find('.detail').addClass('demo')
        var left = parseInt(demo.css('left'));
        var width = parseInt(demo.width());
        $('.ledgend ul').css('left', (left + width + 16) + 'px');
        $('#Wrap').show();
    } else {
        $('.ledgend').hide();
        $('#Wrap').show();
    }
    $('#Wrap').click(function () {
        if ($('.ledgend').css('display') == 'block') {
            $('.ledgend').hide();
            $('[data-level="5"]:nth-of-type(2)').removeClass('z-index').blur().find('.detail').removeClass('demo');
            $('#Wrap').hide();
        }
    })
})



/*var svg = d3.select(this).append('svg').attr('width', width).attr('height', height).append('g').attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');*/

//});
/*$(document).ready(function () {
    $('[data-toggle="popover"]').popover({
        container: 'body',
        placement: 'auto right',
        trigger: 'click focus',
    });
});
$('[data-toggle="popover"]').hoverIntent(function () {
    $(this).popover('show');
}, function () {
    $(this).popover('hide');
});*/

//-------------------------------------------
//functions
function adjustLabel(datum, f) {
    for (i = 1; i < 5; i++) {
        if (datum[i - 1].value / datum[4].value < f) {
            if (datum[checkI(i - 1) - 1].value / datum[4].value < f) {
                if (datum[checkI(i + 1) - 1].value / datum[4].value < f) {
                    d3.selectAll('text').filter(':nth-of-type(' + checkI(i - 1) + ')').attr('dx', '2').attr('dy', '-4');
                    d3.selectAll('textPath').filter(':nth-of-type(' + checkI(i) + ')').attr('dx', '2').attr('dy', '-44');
                    d3.selectAll('textPath').filter(':nth-of-type(' + checkI(i + 1) + ')').attr('dx', '2').attr('dy', '-64');
                    break;
                } else {
                    d3.selectAll('text').filter(':nth-of-type(' + checkI(i - 1) + ')').attr('dx', '2').attr('dy', '-4');
                    d3.selectAll('text').filter(':nth-of-type(' + checkI(i) + ')').attr('dx', '2').attr('dy', '-44');
                    break;
                }
            }
            d3.selectAll('text').filter(':nth-of-type(' + checkI(i) + ')').attr('dx', '2').attr('dy', '24');
        }
    }

    function checkI(i) {
        return i == 0 || i == 5 ? 4 : i;
    }
}


function drawTextPath(pieChat) {
    var angle = d3.scaleLinear()
        .domain([0, 29])
        .range([0, 2.4 * Math.PI])

    var line = d3.radialLine()
        .angle(function (d, i) {
            return angle(i);
        })
        .radius(170)
        .curve(d3.curveCatmullRom.alpha(0.5))

    var textPath = pieChat.append('g')
        .append('path')
        .datum(d3.range(30))
        .attr('id', 'TextPath')
        .attr('d', line)
}

function getBaseLog(x, y) {
    return Math.log(y) / Math.log(x);
}

function drawChat(selection) {
    var radius = 240,
        color = ['#AACF53', '#A8BF93', '#C099A0', '#EB6EA5', '#7EBEAB', '#F6AD49', '#BBC8E6'];
    var svg = d3.select(selection).insert('svg', 'first-child').attr('width', 640).attr('height', 600);
    var arc = d3.arc().outerRadius(radius - 10).innerRadius(radius - 70).padAngle(0.006).cornerRadius(4);
    var pie = d3.pie().sort(null).value(function (d) {
        return d.value
    });

    var datum = [{
        label: "人工标对"
    }, {
        label: "机器标对"
    }, {
        label: "机器标错"
    }, {
        label: "人工标错"
    }, {
        label: "总样本数"
    }, {
        label: "正确样本比重"
    }, {
        label: "人工标注比重"
    }]
    var v = $(selection).attr('data-content');
    for (i = 0; i < 7; i++) {
        datum[i].value = v.substring(0, v.indexOf(';'))
        v = v.substring(v.indexOf(';') + 1)
    }

    var gaugeChat = svg.append('g')
        .attr('id', 'Fillgauge')

    var cfg = liquidFillGaugeDefaultSettings();
    cfg.waveHeight = .1;
    cfg.minValue = 0;
    cfg.maxValue = 1;
    cfg.waveColor = color[6];
    cfg.waveAnimateTime = 1000;

    var fillgauge = loadLiquidFillGauge("Fillgauge", datum[6].value, cfg);

    var pieChat = svg.append('g')
        .attr('id', 'PieChat')
        .attr('width', '600')
        .attr('height', '600')
        .attr('transform', 'translate(' + 320 +
            ',' + 280 + ')');
    var path = pieChat.selectAll('path')
        .data(pie(datum.slice(0, 4)))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', function (d, i) {
            return color[i];
        })

    drawTextPath(pieChat);
    var text = pieChat.select('g')
        .selectAll(".label")
        .data(datum.slice(0, 4))
        .enter()
        .append('text')
        .attr('class', 'label')
        .attr('dx', 4)
        .attr('dy', -24)
        .append('textPath')
        .attr('xlink:href', function () {
            return '#TextPath'
        })
        .attr("startOffset", function (d, i) {
            if (datum[i].value == 0) {
                return '200%';
            } else {
                var s = 0;
                for (j = 0; j < i; j++) {
                    s += parseInt(datum[j].value);
                }
                return changeToPercent(s / datum[4].value / 1.2);
            }

        })
        .style("text-anchor", "start")
        .text(function (d) {
            return d.label;
        })
        .append('tspan')
        .attr('class', 'value')
        .text(function (d) {
            return d.value;
        })

    adjustLabel(datum, 0.08);

    var label = svg.append('g');

    label.append('text')
        .attr('class', 'label')
        .attr('x', '320')
        .attr('y', '320')
        .attr('text-anchor', 'middle')
        .text('样本总数')
    label.append('text')
        .attr('class', 'value')
        .attr('x', '320')
        .attr('y', '340')
        .attr('text-anchor', 'middle')
        .text(function (d) {
            return datum[4].value;
        })
    label.append('text')
        .attr('class', 'label')
        .attr('x', '320')
        .attr('y', '400')
        .attr('text-anchor', 'middle')
        .text('人工审核比率')
    label.append('text')
        .attr('class', 'value')
        .attr('x', '320')
        .attr('y', '420')
        .attr('text-anchor', 'middle')
        .text(function (d) {
            return changeToPercent(datum[6].value);
        })
}

function formatNumber(n) {
    s = n.toString();
    var i = parseInt(s.length / 3);
    var newS = '';
    for (j = 0; j < i; j++) {
        newS += substr(-3 * j - 1, 3);
    }

}

function insertData(selection) {
    selection
        .attr("data-toggle", "popover")
        .attr("data-content", function (d) {
            return d.data.mark_correct_by_man + ';' +
                d.data.mark_correct_by_pc + ';' +
                d.data.mark_wrong_by_pc + ';' +
                d.data.mark_wrong_by_man + ';' + d.data.total_mark_num + ';' + d.data.correct_mark_per.toString().substr(0, 6) + ';' + d.data.man_mark_per.toString().substr(0, 6) + ';';
        });
}

function changeToPercent(num) {
    var result = (num * 100).toString(),
        index = result.indexOf(".");
    if (index == -1 || result.substr(index + 1).length <= 2) {
        return result + "%";
    }
    return result.substr(0, index + 3) + "%";
}

function position(selection) {
    selection
        .style("left", function (d) {
            return d.x0 + "px";
        })
        .style("top", function (d) {
            return d.y0 + "px";
        })
        .style("width", function (d) {
            return d.x1 - d.x0 + "px";
        })
        .style("height", function (d) {
            return d.y1 - d.y0 + "px";
        });
}

function colorize(selection) {
    selection
        .style("background", function (d) {
            var p = d.data.correct_mark_per;
            if (!p < .5) {
                if (p < .6) {
                    return color[1];
                } else if (p < .7) {
                    return color[2];
                } else if (p < .8) {
                    return color[3];
                } else if (p < .9) {
                    return color[4];
                } else {
                    return color[5];
                }
            } else {
                return color[0];
            }
        });
}

function unifySize(d) {
    var n = d.total_mark_num;
    if (d.unique) {
        return n;
    } else {
        if (n > 50000) {
            return 225000;
        } else if (n > 5000) {
            return 22500;
        } else if (n > 500) {
            return 2250;
        } else if (n > 50) {
            return 225;
        } else if (n > 5) {
            return 22.5;
        }
    }
}

function sortData() {
    var keys = Object.keys(data[0]);
    size[0][0] = {
        char: 0,
        mark_wrong_by_pc: 0,
        mark_correct_by_man: 0,
        mark_correct_by_pc: 0,
        mark_wrong_by_man: 0,
        total_mark_num: 0,
        correct_mark_per: 0,
        man_mark_per: 0,
        unique: true,
    };

    for (i in data) {
        var d = data[i];
        var sum = 0,
            corsum = 0,
            mansum = 0;

        //console.log(keys);
        for (j = 1; j < keys.length; j++) {
            sum += d[keys[j]];
            if (j == 2 || j == 3) {
                corsum += d[keys[j]];
            }
            if (j == 2 || j == 4) {
                mansum += d[keys[j]];
            }
        }

        if (sum > 0) {
            if (sum < 5) {
                size[0][0].char_num++;
                size[0][0].mark_wrong_by_pc += d.mark_wrong_by_pc;
                size[0][0].mark_correct_by_man += d.mark_correct_by_man;
                size[0][0].mark_correct_by_pc += d.mark_correct_by_pc;
                size[0][0].mark_wrong_by_man += d.mark_wrong_by_man;
                size[0][0].total_mark_num += sum;
            } else {
                d.total_mark_num = sum;
                d.correct_mark_per = corsum / sum;
                d.man_mark_per = mansum / sum;

                if (sum < 50) {
                    size[1].push(d);
                    //console.log(d);
                } else if (sum < 500) {
                    size[2].push(d);
                } else if (sum < 5000) {
                    size[3].push(d);
                } else if (sum < 50000) {
                    size[4].push(d);
                } else {
                    size[5].push(d);
                }
            }
        }

    }
    size[0][0].correct_mark_per = (size[0][0].mark_correct_by_man + size[0][0].mark_correct_by_pc) / size[0][0].total_mark_num;
    size[0][0].man_mark_per = (size[0][0].mark_correct_by_man + size[0][0].mark_wrong_by_man) / size[0][0].total_mark_num;

    for (i = 1; i < size.length; i++)
        size[i].sort(function (a, b) {
            return d3.descending(a.total_mark_num, b.total_mark_num);
        });
}