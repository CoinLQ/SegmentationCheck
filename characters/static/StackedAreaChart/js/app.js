var sort = [];
sortData();
//console.log(sort.length);
width = window.innerWidth,
    height = window.innerHeight,
    color = ['#B8D200', '#EB6EA5', '#C8D5BB', '#F4B3C2', '#F8B500', '#7EBEAB', '#BBC8E6'],
    svg = d3.select("svg")
    .attr('width', width)
    .attr('height', height);


var x = d3.scaleLinear().range([0, width]),
    y = d3.scaleLog().range([height, 0]);
//z = d3.scaleOrdinal(d3.schemeCategory10);

var xAxis = d3.axisTop(x),
    yAxis = d3.axisRight(y)
    .ticks(20, '.1s');

//var y0Axis = d3.axisRight()
//    .scale(y0)

var keys = ['mark_correct_by_man', 'mark_wrong_by_man', 'mark_correct_by_pc', 'mark_wrong_by_pc'];

var stack = d3.stack()
    .keys(keys)

var series = stack(sort);

var t;
var zoom = d3.zoom()
    .scaleExtent([1, 10])
    .translateExtent([[0, 0], [width, height]])
    .extent([0, 0], [width, height])
    .on('zoom', zoomed);

var area = d3.area()
    .curve(d3.curveMonotoneX)
    .x(function (d, i) {
        return x(d.data.index);
    })
    .y1(function (d) {
        var v = d[1];
        if (v == 0) v = 1e-1
        return y(v);
    })
    .y0(function (d) {
        var v = d[0];
        if (v == 0) v = 1e-1;
        return y(v);
    })

var chart = svg.append("g").attr('class', 'chart')

x.domain([0, sort.length]);
y.domain([1e-1, sort[0].total_mark_num]);

var layer = chart.selectAll(".layer")
    .data(series)
    .enter().append("g")
    .attr("class", "layer");

layer.append("path")
    .attr("class", "area")
    .style("fill", function (d, i) {
        return color[i];
    })
    .attr("d", area);

svg.append("g")
    .attr("class", "axis axis-x")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "axis axis-y")
    .call(yAxis);

var label = ['人工标定正确样本数', '人工标定错误样本数', '机器标定正确样本数', '机器标定错误样本数', '样本总数', '正确样本比率', '人工标定样本比率']
var ledgend = svg.append('g')
    .attr('class', 'ledgend')
    .attr("transform", "translate(" + (width - 320) + "," + 40 + ")")
    .selectAll('.li')
    .data(label.slice(0, 4))
    .enter()
    .append('g')
    .attr('class', 'li')

ledgend.append('rect')
    .attr('width', '20')
    .attr('height', '20')
    .attr('x', '0')
    .attr('y', function (d, i) {
        return i * 28;
    })
    .attr('rx', '8')
    .attr('ry', '8')
    .attr('fill', function (d, i) {
        return color[i];
    })
ledgend.append('text')
    .attr('class', 'label')
    .attr('x', '28')
    .attr('y', function (d, i) {
        return i * 28 + 16;
    })
    .attr('text-anchor', 'middle')
    .attr('text-anchor', 'start')
    .text(function (d) {
        return d
    })
    .append('tspan')
    .attr('class', 'value')

var d0 = 0,
    d1 = sort.length;

svg.call(zoom).transition().duration(1500)
    /*.call(zoom.transform, d3.zoomIdentity
        .scale(width / (x(d1) - x(d0)))
        .translate(-x(d0), 0));*/

var focus = svg.append('g')
    .attr('class', 'focus')
    .style('display', 'none')
    .attr('width', width)
    .attr('height', height)

focus.append('line')
    .attr('x1', 0)
    .attr('y1', 0)
    .attr('x2', 0)
    .attr('y2', height)

focus.append('line')
    .attr('x1', -width)
    .attr('y1', 0)
    .attr('x2', 0)
    .attr('y2', 0)

focus.append('circle')
    .attr('r', 8)

focus.append('text')
    .attr('class', 'char')
    .attr('dx', '-.5em')
    .attr('dy', '-.6em')

