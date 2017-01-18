var char_list = new Vue({
    el: '#charListArea',
    data: {
        selection: 0,
        detect_selection: 0,
        detect_type: 0,
        detect_page: 1,
        detect_pagination: {},
        item_id: '',
        item_url: '',
        item_direct: '',
        items: charListContainer.data,
        detect_items: [],
        degree: 0,
        final_degree: 0,
        detecting: false,
        menu_style: {
            top: 0,
            left: 0,
            display: 'none'
        },
        detect_menu_style:{
            top: 0,
            left: 0,
            display: 'none'
        },
        predict_results: []
    },

    csrf_token: '{{ csrf_token }}',
    methods: {
        gen_cls: function(item) {
            var class_name;
            if (item.is_correct == 1) {
                cls_name = 'correct-char flip-inx'
            } else if (item.is_correct == -1) {
                cls_name = 'error-char flip-inx'
            } else {
                cls_name = 'twinkling'
            }
            // if (this.items.indexOf(item) == this.selection)
            //     cls_name = cls_name.replace(/flip-inx/, '')
            return cls_name;
        },
        gen_detect_cls:  function(item) {
            var class_name;
            if (item.is_correct == 1) {
               cls_name = !item.checked ? 'correct-char flip-inx' : 'error-char flip-inx'
            } else if (item.is_correct == -1) {
                cls_name = !item.checked ? 'error-char flip-inx' : 'correct-char flip-inx'
            } else {
                cls_name = !item.checked ? 'twinkling' : 'correct-char flip-inx'
            }
            return cls_name;
        },
        goto_detail: function(is_detect=false){
            if (is_detect){
                var item = this.detect_items[this.detect_selection]
            } else {
                var item = this.items[this.selection]
            }

            url = "/characters/" + item.id;
            var _open = window.open(url);
        },
        intelli_recog: function(is_detect=false){
            if (is_detect){
                var item = this.detect_items[this.detect_selection]
            } else {
                var item = this.items[this.selection]
            }
            this.item_url = item.image_url
            this.item_id = item.id
            char_list.predict_results = []
            this.menu_style = {
                display: 'none'
            }
             $("#recogModal").modal('show')
            var url = '/api/character/' + this.items[this.selection].id + '/recog'
            $.getJSON(url, function(ret){
                char_list.predict_results = ret['result']

            }).error(function(jqXHR, textStatus, errorThrown){
                char_list.predict_results = [textStatus]
            });
            document.removeEventListener('click', char_list._onContextMenuClick)
        },
        showPanel: function(index) {
            if (this.selection != index) {
                this.ClickedOutside();
            }
            this.selection = index;
            const item = this.items[index];
            if (this.items[index].show)
                return;
            this.items.$set(index, {
                show: true,
                id: item.id,
                image_url: item.image_url,
                cls_name: item.cls_name,
                accuracy: item.accuracy,
                char: item.char,
                is_correct: item.is_correct
            })
            event.preventDefault()
            event.stopPropagation()
        },
        ClickedOutside: function() {
            const item = this.items[this.selection];
            if (!item.show)
                return;
            this.items.$set(this.selection, {
                show: false,
                id: item.id,
                image_url: item.image_url,
                cls_name: item.cls_name,
                accuracy: item.accuracy,
                char: item.char,
                is_correct: item.is_correct
            })
        },
        mark_it: function(item, is_correct) {

            var data = {
                id: item.id,
                is_correct: is_correct,
                char: item.char,
            };
            if (item.is_correct != is_correct) {
                $.post('/characters/set_correct', data);
                if (is_correct == 1) {
                    play_bingo();
                } else {
                    play_fail();
                }

                this.items.$set(this.items.indexOf(item), {
                    show: false,
                    id: item.id,
                    image_url: item.image_url,
                    cls_name: item.cls_name,
                    accuracy: item.accuracy,
                    char: item.char,
                    is_correct: is_correct
                })
            }
        },
        batchMark: function(is_correct) {
            this.items = _.map(this.items, function(item) {
                // is_correct === 0 意义在于批量清除
                if (item.is_correct === 0 || is_correct === 0) {
                    item.is_correct = is_correct
                }
                return item;
            });
        },
        handleContextmenu: function(item, e) {
            document.removeEventListener('click', char_list._onContextMenuClick)
            this.menu_style = {
                top: e.pageY - window.scrollY + 'px',
                left: e.pageX + 'px',
                display: 'block'
            }
            this.selection = this.items.indexOf(item)
            setTimeout(function() { document.addEventListener('click', char_list._onContextMenuClick) }, 200)
        },
        _onContextMenuClick: function(e) {
            e.stopPropagation()
            if ($('.ctx-menu-container').get(0) !== e.target) {
                char_list.menu_style = {
                    display: 'none'
                }
            }
            document.removeEventListener('click', char_list._onContextMenuClick)
        },
        handleDetectContextmenu: function(item, e) {
            document.removeEventListener('click', char_list._onDetectContextMenuClick)
            this.detect_menu_style = {
                top: e.pageY - window.scrollY - 30 + 'px',
                left: e.target.parentNode.parentNode.offsetLeft+ 50 + 'px',
                display: 'block'
            }
            this.detect_selection = this.detect_items.indexOf(item)
            setTimeout(function() { document.addEventListener('click', char_list._onDetectContextMenuClick) }, 200)
        },
        _onDetectContextMenuClick: function(e) {
            e.stopPropagation()
            if ($('.ctx-detect-menu-container').get(0) !== e.target) {
                char_list.detect_menu_style = {
                    display: 'none'
                }
            }
            document.removeEventListener('click', char_list._onDetectContextMenuClick)
        },
        cut_image_modal: function(is_detect=false) {
            if (is_detect){
                var item = this.detect_items[this.detect_selection]
            } else {
                var item = this.items[this.selection]
            }
            this.item_url = item.image_url
            this.item_id = item.id
            $("#cutImageModal").modal('show')
            this.menu_style = {
                display: 'none'
            }
            this.detect_menu_style = {
                display: 'none'
            }
            document.removeEventListener('click', char_list._onContextMenuClick)
            document.removeEventListener('click', char_list._onDetectContextMenuClick)
        },
        cut_detail_modal: function(direct) {
            this.item_direct = direct
            $("#cutDetailModal").modal('show')
        },
        selection_class: function(idx) {
            if (this.detect_type == idx){
               return this.detect_type == 0 ? 'btn-danger' : 'btn-success'
            }
            return 'btn-default'
        },
        has_correct: function(item) {
            return item.is_correct != 1
        },
        detect_class: function(item) {
            if (!item.checked) {
                return this.has_correct(item) ? 'detect-icon-green' : 'detect-icon'
            }
            return this.has_correct(item) ? 'detect-icon' : 'detect-icon-green'
        },
        toggel_check: function(item) {
            item.checked = !item.checked
            this.items.$set(this.detect_items.indexOf(item), item)
        },
        switch_type: function(idx) {
          this.detect_type = idx
          this.fetch_detect_items()
        },
        fetch_detect_items: function(page=1) {
            var idx = this.detect_type
            var url = '/api/character?char=' + charListContainer.char
            if (idx==0){
                url += '&is_correct=-1&is_same=1'
            } else if (idx==1){
                url += '&is_correct=1&is_same=-1'
            } else if (idx==2){
                url += '&is_correct=0&is_same=1'
            }
            url += '&page_size=50'
            url += '&page=' + page
            $.getJSON(url, function(ret){
                char_list.detect_items = _.map(ret.models, function(item) {
                        item['checked'] = true;
                        return item;
                    });
                char_list.detect_pagination = ret.pagination
            }).error(function(jqXHR, textStatus, errorThrown){
                char_list.detect_items = []
            });
        },
        go_first: function() {
            this.fetch_detect_items(1)
        },
        go_last: function() {
            this.fetch_detect_items(this.detect_pagination.total_pages)
        },
        go_previous: function() {
            if (this.detect_pagination.previous_page)
                this.fetch_detect_items(this.detect_pagination.previous_page)
        },
        go_next: function() {
            if (this.detect_pagination.next_page)
                this.fetch_detect_items(this.detect_pagination.next_page)
        },
        detect_batch_toggle: function() {
            char_list.detect_items = _.map(char_list.detect_items, function(item) {
                        item['checked'] = !item['checked'];
                        return item;
                    });
        },
        submit_recog_detect: function(){
            var checked_ids = _.filter(char_list.detect_items, function(item) {
                        if (item['checked']) return item;
                    }).map(function(it){ return it.id });;
            var unchecked_ids = _.filter(char_list.detect_items, function(item) {
                        if (!item['checked']) return item;
                    }).map(function(it){ return it.id });
            var data = {type: this.detect_type, checked_ids: checked_ids, unchecked_ids: unchecked_ids, char: charListContainer.char}
            $.ajax({
              url: '/api/character/filter-mark',
              method: 'post',
              dataType: 'json',
              contentType:"application/json; charset=utf-8",
              data: JSON.stringify(data),
              cache: false,
              success: function(data) {
                char_list.detect_items = []
              }.bind(this),
              error: function(xhr, status, err) {
                console.log('error');
                console.error( err.toString());
              }.bind(this)
            });
        }
    }
});

