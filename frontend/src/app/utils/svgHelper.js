var SVG = require('app/utils/svg');

function drawSVG(dom_id, url ='http://od843aa4c.bkt.clouddn.com/hongwu/040.jpg') {

  var drawing = new SVG(dom_id).viewbox(0,0, 400, 680);
  var image = drawing.image(url)//+'?imageView2/2/w/1000/interlace/1/q/100');
  image.size(400, 680);
  var rect = drawing.rect(410,360).attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4).attr('fill', 'none').x(image.x()).y(image.y());
  var label = drawing.text('V0001P0002B1').attr('stroke', 'rgb(119, 68, 176)');
  var gridSize = 5;
  rect.draggable((function(x, y){
    return {
        x: x - x % gridSize,
        y: y - y % gridSize
    }})).on('dragend', function(e){
      label.move(e.target.x.baseVal.value-28,e.target.y.baseVal.value-28);
  });

  rect.selectize().resize().on('resizedone', function(e){
    console.log(e.target.x);
    rect.selectize().on('t', function(e){
      console.log("seleced");
    });
    label.move(e.target.x.baseVal.value-28,e.target.y.baseVal.value-28);
  });

  label.move(rect.x()-28,rect.y()-28);
  return drawing;
}

export default drawSVG;