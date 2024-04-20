# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Register, Payment
from .utils import send_sms_retry
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date

# tasks.py

# tasks.py

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist
from .models import Register
from .utils import calculate_fields, send_sms_retry

logger = get_task_logger(__name__)

# Inside your process_payment_rows function or elsewhere
#from modern.tasks import send_sms_task

# Call the Celery task

def calculate_fields_part1(register):
    today = datetime.today().date()

    if Payment.objects.filter(owner=register).exists():
        last_payment = Payment.objects.filter(owner=register).order_by('-date_paid').first()
        counts = Payment.objects.filter(owner=register).count()

        if register.reg_status:
            due_months = calculate_month_difference(last_payment.month_paid, today) - counts
            balance = register.room.amount * due_months
            pay_status = "Unpaid"
        else:
            due_months = calculate_month_difference(last_payment.month_paid, register.end_date) - counts
            balance = register.room.amount * due_months
            pay_status = "Unpaid"

        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = last_payment.month_paid + relativedelta(months=i)
            new_month_paid_list.append(new_month_paid)
        #print(new_month_paid_list)
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'mobile': register.owner.mobile,
            'room_number': register.room.room_number,
            'amount': register.room.amount,
            'balance': balance,
            'due_months': due_months,
            #'month_paid': new_month_paid,
            'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'pay_status': pay_status,
        }
    else:
        if register.reg_status:
            due_months = calculate_month_difference(register.start_date, today)
            balance = register.room.amount * due_months
            pay_status = "Unpaid"
        else:
            due_months = calculate_month_difference(register.start_date, register.end_date)
            balance = register.room.amount * due_months
            pay_status = "Unpaid"

        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = register.start_date + relativedelta(months=i)
            #print("new_month_paid_list:",new_month_paid)  
            new_month_paid_list.append(new_month_paid)
        #print("new_month_paid_list:",new_month_paid_list)
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'mobile': register.owner.mobile,
            'room_number': register.room.room_number,
            'amount': register.room.amount,
            'balance': balance,
            'due_months': due_months,
            #'month_paid': new_month_paid,
            'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            'pay_status': pay_status,
        }

@shared_task
def send_sms_task(message, numbers):
    send_sms_retry(message, numbers)


@shared_task
def process_payment_rows():
    logger.info("Processing payment rows...")
    all_new_payment_rows = []
    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        all_new_payment_rows.extend(new_payment_rows)
    
    for payment_row in all_new_payment_rows:
        try:
            message = f"Hello {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding month of {payment_row['month_paid'].strftime('%B %Y')} for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
            send_sms_retry(message, [payment_row['number']])
            logger.info(f"SMS sent to {payment_row['number']}")
        except ObjectDoesNotExist:
            logger.error(f"Failed to send SMS to {payment_row['number']}")




def list_registers_part1(request):
    all_registers = []

    for register in Register.objects.all():
        calculated_fields = calculate_fields_part1(register)
        if Payment.objects.filter(owner=register).exists():
            all_registers.append(calculated_fields)
        else:
            all_registers.append(calculated_fields)
            
    #owner_first_name = payment_row['owner'].split()[0]
    for payment_row in all_registers:
        #message = f"Hello {payment_row['owner']}, your monthly payment for {payment_row['month_paid'].strftime('%B %Y')} is ${payment_row['amount']}. Your current balance is ${payment_row['balance']}."
        message = f"Hi {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding months of {payment_row['new_month_paid_list']}, for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
        #print(payment_row['mobile'])
        send_sms_retry(message, [payment_row['mobile']])  # Use the retrying version of send_sms function

@shared_task
def send_monthly_payment_reminder():
    all_new_payment_rows = []

    # Fetch all new payment rows for the current month
    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        all_new_payment_rows.extend(new_payment_rows)

    # Send SMS for each payment row
    for payment_row in all_new_payment_rows:
        #if payment_row['month_paid'].day == 1:  # Check if it's the 1st day of the month
        message = f"Hello {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding month of {payment_row['month_paid'].strftime('%B %Y')} for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
        send_sms_retry.delay(message, [payment_row['number']])  # Use .delay() to enqueue the task

# tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .utils import send_sms_retry  # Import your SMS sending function
from .models import Register

from celery import shared_task
import datetime
from celery import shared_task
from django.utils import timezone
#from coded.celery import app as celery_app


# # # @shared_task
# # # def send_monthly_sms():
# # #     all_new_payment_rows = []
# # #     for register in Register.objects.all():
# # #         new_payment_rows = calculate_fields(register)
# # #         all_new_payment_rows.extend(new_payment_rows)
    
# # #     for payment_row in all_new_payment_rows:
# # #         message = f"Hello {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding month of {payment_row['month_paid'].strftime('%B %Y')} for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
# # #         send_sms_retry(message, [payment_row['number']])

@shared_task
def send_monthly_sms():
    all_registers = []

    for register in Register.objects.all():
        calculated_fields = calculate_fields_part1(register)
        if Payment.objects.filter(owner=register).exists():
            all_registers.append(calculated_fields)
        else:
            all_registers.append(calculated_fields)
            
    #owner_first_name = payment_row['owner'].split()[0]
    for payment_row in all_registers:
        outstanding_months = ", ".join(map(str, payment_row['new_month_paid_list']))
        #message = f"Hello {payment_row['owner']}, your monthly payment for {payment_row['month_paid'].strftime('%B %Y')} is ${payment_row['amount']}. Your current balance is ${payment_row['balance']}."
        message = f"Hi {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding months of {outstanding_months}, for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
        #print(payment_row['mobile'])
        send_sms_retry(message, [payment_row['mobile']])  # Use the retrying version of send_sms function
       

# @shared_task
# def send_scheduled_sms(message, numbers):
#     send_sms_retry(message, numbers)

# @shared_task
# def schedule_sms():
#     all_new_payment_rows = []

#     # Fetch all registers
#     for register in Register.objects.all():
#         new_payment_rows = calculate_fields(register)
#         all_new_payment_rows.extend(new_payment_rows)

#     # Send SMS for each payment row
#     for payment_row in all_new_payment_rows:
#         # Schedule SMS sending for the next month at noon
#         schedule_time = timezone.now().replace(day=1, hour=12, minute=0, second=0) + timedelta(days=1)  # Schedule for next month
#         message = f"Hello {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding month of {payment_row['month_paid'].strftime('%B %Y')} for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
#         send_scheduled_sms.apply_async(args=[message, [payment_row['number']]], eta=schedule_time)



from datetime import datetime

def calculate_month_difference(start_date, end_date):
    start_date = start_date.date() if isinstance(start_date, datetime) else start_date
    end_date = end_date.date() if isinstance(end_date, datetime) else end_date

    # Calculate the difference in months
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    return months

# def calculate_month_difference(start_date, end_date):
#     #months = relativedelta(end_date, start_date).months
#     #days = relativedelta(end_date, start_date).days
#     # Convert start_date and end_date to date objects if they are datetime objects
#     start_date = start_date.date() if isinstance(start_date, datetime) else start_date

#     # If end_date is None, return 0 months
#     if end_date is None:
#         return 0

#     end_date = end_date.date() if isinstance(end_date, datetime) else end_date

#     # Calculate month difference
#     months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

#     #print("months:",months)
#     return months