function getImageDimension(el, onReady) {
    var src = typeof el.attr === 'function' ? el.attr('src') : el.src !== undefined ? el.src : el;

    var image = new Image();
    image.onload = function(){
        if(typeof(onReady) == 'function') {
            onReady({
                width: image.width,
                height: image.height
            });
        }
    };
    image.src = src;
}
function aysnc_drawSVG(dom_id, rect, url ='http://od843aa4c.bkt.clouddn.com/hongwu/040.jpg') {
  getImageDimension({src: url}, function(data){
      drawSVG(dom_id, url,rect, data.width, data.height);
  })
}
function drawSVG(dom_id, url, rect, width=0, height=0) {

  var drawing = window.drawing = new SVG(dom_id).viewbox(0,0, width, height).attr("overflow", "auto");
  var image = drawing.image(url)//+'?imageView2/2/w/1000/interlace/1/q/100');

  var rect1 = drawing.rect(rect[2],rect[3]).attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4).attr('fill', '#044B94').attr('fill-opacity','0.4').x(rect[0]).y(rect[1]);
  //var rect = drawing.rect(410,360).attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4).attr('fill', 'none').x(image.x()).y(image.y());
  //var label = drawing.text('V0001P0002B1').attr('stroke', 'rgb(119, 68, 176)');
  var gridSize = 5;
  // rect.draggable((function(x, y){
  //   return {
  //       x: x - x % gridSize,
  //       y: y - y % gridSize
  //   }})).on('dragend', function(e){
  //     label.move(e.target.x.baseVal.value-28,e.target.y.baseVal.value-28);
  // });

  // rect.selectize().resize().on('resizedone', function(e){
  //   console.log(e.target.x);
  //   rect.selectize().on('t', function(e){
  //     console.log("seleced");
  //   });
  //   label.move(e.target.x.baseVal.value-28,e.target.y.baseVal.value-28);
  // });

  //label.move(rect.x()-28,rect.y()-28);
  console.log(rect)
  draw_char_column(drawing, rect[0], rect[0]+rect[2], height)
  if (page_detail)
    drawSVGLines(drawing, height);
  return drawing;
}

function draw_char_column(drawing, left, right, height){
  var _column1 = drawing.line(
                right,
                0,
                right,
                height
                ).addClass('hidden column-line').attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4);
  var _column2 = drawing.line(
                left,
                0,
                left,
                height
                ).addClass('hidden column-line').attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4);
}

function draw_char_shown_column(drawing, left, right, height){
  var _column1 = drawing.line(
                right,
                0,
                right,
                height
                ).addClass('column-line').attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4);
  var _column2 = drawing.line(
                left,
                0,
                left,
                height
                ).addClass('column-line').attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4);
}

function drawLines(draw, left, right, char_lst) {
        char_lst.map(function (item, key) {
            var _row1 = draw.line(
                    left,
                    item.top,
                    right,
                    item.top).attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4).addClass('row-line');
            var _row2 = draw.line(
                left,
                item.bottom,
                right,
                item.bottom).attr('stroke', 'rgb(119, 68, 176)').attr('stroke-width', 4).addClass('row-line');
            // _row1.draggable({
            //     minX: 10,
            //     minY: 30,
            //     maxX: window.innerWidth-10,
            //     maxY: window.innerHeight-10
            //     })
            // .on('dragmove', function(e){
            //   this.y(e.detail.p.y);
            //   e.preventDefault();
            // })
            // .on('dragend', function(e){
            //   var key = 'char-' + field.line_no + '-' +item.char_no;
            //   console.log(key + ': y=' + this.y());
            //   this.addClass('highlight-' + item.char_no);
            // })
            // _row2.draggable({
            //     minX: 10,
            //     minY: 30,
            //     maxX: window.innerWidth-10,
            //     maxY: window.innerHeight-10
            //     })
            // .on('dragmove', function(e){
            //   this.y(e.detail.p.y);
            //   e.preventDefault();
            // })
            // .on('dragend', function(e){
            //   var key = 'char-' + field.line_no + '-' +item.char_no;
            //   console.log(key + ': y=' + this.y());
            //   this.addClass('highlight-'+ item.char_no);
            // })
        })
}

function highlightColumn(draw, objects, line_no) {
  objects[line_no-1].col[0].addClass("highlight-11");
  objects[line_no].col[0].addClass("highlight-11");
}

function cleanCutContent(drawing){
  SVG.utils.map(SVG.utils.filterSVGElements(drawing.node.childNodes).slice(2), function(node) {
        return node.remove()
      })
}
var lines;
function drawSVGLines(drawing, height){
  var page_id = $('#page_id').text()
  $.getJSON('/api/page/' + page_id + '/split_presets',function (res){
    lines = res.lines_hash
    for (var key in lines) {
      var left = lines[key]['border_l']
      var right = lines[key]['border_r']
      draw_char_shown_column(drawing, left, right, height)
      drawLines(drawing, left, right, lines[key]['char_lst'])
    }
  })

}