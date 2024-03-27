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
from .models import Register, Payment, Room, Owner, Floor, Receiver, OwnerType
from .forms import RegisterForm , RegisterEditForm, PaymentForm, OwnerForm, Payment1Form, ReceiverForm, OwnerTypeForm
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import CustomUser
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import Payment
from .forms import PaymentForm, Payment2Form
import datetime
import random
import string
from django.contrib.auth.decorators import login_required
from account.decorators import group_required, unauthenticated_user, allowed_users

def stalls(n):
    g = Floor.objects.get(pk=1)
    room = []
    for i in range(1, 176):
        x = 'A' + str(i)
        room.append(x)
    for i in room:
        r = Room.objects.create(floor=g, room = i)
    #g.room = x
        r.save()
        print(r)
    #for i in r:
        print(r)

@login_required(login_url="/account/login")
def dashboard1(request):
    return render(request, 'base1.html')

@login_required(login_url="/account/login")
def ground(request):
    # g = Floor.objects.get(pk=1)
    # room = []
    # for i in range(1, 176):
    #     x = 'A' + str(i)
    #     room.append(x)
    # for i in room:
    #     r = Room.objects.create(floor=g, room_number=i, amount=1500)
    #     r.save()
    #     print(r)

    grounds = Room.objects.filter(floor=1)
    context = {
        'grounds': grounds,
    }
    return render(request, 'ground.html', context)

@login_required(login_url="/account/login")
def first(request):
    first = Room.objects.filter(floor=2)
    context = {
        'first': first,
    }
    return render(request, 'ground.html', context)

@login_required(login_url="/account/login")
def second(request):
    second = Room.objects.filter(floor=3)
    context = {
        'second': second,
    }
    return render(request, 'second.html', context)

@login_required(login_url="/account/login")
def index(request):
    from django.contrib.admin.models import LogEntry
    from account.models import CustomUser

    # Identify invalid user_id values
    invalid_user_ids = LogEntry.objects.exclude(user__in=CustomUser.objects.all())

    # Update invalid user_id values with valid ones
    for log_entry in invalid_user_ids:
        # Assuming there's a valid user_id available in the CustomUser table
        valid_user = CustomUser.objects.first()  # Example, you should replace this with your logic
        log_entry.user_id = valid_user.id
        log_entry.save()

    #rooms_arr = ['A1', 'A3', 'A6', 'A7', 'A8', 'A9']
    grounds = Room.objects.filter(floor=1)
   # print(queryset_objects.room_status)
    first = Room.objects.filter(floor=2)
    second = Room.objects.filter(floor=3)
    rooms = Room.objects.all()
    context = {
        'grounds': grounds,
        'first': first,
        'second': second,  
    }

    return render(request, 'ground.html', context)
    #return render(request, 'dash5.html')
    #return HttpResponse("Hello, world. You're at the polls index.")


###################################################################################################
@login_required(login_url="/account/login")
def dashboard_rooms(request):
    #list all rooms
    rooms = Room.objects.all()
    #list room count per floor with room_status = true(occupied) #and the once with room_status = false(vacant)
    #Get counts of occupied rooms per floor
    occupied_rooms_per_floor = Room.objects.filter(room_status=True).values('floor__name').annotate(occupied_count=Count('floor'))
    #print(occupied_rooms_per_floor)
    # Get counts of vacant rooms per floor
    vacant_rooms_per_floor = Room.objects.filter(room_status=False).values('floor__name').annotate(vacant_count=Count('floor'))
    print(vacant_rooms_per_floor)
    # List vacant rooms
    vacant_rooms = Room.objects.filter(room_status=False)
    # list occupied rooms
    occupied_rooms = Room.objects.filter(room_status=True)
    #print(occupied_rooms)

    #List vacant rooms by floor
    floor_name_ground = 'Ground'  # Specify the floor name here
    floor_name_first = 'First'
    floor_name_second = 'Second'
    vacant_rooms_ground = Room.objects.filter(room_status=False, floor__name=floor_name_ground)
    vacant_rooms_first = Room.objects.filter(room_status=False, floor__name=floor_name_first)
    vacant_rooms_second = Room.objects.filter(room_status=False, floor__name=floor_name_second)
    print(vacant_rooms_second)
    

    #print(reg_status1_count)
    context = {
        'rooms': rooms,
        'occupied_rooms_per_floor': occupied_rooms_per_floor,
        'vacant_rooms_per_floor': vacant_rooms_per_floor,

        'vacant_rooms': vacant_rooms,
        'occupied_rooms': occupied_rooms,

        'floor_name_ground': floor_name_ground,
        'floor_name_first': floor_name_first,
        'floor_name_second': floor_name_second,
        'vacant_rooms_ground': vacant_rooms_ground,
        'vacant_rooms_first': vacant_rooms_first,
        'vacant_rooms_second': vacant_rooms_second,

        #'room_count_per_floor': room_count_per_floor,
        #'reg_status1': reg_status1, 
        #'room_status_floor_True': room_status_floor_True, 
    }

    return render(request, 'dashboard_rooms.html', context)

