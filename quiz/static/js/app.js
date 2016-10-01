var batch_id;
function renderCharArea(area,charArr){
    $(area).empty();
    var char_div = '';
    $.each(charArr, function(i, field){
        char_div = "<div id="+field.id+" class='flow char-image' title='"+field.id+"'><img src='"+field.image_url+"' alt='加载中'></div>"
        $(area).append(char_div);
      });
}
function binding_char_check(area){
    var selector = area + ' .char-image'
    $(selector).click(function(){
          var data = {'id': this.id};
          data['csrfmiddlewaretoken'] = '{{ csrf_token }}';
          if ($(this).hasClass('error-char')) {
            $(this).removeClass('error-char');
            $(this).addClass('correct-char');
            data['is_correct'] = 1;
          } else {
            $(this).removeClass('correct-char');
            $(this).addClass('error-char');
            data['is_correct'] = -1;
          }
          $.post('/quiz/'+batch_id+'/set_correct', data );
    });
}


function handler() {
    var arr =[];
    var charlist = $("#charlistArea").children();
    for (var i=0;i<charlist.length;i++){
        var tmp = charlist[i];
        arr.push(tmp.id);
    }
    var data = {'charArr':arr};
    data['csrfmiddlewaretoken'] = '{{ csrf_token }}';
    $('.batch-check').addClass('btn-warning');
    $('.batch-check').off('click');
    setTimeout(function(){
      $('.batch-check').removeClass('btn-warning');
      $('.batch-check').click(handler)}, 2000);
    $.post('/quiz/'+batch_id+'/set_correct', data, function(status) {
        if(status['score']>=0){
            $('#'+status['status']).removeClass('hidden');
            $('#'+status['status']+'_score').text(status['score']*100+'%');
            $('#myModal').modal({
                backdrop: 'static',
                keyboard: false,
                show: true
            });
        }
        else {
            $.getJSON("/quiz/"+batch_id+"/characters",function(result){
                var char = result[0].char;
                $('#checkchar').text(char);
                renderCharArea("#charlistArea",result);
                binding_char_check('#charlistArea');
            });
        }
    });
}
