from celery import shared_task
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from .models import notification
from promotion.models import Promotion, Coupon, UsedCoupons, CustomerProfile


@shared_task(bind=True)
def promo_notify_customers(self, promotion):
    promotion = Promotion.objects.get(id=promotion)
    devices = FCMDevice.objects.filter(user__role="CUSTOMER")
    title = "{}".format(promotion.name)
    body = "{}".format(promotion.description)

    data = {}
    data["body"] = body
    data["title"] = title

    for device in devices:
        device.send_message(
            Message(
                notification=Notification(
                    title=title,
                    body=body,
                )
            )
        )
        data["user"] = device.user
        notification.objects.create(**data)


@shared_task(bind=True)
def notify_customers_deserving_coupon(self, users, coupon):
    coupon = Coupon.objects.get(pk=coupon)
    customers = CustomerProfile.objects.filter(user__in=users).exclude(
        customer_coupon__coupon_id=coupon
    )
    users = customers.values_list("user", flat=True)
    devices = FCMDevice.objects.filter(
        registration_id="e1iMWVFtTUqTMaiP2zexU7:APA91bGvC9E7zyBnOpET-gQgc1d2PJ3W4vzok9CtTv_Fw26mtvMWhWCG3wj8uqZaRYqjIOWLRW9Mc0-JF7PduyC2ojqM9TJ-B1u_bdpJkAPCcBNq-ZmnMpYeMXnJsDNEp3STG7q5fZ1n"
    )

    body = "your code is {}".format(coupon.coupon_code)
    data = {}
    data["body"] = body
    for device in devices:
        congrat = "hello {} congratulations on earning the coupon {}".format(
            device.user.username, coupon.name
        )
        device.send_message(
            Message(
                notification=Notification(
                    title=congrat,
                    body=body,
                )
            )
        )
        data["title"] = congrat
        data["user"] = device.user
        notification.objects.create(**data)

    for customer in customers:
        UsedCoupons.objects.create(coupon_id=coupon, customer=customer)
    return "notified all customers deserving the coupon "


@shared_task(bind=True)
def notifiy_drivers(self):

    devices = FCMDevice.objects.filter(user__role="DRIVER")
    if devices:
        title = "A New Order is Available"
        body = "open app to view order details"

        for device in devices:
            device.send_message(
                Message(
                    notification=Notification(
                        title=title,
                        body=body,
                    )
                )
            )


@shared_task(bind=True)
def notifiy_to_leave_review(self):
    from order.models import Order
    from datetime import datetime,timedelta
    yesterday = datetime.now - timedelta(1)
    order = Order.objects.filter(order_status = 'Deliverd',date_deliverd__in = datetime.now())
    devices = FCMDevice.objects.filter(user__role="Customer")
    if devices:
        title = "A New Order is Available"
        body = "open app to view order details"

        for device in devices:
            device.send_message(
                Message(
                    notification=Notification(
                        title=title,
                        body=body,
                    )
                )
            )