# @login_required(login_url="/account/login")
# def dashboard_payment(request):
#     username = request.user.username
#     print(username)
#     #list payment
#     payments = Payment.objects.all()
    

#     # To get sum of owner.room.amount per owner and collected_by
#     amount_per_owner_collector = Payment.objects.values( 'collected_by__username').annotate(total_amount=Sum('owner__room__amount'))
#     print(amount_per_owner_collector)

#     # To get sum of amount_received per collector
#     amount_received_per_collector = Receiver.objects.values('collector__username').annotate(total_received=Sum('amount_received'))
#     print(amount_received_per_collector)
#     ###############################################################3
#     # Step 1: Calculate the sum of total amount collected per collected_by in the Payment model
#     total_collected_payment = Payment.objects.values('collected_by').annotate(total_amount_collected=Sum(F('owner__room__amount')))

#     # Step 2: Calculate the sum of total amount collected per collector in the Receiver model
#     total_collected_receiver = Receiver.objects.values('collector').annotate(total_amount_received=Sum('amount_received'))

#     # Step 3: Prepare a dictionary to store the balances
#     balances = {}
#     for collected_payment in total_collected_payment:
#         collected_by = collected_payment['collected_by']
#         total_amount_collected = collected_payment['total_amount_collected']
        
#         for collected_receiver in total_collected_receiver:
#             collector_id = collected_receiver['collector']
#             total_amount_received = collected_receiver['total_amount_received']
            
#             if collected_by == collector_id:
#                 balance = total_amount_collected - total_amount_received
#                 balances[collected_by] = balance

#     context = {
#         'payments': payments,
#         'amount_per_owner_collector': amount_per_owner_collector,
#         'total_collected_payment': total_collected_payment,
#         'total_collected_receiver': total_collected_receiver,
#         'balances': balances,  # Pass the balances dictionary to the template
#         'username': username,
#         #'payment_data': payment_data,
#         #'all_new_payment_rows': all_new_payment_rows,
        
#     }
#     return render(request, 'dashboard_payment.html', context)
from django.contrib.auth.models import User

@login_required(login_url="/account/login")
def dashboard_payment(request):
    username = request.user.username
    print(username)
    # List payments
    payments = Payment.objects.all()

    # To get sum of owner.room.amount per owner and collected_by
    amount_per_owner_collector = Payment.objects.values('collected_by__username').annotate(total_amount=Sum('owner__room__amount'))
    print(amount_per_owner_collector)

    # To get sum of amount_received per collector
    amount_received_per_collector = Receiver.objects.values('collector__username').annotate(total_received=Sum('amount_received'))
    print(amount_received_per_collector)

    # Step 1: Calculate the sum of total amount collected per collected_by in the Payment model
    total_collected_payment = Payment.objects.values('collected_by__username').annotate(total_amount_collected=Sum(F('owner__room__amount')))

    # Step 2: Calculate the sum of total amount collected per collector in the Receiver model
    total_collected_receiver = Receiver.objects.values('collector__username').annotate(total_amount_received=Sum('amount_received'))

    # Step 3: Prepare a dictionary to store the balances
    balances = {}
    for collected_payment in total_collected_payment:
        collected_by_username = collected_payment['collected_by__username']
        total_amount_collected = collected_payment['total_amount_collected']
        
        for collected_receiver in total_collected_receiver:
            collector_username = collected_receiver['collector__username']
            total_amount_received = collected_receiver['total_amount_received']
            
            if collected_by_username == collector_username:
                balance = total_amount_collected - total_amount_received
                balances[collected_by_username] = balance

    context = {
        'payments': payments,
        'amount_per_owner_collector': amount_per_owner_collector,
        'total_collected_payment': total_collected_payment,
        'total_collected_receiver': total_collected_receiver,
        'balances': balances,  # Pass the balances dictionary to the template
        'username': username,
        #'payment_data': payment_data,
        #'all_new_payment_rows': all_new_payment_rows,
    }
    return render(request, 'dashboard_payment.html', context)

