from rest_framework.response import Response
from rest_framework.views import APIView

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification



class Not(APIView):
    def get(self,request,format = None):
        device = FCMDevice()
        device.name = "yamen"
        device.registration_id = 'c6IYPntkTNu_dokXmQ6ogI:APA91bGbDDn0YR-xcgmvMthKrk2EFqn6-Pt_ou_hJJGZOyjQK5WVcKbHC-FJlnGt0oSbPvNkw56kM0M-uuM3eKb2QFekbE7UMQGBtVbajKJMnkoqLGWHb3iawybFv4NddwmS78sH2puG' #sent by the mobile
        device.user = request.user # upto you which user you want to associate
        device.type = "android" # if your device is android
        device.save()
        return Response({"message":"hello"})
    
    def post(self,request,format = None):
        device = FCMDevice.objects.all().first()

        device.send_message(Message(notification=Notification(title='hi', body='ahlen yamen')))

        return Response({"message":"hello"})

    

# def send_push_notification(token, title, body):
#     message = messaging.Message(
#         notification=messaging.Notification(title=title, body=body),
#         token=token,
#     )
    
#     try:
#         response = messaging.send(message)
#         return {'status': 'success', 'response': response}
#     except Exception as e:
#         return {'status': 'error', 'error': str(e)}