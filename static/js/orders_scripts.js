window.onload = function () {
    var _quantity;
    var _price;
    var orderitem_num;
    var delta_quantity;
    var orderitem_quantity;
    var delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    // var TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_tatal_quantity = parseInt($('.order_total_quantity').text());
    var order_tatal_price = parseFloat($('.order_total_cost').text().replace(",", ".")) || 0;

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('span.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    function orderSummaryRecalc() {
        order_tatal_price = 0;
        order_tatal_quantity = 0;
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_tatal_quantity += quantity_arr[i];
            order_tatal_price += price_arr[i] * quantity_arr[i];
        }
        $('.order_total_quantity').html(order_tatal_quantity.toString());
        $('.order_total_cost').html(Number(order_tatal_price.toFixed(2).toString()));
    }

    $('.order_form').on('click', 'input[type=number]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            dеlta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], dеlta_quantity)
        }
    })

    // $('.order_form').on('click', 'input[type=checkbox]', function () {
    //     var target = event.target;
    //     orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
    //     if (target.checked) {
    //         dеlta_quantity = - quantity_arr[orderitem_num];
    //     } else {
    //         dеlta_quantity = quantity_arr[orderitem_num];
    //     }
    //     orderSummaryUpdate(price_arr[orderitem_num], dеlta_quantity);
    // });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity; //Разница по сумме
        order_tatal_price = Number((order_tatal_price + delta_cost).toFixed(2)); //Сумма
        order_tatal_quantity = order_tatal_quantity + delta_quantity; //Кол-во мест

        $('.order_total_quantity').html(order_tatal_quantity.toString());
        $('.order_total_cost').html(order_tatal_price.toString());

    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-DELETE', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }



    $('.order_form').on('change', 'select', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;
        if (orderitem_product_pk) {
            $.ajax({
                url: '/order/product/' + orderitem_product_pk + '/price/',
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        var price_html = '<span>' + data.price.toString().replace('.', ',') + '</span> руб.';
                        var curent_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        curent_tr.find('td:eq(2)').html(price_html);
                        orderSummaryRecalc();
                    }
                }
            })
        }
    });

}