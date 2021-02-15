# from django.core.management.base import BaseCommand
# from mainapp.models import ProductCategory, Product
# from ordersapp.models import OrderItem
# from django.db import connection
# from django.db.models import Q
# from adminapp.views import db_profile_by_type

# from django.db.models import F, When, Case, DecimalField, IntegerField

from django.db.models import F, When, Case, DecimalField, IntegerField
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, DecimalField, IntegerField

from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='офис') |
        #     Q(category__name='модерн')
        # )

        # print(len(test_products))
        # # print(test_products)

        # db_profile_by_type('learn db', '', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)

        # Скидки
        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        # Условия для типов скидок
        action_1_condition = Q(order__updated_at__lte=F('order__updated_at') +
                               action_1_time_delta)

        action_2_condition = Q(
            order__updated_at__lte=F(
                'order__created_at') + action_2_time_delta,
            order__updated_at__gt=F('order__created_at') + action_1_time_delta
        )

        action_3_condition = Q(
            order__updated_at__gt=F(
                'order__created_at') + action_2_time_delta
        )

        # Типы скидок
        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition,
                              then=F('product__price') * F('quantity') * action_1_discount)

        action_2_price = When(action_2_condition,
                              then=F('product__price') * F('quantity') * -action_2_discount)

        action_3_price = When(action_3_condition,
                              then=F('product__price') * F('quantity') * action_3_discount)

        # print('*' * 50)
        # print(f'action_1__order={action_1_order}')
        # print(f'action_2__order={action_2_order}')
        # print(f'action_3_order={action_3_order}')
        # print(f'action_1_price={action_1_price}')
        # print(f'action_2_price={action_2_price}')
        # print(f'action_3_price={action_3_price}')
        # print('*' * 50)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,  # When -объект Условие: Значение
                action_2_order,  # When -объект Условие: Значение
                action_3_order,  # When -объект Условие: Значение
                default=0,       # Значение  по умолчанию (не обязательно)
                output_field=IntegerField(),  # Тип возврата
            )).annotate(
            total_price=Case(
                action_1_price,  # When -объект Условие: Значение
                action_2_price,  # When -объект Условие: Значение
                action_3_price,  # When -объект Условие: Значение
                output_field=DecimalField(),  # Тип возврата
            )).order_by('action_order', 'total_price').select_related()

        for order_item in test_orders:
            print(f'{order_item.action_order:2}: заказ №{order_item.pk:3}:\
                    {order_item.product.name:15}: скидка\
                    {abs(order_item.total_price):6.2f} руб. | \
                    {order_item.order.updated_at - order_item.order.created_at}')
