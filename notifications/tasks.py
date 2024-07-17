from celery import shared_task
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from celery.utils.log import get_task_logger

@shared_task(bind= True)
def notify_customers(self,promotion):
    devices = FCMDevice.objects.filter(user__role = 'CUSTOMER')
    for device in devices:
        device.send_message(Message(notification=Notification(title='{}'.format(promotion.name), body='{}'.format(promotion.description))))

@shared_task(bind=True)
def send_review_email(name,email,coupon):
    return send_review_email(name, email, coupon) 