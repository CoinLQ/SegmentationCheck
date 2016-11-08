var char_list = new Vue({
    el: '#charListArea',
    data: {
        selection: 0,
        item_id: '',
        item_url: '',
        item_direct: '',
        items: charListContainer.data,
        cut_items: [],
        degree: 0,
        final_degree: 0,
        menu_style: {
            top: 0,
            left: 0,
            display: 'none'
        }
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
        goto_detail: function(){
            url = "/characters/" + this.items[this.selection].id;
            var _open = window.open(url);
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
        cut_image_modal: function() {
            var item = this.items[this.selection]
            this.item_url = item.image_url
            this.item_id = item.id
            $("#cutImageModal").modal('show')
            this.menu_style = {
                display: 'none'
            }
            document.removeEventListener('click', char_list._onContextMenuClick)
        },
        cut_detail_modal: function(direct) {
            this.item_direct = direct
            $("#cutDetailModal").modal('show')
        },
    }
});

$(function() {
    $('#cutImageModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget) // Button that triggered
        var modal = $(this)
        modal.find('.modal-title').text('字符切分')
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
                        char_list.item_url = url
                    }, 'json')
                $("#cutDetailModal").modal('hide')
            }
        }
    }
});
