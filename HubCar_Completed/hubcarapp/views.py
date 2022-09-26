from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hubcarapp.forms import UserForm, GarageForm, UserFormForEdit, ItemForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from hubcarapp.models import Item, Order, Driver

from django.db.models import Sum, Count, Case, When

# Create your views here.
def home(request):
    return redirect(garage_home)

@login_required(login_url='/garage/sign-in/')
def garage_home(request):
    return redirect(garage_order)

@login_required(login_url='/garage/sign-in/')
def garage_account(request):
    user_form = UserFormForEdit(instance = request.user)
    garage_form = GarageForm(instance = request.user.garage)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        garage_form = GarageForm(request.POST, request.FILES, instance = request.user.garage)

        if user_form.is_valid() and garage_form.is_valid():
            user_form.save()
            garage_form.save()

    return render(request, 'garage/account.html', {
        "user_form": user_form,
        "garage_form": garage_form
    })

@login_required(login_url='/garage/sign-in/')
def garage_item(request):
    items = Item.objects.filter(garage = request.user.garage).order_by("-id")
    return render(request, 'garage/item.html', {"items": items})

@login_required(login_url='/garage/sign-in/')
def garage_add_item(request):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.garage = request.user.garage
            item.save()
            return redirect(garage_item)

    return render(request, 'garage/add_item.html', {
        "form": form
    })

@login_required(login_url='/garage/sign-in/')
def garage_edit_item(request, item_id):
    form = ItemForm(instance = Item.objects.get(id = item_id))

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance = Item.objects.get(id = item_id))

        if form.is_valid():
            form.save()
            return redirect(garage_item)

    return render(request, 'garage/edit_item.html', {
        "form": form
    })


@login_required(login_url='/garage/sign-in/')
def garage_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], garage = request.user.garage)

        if order.status == Order.PREPARING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(garage = request.user.garage).order_by("-id")
    return render(request, 'garage/order.html', {"orders": orders})

@login_required(login_url='/garage/sign-in/')
def garage_report(request):
    # Calculate revenue and number of order by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    # Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            garage = request.user.garage,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 Items
    top3_items = Item.objects.filter(garage = request.user.garage)\
                     .annotate(total_order = Sum('orderdetails__quantity'))\
                     .order_by("-total_order")[:3]

    item = {
        "labels": [item.name for item in top3_items],
        "data": [item.total_order or 0 for item in top3_items]
    }

    # Top 3 Drivers
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order__garage = request.user.garage, then = 1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'garage/report.html', {
        "revenue": revenue,
        "orders": orders,
        "item": item,
        "driver": driver
    })

def garage_sign_up(request):
    user_form = UserForm()
    garage_form = GarageForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        garage_form = GarageForm(request.POST, request.FILES)

        if user_form.is_valid() and garage_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_garage = garage_form.save(commit=False)
            new_garage.user = new_user
            new_garage.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(garage_home)

    return render(request, "garage/sign_up.html", {
        "user_form": user_form,
        "garage_form": garage_form
    })
