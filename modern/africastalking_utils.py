import africastalking
from django.conf import settings

def send_sms(message, recipients):
    africastalking.initialize(username=settings.AFRICASTALKING_USERNAME, api_key=settings.AFRICASTALKING_API_KEY)
    sms = africastalking.SMS
    response = sms.send(message, recipients)
    return response