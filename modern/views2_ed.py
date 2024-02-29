from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.http import HttpResponse
#ad-#KatuMani@22
#agm4EEgj5qf2hE7-as22
from django.db.models import Q, F
import datetime
from django.contrib import messages
#from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
#from datetime import datetime, date, timedelta
from .models import Register, Payment, Room, Owner
from .forms import RegisterForm , RegisterEditForm, PaymentForm, OwnerForm, Payment1Form
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Subquery, OuterRef, Count
from datetime import date
from django.db.models import Max, Sum
#from django.shortcuts import render
from datetime import datetime, timedelta
import pandas as pd



def index(request):

    return render(request, 'index.html')
    #return HttpResponse("Hello, world. You're at the polls index.")
def month_difference(date1, date2):
    # Calculate the difference in months
    month_diff = date1.month - date2.month + 12 *  (date1.year - date2.year)
    
     
    return month_diff
# Assuming these are your Django model imports
from .models import Register, Payment
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from django.shortcuts import render

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

    

def calculate_fields(register):
    today = date.today()

    if Payment.objects.filter(owner=register).exists():
        last_payment = Payment.objects.filter(owner=register).order_by('-date_paid').first()
        counts = Payment.objects.filter(owner=register).count()

        if register.reg_status:
            due_months = calculate_month_difference(last_payment.month_paid, today) - counts
            balance = register.room.amount * due_months
        else:
            due_months = calculate_month_difference(last_payment.month_paid, register.end_date) - counts
            balance = register.room.amount * due_months

        total_sum_floor = Register.objects.filter(room__floor=register.room.floor).aggregate(Sum('room__amount'))['room__amount__sum']
        total_sum_room = Register.objects.filter(room__room_number=register.room.room_number).aggregate(Sum('room__amount'))['room__amount__sum']
        total_balance_floor = total_sum_floor * due_months
        total_balance_room = total_sum_room * due_months
        '''
        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = last_payment.month_paid + relativedelta(months=i)
            new_month_paid_list.append(new_month_paid)
        '''
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'month_paid': last_payment.month_paid,
            #'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            'total_sum_floor': total_sum_floor,
            'total_sum_room': total_sum_room,
            'total_balance_floor': total_balance_floor,
            'total_balance_room': total_balance_room,
        }
    else:
        if register.reg_status:
            due_months = calculate_month_difference(register.start_date, date.today())
            balance = register.room.amount * due_months
        else:
            due_months = calculate_month_difference(register.start_date, register.end_date)
            balance = register.room.amount * due_months
        print(register.start_date)
        print(date.today())
        total_sum_floor = Register.objects.filter(room__floor=register.room.floor).aggregate(Sum('room__amount'))['room__amount__sum']
        total_sum_room = Register.objects.filter(room__room_number=register.room.room_number).aggregate(Sum('room__amount'))['room__amount__sum']
        total_balance_floor = total_sum_floor * due_months
        total_balance_room = total_sum_room * due_months
        '''
        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = register.start_date + relativedelta(months=i)
            new_month_paid_list.append(new_month_paid)
        '''
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'month_paid': None,
            #'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            'total_sum_floor': total_sum_floor,
            'total_sum_room': total_sum_room,
            'total_balance_floor': total_balance_floor,
            'total_balance_room': total_balance_room,
        }

def list_register_test(request):
    registers_in_payment = []
    registers_not_in_payment = []

    for register in Register.objects.all():
        if Payment.objects.filter(owner=register).exists():
            registers_in_payment.append(calculate_fields(register))
        else:
            registers_not_in_payment.append(calculate_fields(register))

    context = {
        'registers_in_payment': registers_in_payment,
        'registers_not_in_payment': registers_not_in_payment,
    }

    return render(request, 'list_register_test.html', context)

