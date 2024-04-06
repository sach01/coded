# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Register, Payment
from .utils import send_sms_retry
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
@shared_task
def send_monthly_payment_reminder():
    all_new_payment_rows = []

    # Fetch all new payment rows for the current month
    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        all_new_payment_rows.extend(new_payment_rows)

    # Send SMS for each payment row
    for payment_row in all_new_payment_rows:
        if payment_row['month_paid'].day == 1:  # Check if it's the 1st day of the month
            message = f"Hello {payment_row['owner']}, Marsabit Municipality would like you to know that you have outstanding month of {payment_row['month_paid'].strftime('%B %Y')} for stall number {payment_row['room_number']}. Your current balance is Ksh. {payment_row['balance']}."
            send_sms_retry.delay(message, [payment_row['number']])  # Use .delay() to enqueue the task

def calculate_fields(register):
    today = date.today()
    new_payment_rows = []

    if Payment.objects.filter(owner=register).exists():
        payment = Payment.objects.filter(owner=register).order_by('-date_paid')
        last_payment = payment.first()
        counts = payment.count()
        ouw_us = 0
        total_ouw_us = 0
        if register.reg_status:
            due_months = calculate_month_difference(last_payment.month_paid, today) 
            if due_months < 0:
                ouw_us1 = abs(due_months)
                ouw_us = ouw_us1
            print("ouw_us:",ouw_us)
            month_paid = last_payment.month_paid + relativedelta(months=1)
            balance = register.room.amount * due_months
            total_ouw_us = register.room.amount * ouw_us
        else:
            due_months = calculate_month_difference(last_payment.month_paid, register.end_date)
            month_paid = last_payment.month_paid - relativedelta(months=1)
            balance = register.room.amount * due_months
            total_ouw_us = register.room.amount * ouw_us

        for i in range(due_months):
            new_month_paid = last_payment.month_paid + relativedelta(months=i)
            if new_month_paid <= today:  # Skip adding rows for past months
                new_payment_rows.append({
                    'owner': register.owner.name,
                    'floor': register.room.floor,
                    'number': register.owner.mobile,
                    'room_number': register.room.room_number,
                    'amount': register.room.amount,
                    'balance': balance,
                    'due_months': due_months,
                    'ouw_us': ouw_us,
                    'total_ouw_us': total_ouw_us,
                    'month_paid': new_month_paid,
                    'start_date': register.start_date,
                    'end_date': register.end_date,
                })
        
    else:
        if register.reg_status:
            due_months = calculate_month_difference(register.start_date, today)
            month_paid = register.start_date
            balance = register.room.amount * due_months
        else:
            due_months = calculate_month_difference(register.start_date, register.end_date)
            month_paid = register.start_date
            balance = register.room.amount * due_months
        
        for i in range(due_months):
            new_month_paid = register.start_date + relativedelta(months=i)
            if new_month_paid <= today:  # Skip adding rows for past months
                new_payment_rows.append({
                    'owner': register.owner.name,
                    'floor': register.room.floor,
                    'number': register.owner.mobile,
                    'room_number': register.room.room_number,
                    'amount': register.room.amount,
                    'balance': balance,
                    'due_months': due_months,
                    'month_paid': new_month_paid,
                    'start_date': register.start_date,
                    'end_date': register.end_date,
                })

    return new_payment_rows

def calculate_month_difference(start_date, end_date):
    #months = relativedelta(end_date, start_date).months
    #days = relativedelta(end_date, start_date).days
    # Convert start_date and end_date to date objects if they are datetime objects
    start_date = start_date.date() if isinstance(start_date, datetime) else start_date

    # If end_date is None, return 0 months
    if end_date is None:
        return 0

    end_date = end_date.date() if isinstance(end_date, datetime) else end_date

    # Calculate month difference
    months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    print("months:",months)
    return months