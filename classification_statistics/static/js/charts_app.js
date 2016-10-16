var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
var tooltip = d3.select("body")
  .append("div")
  .style("position", "absolute")
  .style("z-index", "10")
  .style("visibility", "hidden")
  .text("");

var dx =0, dy =0;
if (chunk == 1) {
  dx = 3; dy = 7;
} else if (chunk ==4) {
  dx = 9; dy = 13;
} else if (chunk ==10) {
  dx = 21; dy = 25;
}

var x = d3.scaleBand().rangeRound([0, width]),
    y = d3.scaleLinear().rangeRound([height, 0]);
    //y = d3.scalePow().exponent(0.5).rangeRound([height, 0]);
    //y = d3.scaleLog(10).rangeRound([height, 0.1]);
var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function convert_count( n ){
  return n;
  //return Math.sqrt(n);
  //return Math.log10(n);
}



function _render_chart(data) {
  //var index = data.filter(function(d) { if (d.range_idx%10==0) return d; });
  //x.domain(index.map(function(d) { return d.range_idx%200; }));

  x.domain(data.map(function(d) { return d.range_idx; }));
  y.domain([0, d3.max(data, function(d) { return d.count; } )]);

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickValues([0, 0.2, 0.4, 0.6, 0.8]).tickPadding(10));

  g.append("g")
      .attr("transform", "translate("+ dy +",0)")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("分类值");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.range_idx)+dx; })
      .attr("y", function(d) { return y(convert_count(d.count)); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(convert_count(d.count))})
       .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.count);})
  .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
  .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

};
_render_chart(data);