def calculate_payment_data():
    # List all Register entries
    registers = Register.objects.all()

    # List all Payment entries
    payments = Payment.objects.all()

    # Initialize a list to store the final results
    payment_data = []

    # Loop through all registers
    for register in registers:
        # Find corresponding payment (if exists)
        payment = payments.filter(owner=register).order_by('-date_paid').first()

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
            'floor': register.room.floor,
            'room_number': register.room,
            'month_paid': month_paid,
            'due_months': due_months,
            'balance': balance,
        })

    return payment_data

@login_required(login_url="/account/login")
def dashboard_register(request):
    #list payment
    payment = Payment.objects.all()
    register = Register.objects.all()
    # Call the calculate_payment_data function
    payment_data = calculate_payment_data()
    amounts_by_month = defaultdict(float)

    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        for payment_row in new_payment_rows:
            amounts_by_month[payment_row['month_paid']] += payment_row['amount']
    
    amounts_by_month = dict(amounts_by_month)
    # Now you can use the payment data as needed
    #for data in payment_data:
        #print(data)

    #payments_with_sum = Payment.objects.values(
        #'owner__owner__name').annotate(total_sum=Sum('balance'))

    context = {
        'payment': payment,
        'payment_data': payment_data,
        'amounts_by_month': amounts_by_month,

        #'all_new_payment_rows': all_new_payment_rows,
        #'vacant_rooms_per_floor': vacant_rooms_per_floor,

        #'room_count_per_floor': room_count_per_floor,
        #'reg_status1': reg_status1, 
        #'room_status_floor_True': room_status_floor_True, 
    }
    return render(request, 'dashboard_register.html', context)

@login_required(login_url="/account/login")
def dashboard03(request):
    #list payment
    payment = Payment.objects.all()
    register = Register.objects.all()
    # Call the calculate_payment_data function
    payment_data = calculate_payment_data()

    # Now you can use the payment data as needed
    #for data in payment_data:
        #print(data)

    #payments_with_sum = Payment.objects.values(
        #'owner__owner__name').annotate(total_sum=Sum('balance'))

    context = {
        #'payment': payment,
        #'payment_data': payment_data,
        #'all_new_payment_rows': all_new_payment_rows,
        #'vacant_rooms_per_floor': vacant_rooms_per_floor,

        #'room_count_per_floor': room_count_per_floor,
        #'reg_status1': reg_status1, 
        #'room_status_floor_True': room_status_floor_True, 
    }
    return render(request, 'dashboard03.html', context)

@login_required(login_url="/account/login")
def dashboard04(request):
    #list payment
    payment = Payment.objects.all()
    register = Register.objects.all()
    # Call the calculate_payment_data function
    payment_data = calculate_payment_data()

    # Now you can use the payment data as needed
    #for data in payment_data:
        #print(data)

    #payments_with_sum = Payment.objects.values(
        #'owner__owner__name').annotate(total_sum=Sum('balance'))

    context = {
        #'payment': payment,
    }
    return render(request, 'dashboard04.html', context)

from django.utils.crypto import get_random_string

def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    if request.method == 'POST':
        form = Payment2Form(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_detail', payment_id=payment_id)
    else:
        form = Payment2Form(instance=payment)
    return render(request, 'edit_payment.html', {'form': form, 'payment': payment})

@login_required(login_url="/account/login")
def payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'payment_detail.html', {'payment': payment})

@login_required(login_url="/account/login")
def create_receiver(request):
    if request.method == 'POST':
        form = ReceiverForm(request.POST)
        if form.is_valid():
            receiver = form.save(commit=False)
            #if not receiver.reference_number:
            #    receiver.reference_number = get_random_string(length=10).upper()
            receiver.received_by = request.user  # Set received_by to the current user
            receiver.save()
            return redirect('list_receivers')  # Redirect to a success page
    else:
        form = ReceiverForm()
    
    return render(request, 'receiver.html', {'form': form})

@login_required(login_url="/account/login")
def list_receivers(request):
    receivers = Receiver.objects.all()
    return render(request, 'list_receivers.html', {'receivers': receivers})