$(function() {
    $('#cutImageModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget) // Button that triggered
        var modal = $(this)
        modal.find('.modal-title').text('字符切分')
        modal.find('.cut_image_char').text(charListContainer.char)
    });

    $('#recogModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget) // Button that triggered
        var modal = $(this)
        modal.find('.modal-title').text('机器识别')
        modal.find('.cut_image_char').text(charListContainer.char)
    });

    $('#cutDetailModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget) // Button that triggered
        var modal = $(this)
        modal.find('.modal-title').text('字符选择')
        modal.find('.cut_image_char').text(charListContainer.char)
        cut_detail.more_items = []
        $.get('/api/character/' + char_list.item_id + '/direct/' + char_list.item_direct + '/cut', function(res) {
            if (res.direct !== char_list.item_direct) alert(res.direct)
            var _items = _.map(res.cut_list, function(item) {
                if (char_list.item_direct.indexOf('t') != -1) {
                    item.display_degree = item.degree * -1
                } else {
                    item.display_degree = item.degree
                }
                return item;
            });
            if (char_list.item_direct.indexOf('b') != -1) {
                _items = _.reverse(_items)
            }
            //_.reverse()
            cut_detail.cut_items = _items
        }, 'json')
    });

});

var cut_detail = new Vue({
    el: '#cutDetailModal',
    data: {
        current_item: {},
        cut_items: [],
        degree: 0,
        more_items: [],
        final_item: {},
        great_on_ground: {},
    },
    computed: {
        user_degree: function() {
            if (char_list.item_direct.indexOf('t') != -1)
                return this.current_item.degree * -1
            else
                return this.current_item.degree
        },
    },
    methods: {
        item_choice: function(item) {
            if (item === this.current_item) {
                this.final_item = this.current_item = item
                return;
            }
            var idx = this.cut_items.indexOf(item);
            this.great_on_ground = { marginLeft: -20 + 110 * idx + 'px' }
            cut_detail.more_items = []
            this.final_item = this.current_item = item
            this.more()
        },
        more: function() {
            if (!$("input.cut-option").prop('checked')) {
                cut_detail.more_items = []
                return;
            }
            $.get('/api/character/' + char_list.item_id + '/direct/' + char_list.item_direct + '/cut/' + this.current_item.degree, function(res) {
                if (res.direct !== char_list.item_direct) alert(res.direct)
                var _items = _.map(res.cut_list, function(item) {
                    if (char_list.item_direct.indexOf('t') != -1) {
                        item.display_degree = item.degree * -1
                    } else {
                        item.display_degree = item.degree
                    }
                    return item;
                });
                if (char_list.item_direct.indexOf('b') != -1) {
                    _items = _.reverse(_items)
                }
                cut_detail.more_items = _items
            }, 'json')
        },
        toggle_detail: function() {
            cut_detail.more()
        },
        item_final: function(item) {
            this.final_item = item
        },
        gen_cls(item) {
            if (this.final_item === item) {
                return 'gold-border'
            } else if (this.current_item === item) {
                return ''
            } else {
                return ''
            }
        },
        confirm() {
            if (this.final_item) {
                $.post('/api/character/' + char_list.item_id + '/direct/' + char_list.item_direct + '/cut/' + this.final_item.degree,
                    function(res) {
                        var url = res.image_url + "?v=" + Math.random()
                        if (!char_list.detecting){
                            var item = char_list.items[char_list.selection]
                            char_list.items.$set(char_list.selection, {
                                show: false,
                                id: item.id,
                                image_url: url,
                                cls_name: item.cls_name,
                                accuracy: item.accuracy,
                                char: item.char,
                                is_correct: 1
                            })
                        }else {
                            var item = char_list.detect_items[char_list.detect_selection]
                            char_list.detect_items.$set(char_list.detect_selection, {
                                show: false,
                                id: item.id,
                                image_url: url,
                                accuracy: item.accuracy,
                                char: item.char,
                                is_correct: 1,
                                is_same: res.is_same
                            })
                        }

                        char_list.item_url = url
                    }, 'json')
                $("#cutDetailModal").modal('hide')
            }
        }
    }
});
