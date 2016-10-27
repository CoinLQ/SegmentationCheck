var charListContainer =
    {
        char: '',
        page_size: 50,
        page_number: 1,
        filter: '-10',//show all
        accuracy_base: NaN,
        accuracy_scope: 10,
        l_value: 0,
        r_value: 0.99,
        data: [],
        total: 0,
        timers: [],
        pagination: {},
        init: function() {
            this.initTable();
            this.initPageSize();
            this.initPagination();
            this.extras();
        },
        initPageSize: function() {
            var page_size = $.cookie('charindex_page_size');
            if(page_size== undefined){
                page_size = 50;
            }
            charListContainer.page_size = page_size;
        },
        initTable: function () {
            $("#char_index").DataTable({
              "pagingType": "input",
                "info":     false,
                "borderClasses": false,
                "bSortClasses": false,
                "bProcessing": true,
            "bDeferRender": true,
            "bProcessing": true,
            "bDeferRender": true,

            // Rows and column headers stored in a "data" object:
            "aaData": chars,
            language: {
                search:         "",
                lengthMenu:    " _MENU_ 字/页",
                loadingRecords: "载入数据中...",
                paginate: {
                    first:      "<span class='fa fa-step-backward'></span>",
                    previous:   "❮",
                    next:       "❯",
                    last:       "<span class='fa fa-step-forward'></span>"
                }
            }
            });
        },
        initPagination: function () {
            $('.pagitor').click(function(){
                if($(this).hasClass('first')){
                    page_number=1;
                }
                else if($(this).hasClass('previous')){
                    page_number= charListContainer.pagination.previous_page;
                }
                else if($(this).hasClass('next')){
                    page_number= charListContainer.pagination.next_page;
                }
                else if($(this).hasClass('last')){
                    page_number= charListContainer.pagination.total_pages;
                }
                if (!page_number) {
                    return;
                }
                charListContainer.page_number=page_number;
                charListContainer.fetchDataAndRender();
            });
        },
        extras: function(){
            $('.batch-check').click(function(){
                var btn = $(this);
                var is_correct=-2;
                if (btn.attr('id')=='err_btn'){
                    is_correct = -1;
                } else if (btn.attr('id')=='correct_btn') {
                    is_correct = 1;
                } else {
                    is_correct = 0;
                }
                charListContainer.handlerAction(is_correct,btn);
            });
            $('.accuracy_input').on('input',function(e){
                charListContainer.accuracy_base=parseFloat($(this).val());
            });
            var page_size = charListContainer.page_size;
            $("#LineControler button span:first-of-type").text(page_size);
            $('.accuracy_input').val('');

            $("#LineControler li a").click(function () {
                var page_size = $(this).text();
                charListContainer.page_size = page_size;
                $("#LineControler button span:first-of-type").text(page_size);
                $.cookie('charindex_page_size', page_size, { expires: 30 });
                charListContainer.page_number=1;
                charListContainer.fetchDataAndRender();
            })

            $("#find_scope .dropdown-menu a").click(function() {
                var li = $(this);
                li.parent().parent().parent().find("button span:first-of-type").text(li.text());
                charListContainer.filter=li.data('value');
                charListContainer.switchAndRender();
            })

            $("#accuracy_scope .dropdown-menu a").click(function() {
                var li = $(this);
                li.parent().parent().parent().find("button span:first-of-type").text(li.text());
                charListContainer.accuracy_scope=li.data('value');
                charListContainer.switchAndRender();
            })

            $('.accuracy_input').on('input',function(e){
                charListContainer.accuracy_base=parseFloat($(this).val());
            });

            //handler char select
            $('#char_index #char_index_tbody').on('click', 'tr', function(event) {
                $('tr').removeClass("selected");
                $(this).addClass("selected");
                charListContainer.hideWaitingAnimate();
                charListContainer.char = $("tr.selected td:eq(1)").text();
                charListContainer.l_value = parseFloat($("tr.selected td:eq(7)").text());
                charListContainer.r_value = parseFloat($("tr.selected td:eq(8)").text());
                charListContainer.recallWaitingAnimate();
                charListContainer.total = parseInt($("tr.selected td:eq(2)").text());
                $("#checkchar").text(charListContainer.char);
                $(".classifyChart").data('char', charListContainer.char);
                $(".accuracy_cal").data('char', charListContainer.char);
                $(".classifyChart").removeClass('hidden');
                $(".accuracy_cal").removeClass('hidden');
                charListContainer.page_number=1;
                //charListContainer.filter="-10";
                $('.radio-btn').removeClass('actived');
                $('.radio-btn.show-all').addClass('actived');
                charListContainer.fetchDataAndRender();
            })

            $('.radial-progress').click(function(evt) {
              evt.stopPropagation();
            });
            $("img.lazy").lazyload({
                effect : "fadeIn"
            });

            $('input.pagitor_input').keypress(function( event ){
                if(event.which == 13){
                    var page_number = parseInt($('.pagitor_input').val()) || 1;
                    charListContainer.page_number=page_number;
                    charListContainer.fetchDataAndRender();
                }
            });
        },
        handlerAction: function(is_correct,btn) {
            var arr =[];
            var charlist = $("#charBrowseArea").children();
            for (var i=0;i<charlist.length;i++){
                var tmp = charlist[i];

                if (! ($(tmp).hasClass('error-char') || $(tmp).hasClass('correct-char') )){
                    if(is_correct==-1){
                        $(tmp).addClass('error-char');
                    }
                    else if (is_correct==1){
                        $(tmp).addClass('correct-char');
                    }
                    arr.push(tmp.id);
                }
            }
            if (is_correct == 0)
            {
                arr = charlist.map(function() {return this.id}).get();
            }else {
                $(".char-image").removeClass("twinkling")
            }
            var data = {};
            var updateNum = arr.length;
            var e_num = $("#charBrowseArea .error-char").length;
            var c_num = $("#charBrowseArea .correct-char").length;
            data['csrfmiddlewaretoken'] = '{{ csrf_token }}';
            data['char'] = charListContainer.char;
            if ( is_correct == 1) {
                data['c_charArr'] = arr;
                data['c_updateNum'] = arr.length;
            } else if ( is_correct == -1) {
                data['e_charArr'] = arr;
                data['e_updateNum'] = arr.length;
            } else if ( is_correct == 0) {
                data['cl_charArr'] = arr;
                data['cl_updateNum'] = arr.length;
                data['e_num'] = e_num;
                data['c_num'] = c_num;
                $('.correct-char').map(function() {return $(this).removeClass('correct-char')});
                $('.error-char').map(function() {return $(this).removeClass('error-char')});
            }
            $.post('/characters/set_correct', data, function(res) {
               if(res['clear']=='ok'){
                $('.correct-char').map(function() {return $(this).removeClass('correct-char')});
                $('.error-char').map(function() {return $(this).removeClass('error-char')});
                $(".char-image").addClass("twinkling")
               }
            });
            play_batch_mark();
        },
        paginationRender: function(){
            var total_pages = this.pagination.total_pages;
            $('.pagitor_input').val(this.page_number);
            $('.pagitor_input').attr('max',total_pages);
            $('.total_page').text('/ '+total_pages);
        },
        startWaitingAnimate: function(char, least){
          var t = new TimeLeft(char, least);
          this.timers = this.timers.filter(function(el) {
              return el.char != char;
          });
          this.timers.push(t);
          t.Start();
        },
        recallWaitingAnimate: function(){
          var that = this;
          t = this.timers.filter(function(el) {
              return el.char == that.char && el.Enable == true;
          });
          if (t[0]) t[0].showCircle();
        },
        hideWaitingAnimate: function(){
          var that = this;
          t = this.timers.filter(function(el) {
              return el.char == that.char;
          });
          if (t[0]) t[0].hideCircle();
        },
        checkDict: function(){
            url = "http://hanzi.lqdzj.cn/hanzi-dict/search?param="
            url += charListContainer.char;
            var _open = window.open(url);
            if (_open == null || typeof(_open)=='undefined')
                console.log("Turn off your pop-up blocker!");
        },
        renderCharArea : function(){
            var area = "#charBrowseArea";
            var charArr = this.data;
            $(area).empty();
            txt =''
            $.each(charArr, function(i, field){
                txt = "<div id="+field.id+" class='flow "
                if (field.is_correct <0){
                    txt += "error-char o-error-char ";
                }
                else if (field.is_correct == 1){
                    txt += "correct-char o-correct-char ";
                } else {
                   txt += "twinkling ";
                }
                txt +="char-image' title='"+field.id+"'><img src='"+field.image_url +"' alt='加载中...' class='lazy'><span class='badge char-info'> "+ field.accuracy/1000+"</span> </div>"
                $(area).append(txt);
              });
        },
        binding_char_check : function (char){
            var selector = '#charBrowseArea .char-image'
            var _char = char;
            $(selector).click(function(){
                  var data = {'id': this.id};
                  play_bingo();
                  data['csrfmiddlewaretoken'] = '{{ csrf_token }}';
                  data['char'] = _char;
                  if ($(this).hasClass('error-char')) {
                    $(this).removeClass('error-char');
                    $(this).addClass('correct-char');
                    data['is_correct'] = 1;
                  } else {
                    $(this).removeClass('correct-char');
                    $(this).addClass('error-char');
                    data['is_correct'] = -1;
                  }
                $(this).removeClass("twinkling");
                $.post('/characters/set_correct', data);
            });
        },
        renderCharAndBind : function(){
            this.renderCharArea();
            this.binding_char_check(this.char);
        },
        switchAndRender: function() {
            var that = this;
            if (this.char == '') {
                return;
            }
            var query = "/api/character?page_size="+this.page_size
                +"&char="+this.char
                +"&page=1";//+this.page_number;
            var accuracy_cap, accuracy_floor;
            if (this.accuracy_base) {
                accuracy_cap = parseInt(this.accuracy_base*1000 + this.accuracy_scope);
                accuracy_floor = parseInt(this.accuracy_base*1000 - this.accuracy_scope);

                if (accuracy_cap <1 || this.accuracy_scope ==0) {
                    query += "&accuracy__lte="+accuracy_cap;
                }
                if (accuracy_floor>-1 || this.accuracy_scope ==0) {
                    query += "&accuracy__gte="+accuracy_floor;
                }

            }
            if(this.filter != -10){
                query += "&is_correct="+this.filter;
            }

            $.getJSON(query,function(result){
                that.data = result.models;
                var before_page_n = charListContainer.pagination.total_pages;
                that.pagination = result.pagination;
                page_n = $('.pagitor_input').val();
                var current_page = parseInt(page_n) || 0;
                var jump_page = Math.ceil((current_page/ before_page_n) * that.pagination.total_pages);
                if (current_page == 1) {
                    jump_page = 1;
                }
                charListContainer.page_number=jump_page;
                charListContainer.fetchDataAndRender();

            });
        },
        fetchDataAndRender: function(){
            var that = this;
            if (this.char == '') {
                return;
            }
            var query = "/api/character?page_size="+this.page_size
                +"&char="+this.char
                +"&page="+this.page_number;
            var accuracy_cap, accuracy_floor;
            if (this.accuracy_base) {
                accuracy_cap = parseInt(this.accuracy_base*1000 + this.accuracy_scope);
                accuracy_floor = parseInt(this.accuracy_base*1000 - this.accuracy_scope);

                if (accuracy_cap <1 || this.accuracy_scope ==0) {
                    query += "&accuracy__lte="+accuracy_cap;
                }
                if (accuracy_floor>-1 || this.accuracy_scope ==0) {
                    query += "&accuracy__gte="+accuracy_floor;
                }

            }
            if(this.filter != -10){
                query += "&is_correct="+this.filter;
            }

            $.getJSON(query,function(result){
                that.data = result.models;
                that.pagination = result.pagination;
                that.renderCharAndBind();
                that.paginationRender();
            });
        }
    }


$(function(){
    charListContainer.init();
});