def dashboard(request):
    registers = Register.objects.all()
    payment_data = []

    for register in registers:
        payments = Payment.objects.filter(owner=register)
        last_payment = payments.last()
        counts = payments.count()

        if not payments.exists():
            if register.reg_status:
                due_months = (date.today().year - register.start_date.year) * 12 + (date.today().month - register.start_date.month)
                #due_months = (date.today().year - register.start_date.year) * 12 + (date.today().month - register.start_date.month)
                #due_months = (date.today().month - register.start_date.month)
            else:
                due_months = (register.end_date.year - register.start_date.year) * 12 + (register.end_date.month - register.start_date.month)
                #due_months = (register.end_date.month - register.start_date.month)

            month_paid = register.start_date
            pay_status = 'Unpaid' if register.reg_status else 'Pending'
            balance = register.room.amount * due_months

        else:
            '''
            #if not payments.exists():
            if register.reg_status:
                due_months = (date.today().year - register.start_date.year) * 12 + (date.today().month - register.start_date.month)
                #due_months = (date.today().month - register.start_date.month)
            else:
                due_months = (register.end_date.year - register.start_date.year) * 12 + (register.end_date.month - register.start_date.month)
                #due_months = (register.end_date.month - register.start_date.month)

            '''
            #today = date.today()
            #due_months = month_difference(last_payment.month_paid, today) - counts +1
            #print(due_months)
            #due_months = (date.today().month - last_payment.month_paid.month) - counts+1
            #print(due_months)
            month_paid = last_payment.month_paid
            pay_status = 'Unpaid' if register.reg_status else 'Pending'
            balance = register.room.amount * due_months


        for i in range(0, due_months ):
            new_month_paid = month_paid + relativedelta(months=i)

            duplicated_payment = {
                'owner': register.owner,
                'floor': register.room.floor.name,
                'room': register.room.room_number,
                'date_paid': timezone.now(),
                'month_paid': new_month_paid,
                'pay_status': pay_status,
                'due_months': 1,
                'amount': register.room.amount,
                'balance': balance,
            }

            payment_data.append(duplicated_payment)

    return render(request, 'payment_duplicate_list.html', {'payment_data': payment_data})
    
'''
def dashboard(request):
    registers = Register.objects.all()
    payment_data = []

    for register in registers:
        payments = Payment.objects.filter(owner=register)
        #last_payment = payments.last()
        last_payment = payments.latest('date_paid')
        
        if not payments.exists():
            # Calculate due_months based on conditions
            due_months = (date.today().month - register.start_date.month) if register.reg_status else (register.end_date.month - register.start_date.month)
            month_paid = register.start_date
            pay_status = 'Unpaid' if register.reg_status else 'Pending'
            balance = register.room.amount * due_months

        else:
            counts = payments.count()
            print(counts)
            #delta = relativedelta(date.today(), last_payment.month_paid)
            #delta2 = relativedelta(register.end_date.month - last_payment.month_paid.month)
            #month_difference = delta.years * 12 + delta.months
            ##due_months = (delta.years * 12 + delta.months) - counts if register.reg_status else (delta2.years * 12 + delta2.months) - counts
            ##due_months = (date.today().year - last_payment.month_paid.year) * 12 + (date.today().month - last_payment.month_paid.month) - counts if register.reg_status else (register.end_date.year - last_payment.month_paid.year) * 12 + (register.end_date.month - last_payment.month_paid.month) - counts
            #month_paid = last_payment.month_paid 
            due_months = (date.today().month - last_payment.month_paid.month) - counts if register.reg_status else (register.end_date.month - last_payment.month_paid.month) - counts
            #due_months = due_months1.years * 12 + due_months1.months
            month_paid = last_payment.month_paid 
            #+ relativedelta(months=1)
            pay_status = 'Unpaid' if register.reg_status else 'Pending'
            balance = register.room.amount * due_months
            print('due:',due_months)
        for i in range(0, due_months + 1 ):
            new_month_paid = month_paid + relativedelta(months=i)
            #floor_sum = 
            duplicated_payment = {
                'owner': register.owner,
                'floor': register.room.floor.name,
                'room': register.room.room_number,
                #'floor_sum': floor_sums,
                'date_paid': timezone.now(),
                'month_paid': new_month_paid,
                'pay_status': pay_status,
                'due_months': 1,
                'amount': register.room.amount,
                'balance': balance,
            }

            payment_data.append(duplicated_payment)
            #data = pd.DataFrame(list(payment_data))
            #html_table = data.to_html()
            #print(data)
            #print(html_table)
    df = pd.DataFrame(payment_data)

    # Group by 'Category' and calculate the sum for each group
    result = df.groupby('floor')['amount'].sum()

    # Display the result
    print(result)
    ##for i in payment_data:if i.floor:sum()print(i)
    
    return render(request, 'payment_duplicate_list.html', {'payment_data': payment_data})
'''

##################

#######################
    #return HttpResponse("Hello, world. You're at the polls index.")