focus.append('text')
    .attr('y', '28')
    .attr('class', 'li')
    .attr('text-anchor', 'middle')
    .text(label[4])
    .append('tspan')
    .attr('class', 'value')

focus.append('text')
    .attr('y', '56')
    .attr('class', 'li')
    .attr('text-anchor', 'middle')
    .text(label[5])
    .append('tspan')
    .attr('class', 'value')

focus.append('text')
    .attr('y', '84')
    .attr('class', 'li')
    .attr('text-anchor', 'middle')
    .text(label[6])
    .append('tspan')
    .attr('class', 'value')

svg.append('rect')
    .attr('class', 'overlay')
    .attr("width", width)
    .attr("height", height)
    .on('mouseover', function () {
        focus.style('display', null)
        ledgend.selectAll('.value')
            .style('display', null)
    })
    .on('mouseout', function () {
        focus.style('display', 'none')
        ledgend.selectAll('.value')
            .style('display', 'none')
    })
    .on('mousemove', mouseMove)

d3.selectAll('.value')
    .attr('dx', '5')

function mouseMove() {
    focus.style('display', null)
    if (!t) {
        t = d3.zoomIdentity.translate(0, 0).scale(1);
    }
    var m = d3.mouse(this)[0],
        xt = t.rescaleX(x),
        yt = t.rescaleY(y);
    i = Math.round((m - t.x) / t.k / width * sort.length);

    svg.selectAll('.value')
        .text(function (d, j) {
            //console.log(keys[j]);
            return sort[i][keys[j]];
        })

    focus.selectAll('.value').text(function (d, j) {
        switch (j) {
        case 0:
            return sort[i].total_mark_num;
        case 1:
            return changeToPercent(sort[i].correct_mark_per);
        case 2:
            return changeToPercent(sort[i].man_mark_per);
        }
    })
    focus.select('.char').text(sort[i].char);
    focus.attr('transform', "translate(" + xt(i) + "," + yt(sort[i].total_mark_num) + ")")

}

/*var i = (x.invert(d3.mouse(this)[0])),
    d = sort[Math.ceil(i)];

focus.select('.rect') attr('transform', "translate(" + x(d.index) + "," + y(d.total_mark_num) + ")");
focus.select('text').text(d.char + ' ' + d.total_mark_num);*/


function zoomed() {
    focus.style('display', 'none');

    t = d3.event.transform;

    if (t.x > 0) t.x = 0;
    else if (t.x < width * (1 - t.k)) t.x = width * (1 - t.k);

    if (t.y > 0) t.y = 0;
    else if (t.y < height * (1 - t.k)) t.y = height * (1 - t.k);

    svg.select(".chart").attr("transform", t);
    //svg.select('.overlay').attr('transform', t);
    /*g.selectAll(".area").attr("d", area.x(function (d) {
        return xt(d.data.index);
    }));*/

    var xt = t.rescaleX(x),
        yt = t.rescaleY(y);
    svg.select(".axis-x").call(xAxis.scale(xt));
    svg.select('.axis-y').call(yAxis.scale(yt));
}

//function--------------------------------
function changeToPercent(num) {
    var result = (num * 100).toString(),
        index = result.indexOf(".");
    if (index == -1 || result.substr(index + 1).length <= 2) {
        return result + "%";
    }
    return result.substr(0, index + 3) + "%";
}

function sortData() {
    var k = Object.keys(data[0]);
    for (i in data) {
        var d = data[i];
        var sum = 0,
            corsum = 0,
            mansum = 0;

        //console.log(keys);
        for (j = 1; j < k.length; j++) {
            sum += d[k[j]];
            if (j == 2 || j == 3) {
                corsum += d[k[j]];
            }
            if (j == 2 || j == 4) {
                mansum += d[k[j]];
            }
        }
        d.total_mark_num = sum;
        d.correct_mark_per = corsum / sum;
        d.man_mark_per = mansum / sum;
        sort.push(d);
    }

    for (i = 1; i < sort.length; i++) {
        sort.sort(function (a, b) {
            return d3.descending(a.total_mark_num, b.total_mark_num);
        });
    }
    for (i in sort) sort[i].index = i;
}