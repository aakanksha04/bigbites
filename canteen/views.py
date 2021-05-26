from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from . utils import *

# Create your views here.
def adminpanel(request):

    orders = Order.objects.all()
    orderItems = OrderItem.objects.all()

    for order in orders:
        for item in orderItems:
            print(order.product)
            if order.product == item:
                print(item) 
    context = {'orders':orders}

    return render(request, 'canteen/admin-panel.html', context)

    # def test_func(self):
    #     return self.request.user.groups.filter(name='Staff').exists()


# ------------------------------------------------------------------------------------------
def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request,'canteen/store.html',context)

def cart(request):

    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'canteen/cart.html',context)

def checkout(request):

    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'canteen/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId =  data['productId']
    action = data['action']
    print('action: ',action)
    print('ProductId: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer, complete=False) 

    orderItem ,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity-1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False) 
        
    else:
        print("user is not logged in..")
        customer, order = guestOrder(request, data)
        print('COOKIES: ',request.COOKIES)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    ShippingTo.objects.create(
    customer=customer,
    order=order,
    # address=data['shipping']['address'],
    # city=data['shipping']['city'],
    # state=data['shipping']['state'],
    roll_no=data['shipping']['zipcode'],
    )   

    return JsonResponse('Payment submitted...',safe=False)