#################
#Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)

            # Check room status and set the values accordingly
            if not register.room.room_status:
                register.room.room_status = True
                register.reg_status = True
                register.start_date = date.today()
                register.end_date = None
                register.room.save()
                register.save()

                messages.success(request, 'Room registered successfully.')
                return redirect('list_registers')
            else:
                messages.error(request, 'This room is occupied.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def get_rooms_by_floor(request):
    selected_floor = request.GET.get('floor')
    if selected_floor:
        rooms = Room.objects.filter(floor=selected_floor).values('id', 'room_number')
    else:
        rooms = Room.objects.all().values('id', 'room_number')

    return JsonResponse({'rooms': list(rooms)})
# views.py
from django.http import JsonResponse

def get_floor_choices(request):
    floors = Room.objects.values_list('floor', flat=True).distinct()
    floor_choices = [(floor, floor) for floor in floors]
    return JsonResponse({'floor_choices': floor_choices})

def get_room_numbers(request):
    floor = request.GET.get('floor')
    rooms = Room.objects.filter(floor=floor)
    room_numbers = [(room.room_number, room.room_number) for room in rooms]
    return JsonResponse({'room_numbers': room_numbers})

def get_rooms(request):
    room_floor = request.GET.get('room_floor')

    if room_floor:
        # Retrieve available room numbers for the selected room floor
        room_numbers = Room.objects.filter(floor=room_floor).values_list('room_number', flat=True).distinct()
    else:
        room_numbers = []

    data = {
        'room_numbers': '<option value="">Select Room Number</option>' + ''.join([f'<option value="{number}">{number}</option>' for number in room_numbers]),
    }

    return JsonResponse(data)

def list_registers(request):
    registers = Register.objects.filter(reg_status=True)  # Get registered models
    return render(request, 'list_registers.html', {'registers': registers})
def edited_registers(request):
    e_reg = Register.objects.filter(reg_status=False)  # Get edited register models
    return render(request, 'e_reg.html', {'e_reg':e_reg})
#list#reg_status=true/false
#edit_reg# due_month=0 and bal is 0
def edit_register(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    if request.method == 'POST':
        form = RegisterEditForm(request.POST, instance=register)
        if form.is_valid():
            if form.cleaned_data['reg_status'] is False:
                # Update room status and end date
                register.room.room_status = False
                register.end_date = date.today()
                register.room.save()
                register.save()
                return redirect('list_registers')
            else:
                register.save()
                return redirect('list_registers')
    else:
        form = RegisterEditForm(instance=register)

    return render(request, 'edit_register.html', {'form': form, 'register': register})

def list_register(request):
    registers = Register.objects.all()  # Query all Register objects from the database
    return render(request, 'register_list.html', {'registers': registers})

##################
#################
#dasboard

def calculate_balance_by_owner(owner, start_date, end_date, due_months):
    room_amount = owner.room.amount
    return room_amount * due_months

def calculate_due_months(start_date, end_date):
    if end_date:
        return (end_date - start_date).days // 30
    else:
        return (date.today() - start_date).days // 30

def create_payment_entry(register, pay_status, month_paid, balance, due_months):
    Payment.objects.create(
        owner=register,
        pay_status=pay_status,
        month_paid=month_paid,
        balance=balance,
        due_months=due_months
    )


def calculate_balance(room_amount, due_months):
    return room_amount * due_months

def calculate_due_months(start_date, end_date):
    if end_date:
        return (end_date - start_date).days // 30
    else:
        return (date.today() - start_date).days // 30

def create_payment_entry(register, pay_status, month_paid, balance, due_months):
    Payment.objects.create(
        owner=register,
        pay_status=pay_status,
        month_paid=month_paid,
        balance=balance,
        due_months=due_months
    )

def list_details(request):
    # Query all Register objects
    registers = Register.objects.all()

    # Iterate through each Register object and perform calculations
    for register in registers:
    # 
    # Check if there are any payments for the current register
        payments = Payment.objects.filter(owner=register)
        last_payment = payments.last()


        if not payments.exists():
        # Register ID not in Payment
            if register.reg_status:
                due_months = calculate_due_months(register.start_date, register.end_date)
                count_months = (date.today() - register.start_date).days // 30
                month_paid = register.start_date + timedelta(days=count_months * 30)
                pay_status = 'Unpaid'
                balance = calculate_balance(register.room.amount, due_months)
                print(due_months)
            else:
                due_months = calculate_due_months(register.start_date, register.end_date)
                pay_status = 'Pending'
                count_months = (date.today() - register.end_date).days // 30
                month_paid = register.end_date + timedelta(days=count_months * 30)
                balance = calculate_balance(register.room.amount, due_months)

            create_payment_entry(register, pay_status, month_paid, balance, due_months)

        else:
            # Register ID in Payment
            if register.reg_status:
                count_months = payments.count()
                due_months = (date.today().month - last_payment.month_paid.month) - count_months
            else:
                count_months = payments.count()
                due_months = (register.end_date.month - last_payment.month_paid.month) - count_months

        pay_status = 'Unpaid' if register.reg_status else 'Pending'
        month_paid = last_payment.month_paid + timedelta(days=due_months * 30)
        balance = calculate_balance(last_payment.owner.room.amount, due_months)

        create_payment_entry(register, pay_status, month_paid, balance, due_months)


    # Query the required data for displaying in the template
    data = Payment.objects.values(
        'owner__room__room_number',
        'owner__owner__name',
        'owner__room__floor',
        'owner__room__room_number',
        'owner__start_date',
        'pay_status',
        'month_paid',
        'balance',
        'due_months'
    )

    return render(request, 'list_details.html', {'data': data})

def display_details_1(request):
    # Get all registers
    registers = Register.objects.all()

    # Create an empty list to store the results
    result_list = []

    for register in registers:
        # Check if the register has payments
        payments = Payment.objects.filter(owner=register)

        if payments.exists():
            # If there are payments, get the last payment
            last_payment = payments.latest('date_paid')

            # Calculate due_months and set pay_status
            if register.reg_status:
                due_months = (datetime.now().month - last_payment.month_paid.month) - payments.count()
                pay_status = 'Unpaid'
            else:
                due_months = (register.end_date.month - last_payment.month_paid.month) - payments.count()
                pay_status = 'Pending'

            # Increment month_paid by due_months
            month_paid = last_payment.month_paid + timedelta(days=30 * due_months)
            print(due_months)
            print(month_paid)
            # Calculate balance
            balance = register.room.amount * due_months

        else:
            # If there are no payments, calculate due_months, pay_status, and balance
            if register.reg_status:
                due_months = datetime.now().month - register.start_date.month
                print(due_months)
                pay_status = 'Unpaid'
            else:
                due_months = (register.end_date.month - register.start_date.month) + 1
                pay_status = 'Pending'

            month_paid = register.start_date + timedelta(days=30 * due_months)
            print(month_paid)
            balance = register.room.amount * due_months

        # Append the result to the result_list
        result_list.append({
            'room_number': register.room.room_number,
            'owner': register.owner.name,
            'floor': register.room.floor,
            'room': register.room,
            'start_date': register.start_date,
            'pay_status': pay_status,
            'month_paid': month_paid,
            'balance': balance,
            'due_months': due_months,
        })

    # Pass the result_list to the template and render it
    context = {'result_list': result_list}
    return render(request, 'result_list.html', context)



def display_payment_details(request, register_id):
    try:
        register = Register.objects.get(id=register_id)
    except Register.DoesNotExist:
        # Handle the case where the register ID doesn't exist
        return render(request, 'error_page.html', {'error_message': 'Register not found'})

    # Check if the register ID exists in payments
    payments = Payment.objects.filter(register_id=register_id)
    if payments.exists():
        # Get the last payment for the room
        last_payment = payments.latest('date_paid')

        # Calculate due_months based on reg_status
        if register.reg_status:
            due_months = (date.today().month - last_payment.month_paid.month) - last_payment.counts
            pay_status = 'Unpaid'  # Replace with your choice field values
        else:
            due_months = (register.end_date - last_payment.month_paid.month) - last_payment.counts
            pay_status = 'Pending'  # Replace with your choice field values

        #month_paid = last_payment.month_paid + timedelta(months=due_months)
    else:
        # Handle the case where register ID doesn't exist in payments
        if register.reg_status:
            due_months = (date.today().month - register.start_date.month)
            pay_status = 'Unpaid'  # Replace with your choice field values
        else:
            due_months = (register.end_date - register.start_date.month)
            pay_status = 'Pending'  # Replace with your choice field values

        month_paid = register.start_date + timedelta(months=due_months)

    # Calculate balance, sum_paid, sum_unpaid, sum_pending
    balance = register.owner.room.amount * due_months
    sum_paid = Payment.objects.filter(register_id=register_id, pay_status='Paid').aggregate(Sum('amount'))['amount__sum']
    sum_unpaid = Payment.objects.filter(register_id=register_id, pay_status='Unpaid').aggregate(Sum('amount'))['amount__sum']
    sum_pending = Payment.objects.filter(register_id=register_id, pay_status='Pending').aggregate(Sum('amount'))['amount__sum']

    context = {
        'register': register,
        'due_months': due_months,
        'pay_status': pay_status,
        'month_paid': month_paid,
        'balance': balance,
        'sum_paid': sum_paid,
        'sum_unpaid': sum_unpaid,
        'sum_pending': sum_pending,
    }

    return render(request, 'payment_details.html', context)

######################


def get_payment_details(owner_id):
    payments = Payment.objects.filter(owner_id=owner_id)
    registration = Register.objects.filter(owner_id=owner_id).first()
    if registration:
        register_ids_with_payments = Payment.objects.filter(register__id=registration.id).values_list('register__id', flat=True)
        register_with_no_payments = Register.objects.exclude(id__in=register_ids_with_payments).filter(owner_id=owner_id)

        for reg in register_with_no_payments:
            due_months = (datetime.now().date() - reg.start_date).days // 30
            if reg.reg_status:
                pay_status = Payment.PAY_STATUS_CHOICES[1][0] # Unpaid
                month_paid = reg.start_date + timedelta(days=due_months*30)
            else:
                pay_status = Payment.PAY_STATUS_CHOICES[2][0] # Pending
                month_paid = reg.start_date + timedelta(days=due_months*30)

            balance = reg.owner.room.amount * due_months
            sum_paid = Payment.objects.filter(register__id=reg.id, pay_status=Payment.PAY_STATUS_CHOICES[0][0]).aggregate(Sum('balance'))['balance__sum'] or 0
            sum_unpaid = Payment.objects.filter(register__id=reg.id, pay_status=Payment.PAY_STATUS_CHOICES[1][0]).aggregate(Sum('balance'))['balance__sum'] or 0
            sum_pending = Payment.objects.filter(register__id=reg.id, pay_status=Payment.PAY_STATUS_CHOICES[2][0]).aggregate(Sum('balance'))['balance__sum'] or 0

            payment = Payment(
                owner=reg.owner,
                floor=reg.floor,
                room=reg.room,
                start_date=reg.start_date,
                pay_status=pay_status,
                month_paid=month_paid,
                balance=balance,
                sum_paid=sum_paid,
                sum_unpaid=sum_unpaid,
                sum_pending=sum_pending,
                register=reg,
            )
            payments = payments | payment

    return payments

def payment_details(request, owner_id):
    payments = get_payment_details(owner_id)

    return render(request, 'payment_details.html', {'payments': payments})
#######################

def calculate_balance(register):
    last_payment = Payment.objects.filter(owner=register).order_by('-date_paid').last()
    if last_payment:
        counts = Payment.objects.filter(owner=register).count()
        if register.reg_status:
            #due_months =  (register.start_date.month - last_payment.month_paid.month) - counts
            due_months =   last_payment.due_months - counts 
            month_paid = last_payment.month_paid + relativedelta(months=1)
            print('next',month_paid)
            # #print(register.start_date.month)
            # print(counts-last_payment.due_months)
            print(register.start_date)
            print(last_payment.month_paid, date)
            print('due:',due_months)
        else:
            due_months =  (register.end_date.month - last_payment.month_paid.month) - counts
            month_paid = last_payment.month_paid + relativedelta(months=1)
            print('next',month_paid)
            print(register.end_date.month)
            print('due1:',due_months)
        
        #balance = register.room.amount * due_months
    else:
        if register.reg_status:
            due_months = timezone.now().month - register.start_date.month
            #print(due_months)
        else:
            due_months = register.end_date.month - register.start_date.month
            print(due_months)
    balance = register.room.amount * due_months
    return due_months, balance

def list_registers2(request):
    registers_in_payment = []
    registers_not_in_payment = []

    all_registers = Register.objects.all()

    for register in all_registers:
        payment_exists = Payment.objects.filter(owner=register).exists()
        due_months, balance = calculate_balance(register)

        if payment_exists:
            registers_in_payment.append({
                'register_id': register.owner.name,
                'due_months': due_months,
                'balance': balance,
                'reg_status': register.reg_status,
                
                #'month_paid': month_paid,
            })
        else:
            registers_not_in_payment.append({
                'register_id': register.owner.name,
                'due_months': due_months,
                'balance': balance,
                'reg_status': register.reg_status,
                #'month_paid': month_paid,
            })

    return render(request, 'list_registers2.html', {
        'registers_in_payment': registers_in_payment,
        'registers_not_in_payment': registers_not_in_payment,
    })

def register_list3(request):
    # Get all registers
    registers = Register.objects.all()

    # Create empty lists to store the results
    registers_in_payment = []
    registers_not_in_payment = []

    # Iterate through all registers
    for register in registers:
        payments = Payment.objects.filter(owner=register)
        last_payment = payments.last() if payments else None

        # Calculate due_months based on conditions
        if register.reg_status and last_payment:
            due_months = (register.start_date.month - last_payment.month_paid.month) 
        elif not register.reg_status and last_payment:
            due_months = (register.end_date.month - last_payment.month_paid.month) 
        elif register.reg_status:
            due_months = datetime.today().month - register.start_date.month
        else:
            due_months = register.end_date.month - register.start_date.month

        # Calculate balance
        balance = register.room.amount * due_months

        # Create a dictionary with the calculated values
        result = {
            'register_id': register.owner.name,
            'due_months': due_months,
            'balance': balance,
        }

        # Append the result to the appropriate list
        if payments:
            registers_in_payment.append(result)
        else:
            registers_not_in_payment.append(result)

    # Render a template with the results
    return render(request, 'register_list3.html', {
        'registers_in_payment': registers_in_payment,
        'registers_not_in_payment': registers_not_in_payment,
    })
#############
##############

def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)  # Create the Payment instance but don't save it yet
            # Add your custom logic here to set the fields before saving
            # You can use the same logic you provided in the Payment model's save method
            if payment.owner.reg_status:
                payment.month_paid = payment.owner.start_date
                payment.due_months = 1
            else:
                last_payment = Payment.objects.filter(owner=payment.owner).order_by('-date_paid').first()
                if last_payment:
                    last_month_paid = last_payment.month_paid
                    if payment.owner.reg_status:
                        payment.month_paid = last_month_paid + relativedelta(months=1)
                        payment.due_months = (date.today() - payment.month_paid).days // 30
                    else:
                        payment.month_paid = last_month_paid + relativedelta(months=1)
                        payment.due_months = (payment.owner.end_date - payment.month_paid).days // 30

            # Calculate the balance
            date_now = date.today()
            payment.due_months = date_now.month - payment.month_paid.month + 12 * (date_now.year - payment.month_paid.year)
            payment.balance = payment.owner.room.amount * payment.due_months

            # Check if the balance is below zero and raise a ValidationError if it is
            if payment.balance < 0:
                raise ValidationError("Balance cannot be negative")

            payment.save()  # Save the Payment instance with the updated fields
            return redirect('list_registers2')  # Redirect to a success page

    else:
        form = PaymentForm()

    return render(request, 'create_payment.html', {'form': form})
##############
##########5ww
def payment_list(request):
    # List all Register entries
    registers = Register.objects.all()

    # List all Payment entries
    payments = Payment.objects.all()

    # Initialize a list to store the final results
    payment_data = []

    # Loop through all registers
    for register in registers:
        # Find corresponding payment (if exists)
        payment = payments.filter(owner=register).order_by('-date_paid').last()

        # Calculate month_paid, due_months, and balance
        if register.reg_status:
            month_paid = register.start_date
            due_months1 = (date.today().year - register.start_date.year) * 12 + (date.today().month - register.start_date.month)
            due_months = (date.today().year - register.start_date.year) * 12 + (date.today().month - register.start_date.month)

            balance = register.room.amount * due_months
        else:
            month_paid = register.start_date
            due_months = (register.end_date.year - register.start_date.year) * 12 + (register.end_date.month - register.start_date.month)
            balance = register.room.amount * due_months

        # If a payment exists, update month_paid, due_months, and balance accordingly
        if payment:
            if register.reg_status:
                month_paid = payment.month_paid + timedelta(days=30)  # Assuming a 30-day month
                due_months = (date.today().year - payment.month_paid.year) * 12 + (date.today().month - payment.month_paid.month)
                balance = register.room.amount * due_months
            else:
                month_paid = payment.month_paid
                due_months = (register.end_date.year - payment.month_paid.year) * 12 + (register.end_date.month - payment.month_paid.month)
                balance = register.room.amount * due_months

        # Add the payment data to the list
        payment_data.append({
            'owner': register.owner,
            'month_paid': month_paid,
            'due_months': due_months,
            'balance': balance,
        })

    return render(request, 'payment_list.html', {'payment_data': payment_data})

