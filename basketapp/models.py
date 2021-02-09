from django.db import models
from django.conf import settings
from mainapp.models import Product
from authapp.models import ShopUser
from django.utils.functional import cached_property

class BasketQuerySet(models.QuerySet):
    """Обработчик для QuerySet
    """

    def delete(self, *args, **kwargs):
        """
        Переопределяем метод delete
        """
        for _object in self:
            _object.product.quantity += _object.quantity
            _object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(
        verbose_name='время добавления', auto_now_add=True)

    # def save(self):
    #     """Переопределяем save для
    #         выявление изменения остатков при редактировании заказа
    #     """
    #     if self.pk:
    #         self.product.quantity -= self.quantity - \
    #             - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save()

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def _get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)

    def _get_total_quantity(self):
        "return total quantity for user"
        _items = Basket.objects.filter(user=self.user)
        # _item = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    # total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        # _item = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    total_cost = property(_get_total_cost)

    @staticmethod
    def get_items(self, user):
        return Basket.objects.filter(user=user).order_by('product__category').select_related()

    @staticmethod
    def get_product(self, user, product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity})
         for item in basket_items]

        return basket_items_dic

    @staticmethod
    def get_item(pk):
        "Метод для получения информации по продукту"
        return Basket.objects.filter(pk=pk).first()

    # def delete(self):
    #     """Переопределение метода, возвражая остатки на склад
    #     Остатки хрянятся в самом продукте
    #     """
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()
