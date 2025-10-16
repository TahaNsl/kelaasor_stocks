from django.db.models.signals import post_save
from django.dispatch import receiver

from companies.models import Share
from orders.models import Order, Transaction


@receiver(post_save, sender=Order)
def match_orders(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.order_type == 'BUY':
        sells = Order.objects.filter(
            company=instance.company,
            order_type='SELL',
            price__lte=instance.price
        ).order_by('price', 'created_at')
    else:
        sells = []
        buys = Order.objects.filter(
            company=instance.company,
            order_type='BUY',
            price__gte=instance.price
        ).order_by('-price', 'created_at')

    if instance.order_type == 'BUY':
        match_list = sells
    else:
        match_list = buys

    remaining_qty = instance.quantity

    for order in match_list:
        if remaining_qty == 0:
            break

        traded_qty = min(remaining_qty, order.quantity)
        trade_price = order.price if instance.order_type == 'BUY' else instance.price

        Transaction.objects.create(
            buyer=instance.user if instance.order_type == 'BUY' else order.user,
            seller=order.user if instance.order_type == 'BUY' else instance.user,
            company=instance.company,
            quantity=traded_qty,
            price=trade_price
        )

        buyer = instance.user if instance.order_type == 'BUY' else order.user
        seller = order.user if instance.order_type == 'BUY' else instance.user

        buyer_share, _ = Share.objects.get_or_create(owner=buyer, company=instance.company)
        seller_share, _ = Share.objects.get_or_create(owner=seller, company=instance.company)

        seller_share.quantity -= traded_qty
        buyer_share.quantity += traded_qty
        seller_share.save()
        buyer_share.save()

        order.quantity -= traded_qty
        remaining_qty -= traded_qty

        if order.quantity == 0:
            order.delete()
        else:
            order.save()

    if remaining_qty == 0:
        instance.delete()
    else:
        instance.quantity = remaining_qty
        instance.save()
