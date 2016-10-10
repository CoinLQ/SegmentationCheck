< script >
    //dealing with data
    function sortData() {
        var dataCopy = data.concat();
        var keys = Object.keys(data[0]);
        for (i in data) {
            var d = data[i];
            var sum = 0,
                corsum = 0;
            var sizeLev[5][];
            for (j = 1; j < keys.length; j++) {
                sum += d[i][keys[j]];
                if (j == 2 || j == 3) {
                    corsum += d[i][keys[j]];
                }
            }
            if (sum > 5000)
                Object.defineProperty(dataCopy[i], 'total_mark_num', {
                    value: sum,
                });
            Object.defineProperty(dataCopy[i], 'correct_mark_per', {
                value: sum == 0 ? 0 : corsum / sum,
            });

        }
    }
    /*dataCopy.sort(function (a, b) {
        return d3.descending(a.total_mark_num, b.total_mark_num);
    });
    console.log(dataCopy.length);
    var i = 1;
    while (dataCopy[dataCopy.length - i].total_mark_num < 5) {
        dataCopy.pop();
        i++;
    }
    console.log(dataCopy.length);*/
var dataContainer = new Object();
Object.defineProperty(dataContainer, '5w', {
    value: dataCopy,
}).defineProperties;


//D3 stage
var width = window.innerWidth,
    height = window.innerHeight,
    color = d3.scaleSequential(d3.interpolateSpectral),
    div = d3.select('body').append('div').style('position', 'relative');

var treemap = d3.treemap()
    .tile(d3.treemapBinary)
    .size([width, height])
    .round(true);

var root1 = d3.hierarchy(dataContainer).sum(function (d) {
    return d.total_mark_num;
});
var root2 = d3.hierarchy(dataContainer).sum(function (d) {
    return d.correct_mark_per;
});

/*var toggle = function () {
    var fn = arguments;
    var l = arguments.length;
    var i = 0;
    return function () {
        if (l <= i) i = 0;
        fn[i++]();
    }
}*/
treemap(root1);
treemap(root2);

/*        var changeDraw = toggle(
            function () {
                drawChart(root1)
            },
            function () {
                drawChart(root2)
            }
        );
        setInterval(changeDraw, 3000);
        changeDraw();*/

//function drawChart(root) {
var node = div.selectAll(".node")
    .data(root1.leaves())
    .enter().append("div")
    .attr("class", "node")
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
    })
    .style("background", function (d) {
        return color(1 - d.data.correct_mark_per);
    })
    .text(function (d) {
        return d.data.char + ' ' + formatFloat(d.data.correct_mark_per, 2);
    });
//}

function formatFloat(src, pos) {
    return Math.round(src * Math.pow(10, pos)) / Math.pow(10, pos);
} < /script>