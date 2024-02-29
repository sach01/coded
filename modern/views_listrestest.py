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
from .models import Register, Payment, Room, Owner, Floor
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth
#St@11s@4321
#modern

def stalls(n):
    g = Floor.objects.get(pk=1)
    room = []
    for i in range(1, 176):
        x = 'C' + str(i)
        room.append(x)
    for i in room:
        r = Room.objects.create(floor=g, room = i)
    #g.room = x
        r.save()
    for i in r:
        print(r)

def index(request):
    #rooms_arr = ['A1', 'A3', 'A6', 'A7', 'A8', 'A9']
    grounds = Room.objects.filter(floor=1)
   # print(queryset_objects.room_status)
    first = Room.objects.filter(floor=2)
    second = Room.objects.filter(floor=3)

    context = {
        'grounds': grounds,
        'first': first,
        'second': second,  
    }

    return render(request, 'dash7.html', context)
    #return render(request, 'dash5.html')
    #return HttpResponse("Hello, world. You're at the polls index.")




####################################################################################################


################################## BEGINING OF PAYMENT FUNCTIONS #######################################

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
################# END OF REGISTER FUNCTIONS #######################################

####################################################################################################

################## BEGINING OF PAYMENT FUNCTIONS #######################################


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
           
            payment.created_by = request.user 
            payment.pay_status = 'Pending'
            payment.status = False
            # Calculate the balance
            date_now = date.today()
            payment.due_months = date_now.month - payment.month_paid.month + 12 * (date_now.year - payment.month_paid.year)
            payment.balance = payment.owner.room.amount * payment.due_months

            # Check if the balance is below zero and raise a ValidationError if it is
            if payment.balance < 0:
                raise ValidationError("Balance cannot be negative")

            payment.save()  # Save the Payment instance with the updated fields
            list_register_test
            return redirect('list_register_test')  # Redirect to a success page
            #return redirect('list_registers2')  # Redirect to a success page

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


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import Register, Payment
from django.shortcuts import render


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

    if Payment.objects.filter(owner=register).exists():
        last_payment = Payment.objects.filter(owner=register).order_by('-date_paid').first()
        counts = Payment.objects.filter(owner=register).count()
        ouw_us = 0
        total_ouw_us = 0
        if register.reg_status:
            #counts
            due_months = calculate_month_difference(last_payment.month_paid, today) -1
            #ouw_us = 0
            if due_months < 0:
                ouw_us = abs(due_months)
                due_months = 0
                print(ouw_us)
                print("ouw_us:",ouw_us)
                print("due_months:",due_months)
            #due_months =   last_payment.due_months - counts 
            #month_paid = last_payment.month_paid + relativedelta(months=1)
            month_paid = last_payment.month_paid + relativedelta(months=1)
            balance = register.room.amount * due_months
            total_ouw_us = register.room.amount * ouw_us
        else:
            due_months = calculate_month_difference(last_payment.month_paid, register.end_date) 
            month_paid = last_payment.month_paid - relativedelta(months=1)
            balance = register.room.amount * due_months
            total_ouw_us = register.room.amount * ouw_us
            
        pay_status = last_payment.pay_status
        status = last_payment.status
        print("status:", status)
        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = last_payment.month_paid + relativedelta(months=i)
            new_month_paid_list.append(new_month_paid)
        
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'ouw_us': ouw_us,
            'total_ouw_us': total_ouw_us,
            'month_paid': last_payment.month_paid,
            'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            'pay_status': last_payment.pay_status
        }
    else:
        if register.reg_status:
            due_months = calculate_month_difference(register.start_date, date.today())
            month_paid = register.start_date
            balance = register.room.amount * due_months
        else:
            due_months = calculate_month_difference(register.start_date, register.end_date)
            month_paid = register.start_date
            balance = register.room.amount * due_months
        print(register.start_date)
        print(date.today())
       
        #floor = register.room.floor  # Get the floor information

        new_month_paid_list = []
        for i in range(0, due_months):
            new_month_paid = register.start_date + relativedelta(months=i)
            new_month_paid_list.append(new_month_paid)
        
        return {
            'owner': register.owner.name,
            'floor': register.room.floor,
            'room_number': register.room.room_number,
            'balance': balance,
            'due_months': due_months,
            'month_paid': month_paid,
            'new_month_paid_list': new_month_paid_list,  # List of incremented month_paid values
            'start_date': register.start_date,
            'end_date': register.end_date,
            
        }

def list_register_test(request):
    registers_in_payment = []
    registers_not_in_payment = []
    
    # Dictionary to store total balance per floor
   # total_balance_per_floor = {}

    for register in Register.objects.all():
        result = calculate_fields(register)
        if Payment.objects.filter(owner=register).exists():
            registers_in_payment.append(result)
        else:
            registers_not_in_payment.append(result)

        # Update the total balance for the floor
        #floor = result['floor']
        #total_balance_per_floor[floor] = total_balance_per_floor.get(floor, 0) + result['balance']

    context = {
        'registers_in_payment': registers_in_payment,
        'registers_not_in_payment': registers_not_in_payment,
        #'total_balance_per_floor': total_balance_per_floor,  # Add this to the context
    }

    #return render(request, 'list_register_test.html', context)
    return render(request, 'list_register_test_org.html', context)

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