@login_required(login_url="/account/login")
def list_owner(request):
    owners = Owner.objects.all()
    return render(request, 'list_owner.html', {'owners': owners})

@login_required(login_url="/account/login")
def create_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            # Set created_by field to the currently logged-in user
            owner = form.save(commit=False)
            owner.created_by = request.user
            owner.save()
            return redirect('list_owner')
    else:
        form = OwnerForm()
    return render(request, 'create_owner.html', {'form': form})
  
def owner_detail(request, pk):
    owner = Owner.objects.get(pk=pk)
    return render(request, 'owner_detail.html', {'owner': owner})

def owner_update(request, pk):
    owner = Owner.objects.get(pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'owner_form.html', {'form': form})

def owner_delete(request, pk):
    owner = Owner.objects.get(pk=pk)
    owner.delete()
    messages.success(request, 'Owner deleted successfully.')
    return redirect('list_owner')

# def owner_delete(request, pk):
#     owner = Owner.objects.get(pk=pk)
#     if request.method == 'POST':
#         owner.delete()
#         return redirect('owner_list')
#     return render(request, 'owner_confirm_delete.html', {'owner': owner})


def list_owner_type(request):
    owner_type = OwnerType.objects.all()
    return render(request, 'list_owner_type.html', {'owner_type': owner_type})

def create_owner_type(request):
    if request.method == 'POST':
        form = OwnerTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_owner_type')  # Redirect to a success page or URL
    else:
        form = OwnerTypeForm()
    return render(request, 'owner_type.html', {'form': form})

