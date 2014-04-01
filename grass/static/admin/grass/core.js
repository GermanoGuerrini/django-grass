(django.jQuery)(function() {

    var name = 'grass',
        defaults = {
            ajax_url: '',
            static_url: '/static/',
            loader_url: 'autocomplete_light/xhr-pending.gif',
        };

    var Grass = function(element, options) {
        this.options = $.extend({}, defaults, options);
        this.$element = $(element);
        this.$container = this.$element.parents('.inline-group');
        this.$loader = $('<img>').insertAfter(this.$element);
        this.$results = $('<div>').insertAfter(this.$element);
        this.$add = $('<button>').insertAfter(this.$results);
        this.$add_inline = this.$container.find('.add-row a').first();
        this.$remove = null;
        this.setup();
        this.bind();
    };

    Grass.prototype.setup = function() {
        this.$loader.hide().attr('src', this.options.static_url + this.options.loader_url);
        this.$add.hide().text('Add');
    };

    Grass.prototype.bind = function() {
        var $autocomplete = this.$element.yourlabsAutocomplete()
        $autocomplete.input.bind('selectChoice', this.select());
        this.$add.on('click', this.add());
    };

    Grass.prototype.select = function() {
        var _this = this;
        return function(e, choice, autocomplete) {
            var selected_data = choice.data('value');
            var data_bits = selected_data.split('-');
            $.ajax({
                url: _this.options.ajax_url,
                data: {content_type: data_bits[0], object_id: data_bits[1]},
                beforeSend: function() { _this.$loader.show(); },
                success: function(data) { _this.$results.html(data); },
                complete: function() {
                    _this.$loader.hide();
                    _this.$add.show();
                    _this.$remove = _this.$container.find('.deck .remove');
                    _this.$remove.on('click', _this.reset());
                },
            });
        };
    };

    Grass.prototype.collect = function() {
        var items = [];
        var main = this.$container.find('.deck span').data('value');
        items.push(main.split('-'));
        var $selects = this.$results.find('select');
        $selects.each(function() {
            var ct = $(this).data('grass-ct');
            var values = $(this).val();
            for(var v in values)
                items.push([ct, values[v]]);
        });
        return items;
    };

    Grass.prototype.add = function() {
        var _this = this;
        return function(e) {
            e.preventDefault();
            var items = _this.collect();
            for(var i in items)
                _this.insert(items[i]);
            _this.$remove.trigger('click');
        };
    };

    Grass.prototype.insert = function(item) {
        this.$add_inline[0].click();
        var content_type = this.$container.find('.field-content_type:visible select').last();
        var object_id = this.$container.find('.field-object_id:visible input').last();
        content_type.val(item[0]);
        object_id.val(item[1]);
    };

    Grass.prototype.reset = function() {
        var _this = this;
        return function() {
            _this.$results.text('');
            _this.$add.hide();
        };
    };

    $.fn[name] = function(options) {
        return this.each(function() {
            if(!$.data(this, 'plugin_' + name))
                $.data(this, 'plugin_' + name, new Grass(this, options));
        });
    };

});