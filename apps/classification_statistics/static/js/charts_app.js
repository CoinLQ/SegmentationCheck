var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var tooltip = d3.select("body")
  .append("div")
  .style("position", "absolute")
  .style("z-index", "10000")
  .style("visibility", "hidden")
  .text("");

var dx =0, dy =0, vidisor=1;
if (chunk == 5) {
  dx = 3; dy = 6; vidisor =200;
} else if (chunk ==20) {
  dx = 7; dy = 31; vidisor =12;
} else if (chunk ==50) {
  dx = 16; dy = 16; vidisor = 20;
}

var x = d3.scaleBand().rangeRound([0, width]),
    y = d3.scaleLinear().rangeRound([height, 0]);
    //y = d3.scalePow().exponent(0.5).rangeRound([height, 0]);
    //y = d3.scaleLog(10).rangeRound([height, 0.1]);
var x2 = d3.scaleLinear().rangeRound([0, width]);
var y2 = d3.scaleLinear().rangeRound([height, 0]);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function convert_count( n ){
  return n;
  //return Math.sqrt(n);
  //return Math.log10(n);
}

function draw_gravity_line(val) {
  var diff = val/vidisor;
  g.append("line")
      .attr("transform", "translate("+ dy +",0)")
      .attr("stroke-width",2)
      .attr("x1", x2(val -diff))
      .attr("y1", "-10")
      .attr("x2", x2(val -diff))
      .attr("y2", "10")
      .attr("stroke", "#006600")
      .attr("class", "gravity")


  g.append("text")
        .attr("transform", "translate("+ dy +",0)")
        .attr("dx", x2(val-diff))
        .attr("dy", "-10")
        .text(val)
        .attr("text-anchor", "middle")
      .style("font-size", "0.6em")
//      .style("text-decoration", "underline")
      .attr("class", "gravity shadow");
  g.append("text")
        .attr("transform", "translate("+ dy +",0)")
        .attr("dx", x2(val-diff))
        .attr("dy", "-10")
        .text(val)
        .attr("text-anchor", "middle")
      .style("font-size", "0.6em")
//      .style("text-decoration", "underline")
      .attr("class", "gravity");

}

function draw_title_line(min, max) {
  var text = "区分度: " + (max-min);
  g.append("line")
      .attr("transform", "translate("+ dy +",0)")
      .attr("stroke-width",1.3)
      .attr("x1", x2(min- min/vidisor))
      .attr("y1", "-2")
      .attr("x2", x2(max-max/vidisor))
      .attr("y2", "-2")
      .attr("stroke", "#006600")
      .attr("marker-end", "url(#r-arrow)")
      .attr("marker-start", "url(#l-arrow)")
      .attr("class", "gravity");
  g.append("text")
        .attr("transform", "translate("+ dy +",0)")
        .attr("dx", x2((max-min)/2))
        .attr("dy", "-7")
        .text(text)
        .attr("text-anchor", "middle")
      .style("font-size", "1em")
//      .style("text-decoration", "underline")
      .attr("class", "shadow gravity");
   g.append("text")
        .attr("transform", "translate("+ dy +",0)")
        .attr("dx", x2((max-min)/2))
        .attr("dy", "-7")
        .text(text)
        .attr("text-anchor", "middle")
      .style("font-size", "1em")
//      .style("text-decoration", "underline")
      .attr("class", "gravity");
}

function _render_chart(data) {
  var max_y = d3.max(data, function(d) { return d.count; } );
  x.domain(data.map(function(d) { return d.range_idx; }));
  y.domain([0, max_y]);

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickValues(d3.ticks(0, 1, 20).map(function(n){
        return Math.round(n*100)/100;
      }) ).tickPadding(10));

  g.append("g")
      .attr("transform", "translate("+ dy +",0)")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).tickValues( y.ticks(5)))
  .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Frequency");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("y", height)
      .attr("height", 0)
      .attr("class", "bar")
      .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.count+ "("+d.range_idx+")");})
      .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .attr("x", function(d) { return x(d.range_idx)+dx; })
      .transition()
      .duration(1000)
      .attr("y", function(d) { return y(convert_count(d.count)); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(convert_count(d.count))});

  defs = svg.append("defs");
  defs.append("marker")
        .attr("id", "r-arrow")
        .attr("markerWidth",10)
        .attr("refX", 7)
        .attr("refY", 3)
        .attr("markerHeight", 10)
        .attr("orient", "auto")
        .attr("markerUnits","strokeWidth")
        .append("path")
          .attr("d", "M0,0 L0,6 L7,3 z")
          .attr("dy","-3")
          .attr("fill","#006600");

  defs.append("marker")
        .attr("id", "l-arrow")
        .attr("markerWidth",10)
        .attr("refX",0)
        .attr("refY", 3)
        .attr("markerHeight", 10)
        .attr("orient", "auto")
        .attr("markerUnits","strokeWidth")
        .append("path")
          .attr("d", "M7,0 L7,6 L0,3 z")
          .attr("dy","-3")
          .attr("fill","#006600");
  d3.selectAll("g.axis--x g.tick line").attr("y2", function(d){
      var a = $(this);
      if ( (10*d)%1 || (d==6) ) { //小数被1整除
        $(this).next().text("")
        return 6;
      }
      else
         return 10;
  });

  draw_gravity_line(charListContainer.r_value)
  draw_gravity_line(charListContainer.l_value)

  draw_title_line(charListContainer.l_value,charListContainer.r_value)
};

_render_chart(data);
$(".gravity").addClass("hidden");