from collections import defaultdict
def calculate_fields(register):
    today = date.today()
    new_payment_rows = []
    
    if Payment.objects.filter(owner=register).exists():
        payment = Payment.objects.filter(owner=register).order_by('-date_paid')
        last_payment = payment.first()
        counts = Payment.objects.filter(owner=register).count()
        ouw_us = 0
        total_ouw_us = 0
        
        if register.reg_status:
            due_months = calculate_month_difference(last_payment.month_paid, today)
            if due_months < 0:
                ouw_us = abs(due_months)
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
            new_payment_rows.append({
                'owner_name': register.owner.name,
                'floor_name': register.room.floor.name,
                'room_number': register.room.room_number,
                'room_number': register.room.amount,
                'balance': balance,
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
            new_payment_rows.append({
                'owner_name': register.owner.name,
                'floor_name': register.room.floor.name,
                'room_number': register.room.room_number,
                'amount': register.room.amount,
                'balance': balance,
                'month_paid': new_month_paid,
                'start_date': register.start_date,
                'end_date': register.end_date,
            })

    return new_payment_rows

def list_register_test1(request):
    all_new_payment_rows = []
    owner_total_balance = defaultdict(int)  # Dictionary to store total balance for each combination
    
    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        all_new_payment_rows.extend(new_payment_rows)
        
        # Calculate and accumulate total balance for each combination
        for row in new_payment_rows:
            combination_key = (
                row['owner'],
                row['room_number'],
                row['floor']
            )
            owner_total_balance[combination_key] += row['balance']

    # Convert defaultdict to regular dictionary
    owner_total_balance = dict(owner_total_balance)
    
    context = {
        'all_new_payment_rows': all_new_payment_rows,
        'owner_total_balance': owner_total_balance,  # Include total balance in context
    }
    return render(request, 'list_register_test1.html', context)


####################################################################################################


################################## BEGINING OF PAYMENT FUNCTIONS #######################################
#@login_required
#@group_required('allowed_group')
@login_required(login_url="/account/login")
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
                register.created_by = request.user 
                register.room.save()
                register.save()

                messages.success(request, 'Room registered successfully.')
                return redirect('list_registers')
            else:
                messages.error(request, 'This room is occupied.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url="/account/login")
def get_rooms_by_floor(request):
    selected_floor = request.GET.get('floor')
    if selected_floor:
        rooms = Room.objects.filter(floor=selected_floor).values('id', 'room_number')
    else:
        rooms = Room.objects.all().values('id', 'room_number')

    return JsonResponse({'rooms': list(rooms)})
# views.py
from django.http import JsonResponse

@login_required(login_url="/account/login")
def get_floor_choices(request):
    floors = Room.objects.values_list('floor', flat=True).distinct()
    floor_choices = [(floor, floor) for floor in floors]
    return JsonResponse({'floor_choices': floor_choices})

@login_required(login_url="/account/login")
def get_room_numbers(request):
    floor = request.GET.get('floor')
    rooms = Room.objects.filter(floor=floor)
    room_numbers = [(room.room_number, room.room_number) for room in rooms]
    return JsonResponse({'room_numbers': room_numbers})

@login_required(login_url="/account/login")
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

# def list_register(request):
#     registers = Register.objects.all()  # Query all Register objects from the database
#     return render(request, 'register_list.html', {'registers': registers})

@login_required(login_url="/account/login")
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



#######################

################# END OF REGISTER FUNCTIONS #######################################

####################################################################################################

################## BEGINING OF PAYMENT FUNCTIONS #######################################
from datetime import datetime
def generate_invoice_number():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    #invoice_number = f"{year}{month:02d}{day:02d}-{random_part}"
    invoice_number = f"{day:02d}{month:02d}{year}{random_part}"
    return invoice_number

@login_required(login_url="/account/login")
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)  # Create the Payment instance but don't save it yet

            # Generate invoice number
            payment.invoice_number = generate_invoice_number()

            # Add your custom logic here to set the fields before saving
            if payment.owner.reg_status:
                payment.month_paid = payment.owner.start_date + relativedelta(months=1)
                payment.due_months = (date.today() - payment.month_paid).days // 30
                print(payment.due_months)
            else:
                last_payment = Payment.objects.filter(owner=payment.owner).order_by('-date_paid').first()
                if last_payment:
                    last_month_paid = last_payment.month_paid
                    if payment.owner.reg_status:
                        payment.month_paid = last_month_paid + relativedelta(months=1)
                        payment.due_months = (date.today() - payment.month_paid).days // 30
                        print(payment.due_months)
                    else:
                        payment.month_paid = last_month_paid + relativedelta(months=1)
                        payment.due_months = (payment.owner.end_date - payment.month_paid).days // 30
                        print(payment.due_months)
            
            # Set the created_by field to the currently logged-in user
            payment.collected_by = request.user
            
            # Set the pay_status field to 'Paid'
            payment.pay_status = 'Paid'
            
            # Calculate the balance
            date_now = date.today()
            payment.due_months = date_now.month - payment.month_paid.month + 12 * (date_now.year - payment.month_paid.year) 
            payment.balance = payment.owner.room.amount * payment.due_months

            # Check if the balance is below zero and raise a ValidationError if it is
            if payment.balance < 0:
                raise ValidationError("Balance cannot be negative")

            payment.save()  # Save the Payment instance with the updated fields
            return redirect('list_register_test')  # Redirect to a success page
    else:
        form = PaymentForm()

    return render(request, 'create_payment.html', {'form': form})

from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from .forms import PaymentForm
from .models import Payment, Register

@login_required(login_url="/account/login")
def create_payment_test2(request, register_id):
    if request.method == 'POST':
        register = get_object_or_404(Register, pk=register_id)
        owner = register.owner
        form = PaymentForm(request.POST, instance=register)
        if form.is_valid():
            payment = form.save(commit=False)  # Create the Payment instance but don't save it yet
            # Add your custom logic here to set the fields before saving
            
            # Correct the assignment of the owner
            payment.owner = owner.name

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

            payment.created_by = request.user 
            payment.pay_status = 'Paid'

            # Calculate the balance
            date_now = date.today()
            payment.due_months = date_now.month - payment.month_paid.month + 12 * (date_now.year - payment.month_paid.year)
            payment.balance = payment.owner.room.amount * payment.due_months

            # Check if the balance is below zero and raise a ValidationError if it is
            if payment.balance < 0:
                raise ValidationError("Balance cannot be negative")

            payment.save()  # Save the Payment instance with the updated fields
            return redirect('list_register_test')  # Redirect to a success page
    else:
        form = PaymentForm()

    registers = Register.objects.all()
    return render(request, 'create_payment_test2.html', {'form': form, 'registers': registers})

@login_required(login_url="/account/login")
def list_registers(request):
    registers = Register.objects.all()  # Fetch all register IDs
    return render(request, 'list_registers.html', {'registers': registers})
##########
@login_required(login_url="/account/login")
def list_registers(request):
    registers = Register.objects.filter(reg_status=True)  # Get registered models
    return render(request, 'list_registers.html', {'registers': registers})
##############
def create_payment_test(request, register_id):
    register = Register.objects.get(pk=register_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.owner = register  # Associate the payment with the register
            payment.save()
            return redirect('list_register_test')  # Redirect to a success page
    else:
        form = PaymentForm()

    return render(request, 'create_payment_test.html', {'form': form})

def get_rooms_and_floor(request):
    owner_id = request.GET.get('owner_id')
    register = Register.objects.get(pk=owner_id)
    rooms = Room.objects.filter(floor=register.room.floor).values('id', 'room_number')
    floor = register.room.floor.name
    return JsonResponse({'rooms': list(rooms), 'floor': floor})

def get_owner_name(request):
    owner_id = request.GET.get('owner_id')
    owner = Owner.objects.get(pk=owner_id)
    return HttpResponse(owner.name)

def get_owner_data(request):
    owner_id = request.GET.get('owner_id')
    owner = Owner.objects.get(pk=owner_id)
    register = owner.register_set.first()  # Assuming one owner can have only one register
    room = register.room
    floor = room.floor.name
    return JsonResponse({'rooms': [{'id': room.id, 'room_number': room.room_number}], 'floor': floor, 'room_number': room.room_number, 'owner_name': owner.name})
from django.http import JsonResponse
from .models import Owner, Room, Floor

def get_owner_data(request):
    owner_id = request.GET.get('owner_id')
    owner = Owner.objects.get(pk=owner_id)
    return JsonResponse({'floors': [{'id': floor.id, 'name': floor.name} for floor in owner.room_set.values('floor_id', 'floor__name').distinct()], 'owner_name': owner.name})

def get_rooms1(request):
    floor_id = request.GET.get('floor_id')
    rooms = Room.objects.filter(floor_id=floor_id).values('id', 'room_number')
    return JsonResponse({'rooms': list(rooms)})

def get_rooms(request):
    floor_id = request.GET.get('floor_id')
    rooms = Room.objects.filter(floor_id=floor_id).values('id', 'room_number')
    return JsonResponse({'rooms': list(rooms)})


def get_owner(request):
    room_id = request.GET.get('room_id')
    owner = Room.objects.get(pk=room_id).owner
    return JsonResponse({'owner_name': owner.name})


def get_room_and_owner(request):
    payment_id = request.GET.get('payment_id')
    payment = Payment.objects.get(pk=payment_id)
    room_number = payment.owner.room.room_number
    owner_name = payment.owner.owner.name
    return JsonResponse({'room_number': room_number, 'owner_name': owner_name})

##############
##########5ww
@login_required(login_url="/account/login")
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

        return {
            'owner': register.owner,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'month_paid': last_payment.month_paid,
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
            new_month_paid_list.append(new_month_paid)

        return {
            'owner': register.owner,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'month_paid': None,
            'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            'pay_status': pay_status,
        }

@login_required(login_url="/account/login")
def list_registers_part1(request):
    registers_in_payment = []
    registers_not_in_payment = []

    for register in Register.objects.all():
        if Payment.objects.filter(owner=register).exists():
            registers_in_payment.append(calculate_fields_part1(register))
        else:
            registers_not_in_payment.append(calculate_fields_part1(register))

    context = {
        'registers_in_payment': registers_in_payment,
        'registers_not_in_payment': registers_not_in_payment,
    }

    return render(request, 'list_registers_part1.html', context)


def month_difference(date1, date2):
    # Calculate the difference in months
    month_diff = date1.month - date2.month + 12 *  (date1.year - date2.year)
        
    return month_diff


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
                    'room_number': register.room.room_number,
                    'amount': register.room.amount,
                    'balance': balance,
                    'due_months': due_months,
                    'month_paid': new_month_paid,
                    'start_date': register.start_date,
                    'end_date': register.end_date,
                })

    return new_payment_rows

@login_required(login_url="/account/login")
def list_register_test(request):
    amounts_by_month = defaultdict(float)

    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        for payment_row in new_payment_rows:
            amounts_by_month[payment_row['month_paid']] += payment_row['amount']
    
    amounts_by_month = dict(amounts_by_month)

    all_new_payment_rows = []

    for register in Register.objects.all():
        new_payment_rows = calculate_fields(register)
        all_new_payment_rows.extend(new_payment_rows)
    
    context = {
        'all_new_payment_rows': all_new_payment_rows,
        'amounts_by_month': amounts_by_month,
        
    }

    return render(request, 'list_register_test.html', context)


def duplicate_payment_rows(register_id, due_months):
    register = Register.objects.get(id=register_id)
    last_payment = Payment.objects.filter(owner=register).latest('date_paid')
    current_month_paid = last_payment.month_paid

    for i in range(1, due_months + 1):
        # Increment the month paid by one month
        current_month_paid += timedelta(days=30)  # Roughly one month increment
        
        # Create a new Payment object for each duplicated row
        new_payment = Payment.objects.create(
            owner=register,
            date_paid=last_payment.date_paid,
            month_paid=current_month_paid,
            due_months=due_months - i,  # Decrease due months with each iteration
            balance=register.room.amount * (due_months - i),
            pay_status='Unpaid'
            # Add any additional fields you want to save for each duplicated row
        )
        new_payment.save()

    return f"Duplicated {due_months} rows for register {register_id}."


################# END OF PAYMENT FUNCTIONS #######################################

####################################################################################################


################# BEGINING OF (AUTHENTICATION && AUTHORIZATION) FUNCTIONS #######################################


# # Create your views here.
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Permission
# #from .models import CustomUser
# #from .forms import CustomUserForm
# from functools import wraps
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Group 
# #as AuthGroup

# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import login, logout
# from django.shortcuts import render, redirect


# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import Group
# from django.shortcuts import render, redirect
# from .models import CustomUser, CustomeGroup
# from .forms import CustomUserForm, CustomGroupForm

# def create_group(request):
#     if request.method == 'POST':
#         group_name = request.POST.get('group_name')
#         if not Group.objects.filter(name=group_name).exists():
#             Group.objects.create(name=group_name)
#             return redirect('group_list')
#         else:
#             error_message = "Group with this name already exists."
#             return render(request, 'create_group.html', {'error_message': error_message})
#     return render(request, 'create_group.html')

# def group_list(request):
#     groups = Group.objects.all()
#     return render(request, 'group_list.html', {'groups': groups})


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Redirect to home or any other page
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def user_logout(request):
#     logout(request)
#     return redirect('login')



# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Redirect to home or any other page after successful login
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('firstapp:home')  # Assuming firstapp has a URL named 'home'
#         else:
#             # Handle invalid login
#             return render(request, 'login.html', {'error': 'Invalid credentials'})
#     else:
#         return render(request, 'login.html')

# def user_logout(request):
#     logout(request)
#     return redirect('login')

# def group_required(group_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapped_view(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 content_type = ContentType.objects.get_for_model(CustomUser)
#                 permission_codename = f'view_{CustomUser._meta.model_name}'
#                 if request.user.has_perm(permission_codename, content_type):
#                     return view_func(request, *args, **kwargs)
#                 else:
#                     return redirect('unauthorized_page')
#             else:
#                 return redirect('unauthorized_page')
#         return wrapped_view
#     return decorator

# @login_required
# @group_required('Collector')
# def user_list(request):
#     users = CustomUser.objects.all()
#     return render(request, 'user_list.html', {'users': users})

# @login_required
# @group_required('admin')
# def user_detail(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     return render(request, 'user_detail.html', {'user': user})

# @login_required
# @group_required('admin')
# def user_create(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = CustomUserForm()
#     return render(request, 'user_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def user_update(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = CustomUserForm(instance=user)
#     return render(request, 'user_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def user_delete(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'user_confirm_delete.html', {'user': user})

# @login_required
# @group_required('admin')
# def group_list(request):
#     groups = Group.objects.all()
#     return render(request, 'group_list.html', {'groups': groups})

# @login_required
# @group_required('admin')
# def group_detail(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     return render(request, 'group_detail.html', {'group': group})

# @login_required
# @group_required('admin')
# def group_create(request):
#     if request.method == 'POST':
#         form = CustomGroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('group_list')
#     else:
#         form = CustomGroupForm()
#     return render(request, 'group_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def group_update(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     if request.method == 'POST':
#         form = CustomGroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             return redirect('group_list')
#     else:
#         form = CustomGroupForm(instance=group)
#     return render(request, 'group_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def group_delete(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     if request.method == 'POST':
#         group.delete()
#         return redirect('group_list')
#     return render(request, 'group_confirm_delete.html', {'group': group})

# @login_required
# def unauthorized_page(request):
#     return render(request, 'unauthorized_page.html')


################# END OF AUTHENTICATION FUNCTIONS #######################################

####################################################################################################