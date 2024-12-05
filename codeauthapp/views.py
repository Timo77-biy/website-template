from __future__ import unicode_literals
from .models import Product
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.shortcuts import render, redirect
from django.contrib import messages




def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})

from django.shortcuts import render
from django.http import JsonResponse
import requests

def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Erick were",
            "TransactionDesc": "Web Development Charges"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()

        # Check for successful response (adjust according to Safaricom API documentation)
        if response.status_code == 200 and response_data.get("ResponseCode") == "0":
            # Payment processed successfully
            context = {
                "payment_success": True,
                "phone": phone,
                "amount": amount
            }
        else:
            # Payment failed
            context = {
                "payment_success": False,
                "error_message": response_data.get("errorMessage", "Payment failed. Please try again."),
                "phone": phone,
                "amount": amount
            }

        return render(request, 'pay.html', context)

    return render(request, 'pay.html')




def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('user-login')

@login_required
def add_product(request):
    if request.method == "POST":
        prod_name = request.POST.get("p-name")
        prod_quantity = request.POST.get("p-qtty")
        prod_size = request.POST.get("p-size")
        prod_price = request.POST.get("p-price")
        context = {
            "prod_name": prod_name,
            "prod_quantity": prod_quantity,
            "prod_size": prod_size,
            "prod_price": prod_price,
            "success": "Data saved successfully"
        }
        query = Product(name=prod_name, qtty=prod_quantity,
                        size=prod_size, price=prod_price)
        query.save()
        return render(request, 'add-product.html', context)
    return render(request, 'add-product.html')


@login_required
def products(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, 'products.html', context)


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('all-products')


@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    if request.method == "POST":
        updated_name = request.POST.get('p-name')
        updated_qtty = request.POST.get('p-qtty')
        updated_size = request.POST.get('p-size')
        updated_price = request.POST.get('p-price')
        product.name = updated_name
        product.qtty = updated_qtty
        product.size = updated_size
        product.price = updated_price
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('all-products')
    return render(request, 'update-product.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            return redirect('user-registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def shop(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, 'shop.html', context)


    mpesa_client = MpesaClient()
    stk_push_callback_url = 'https://api.darajambili.com/express-payment'





# Contact page view
def contact(request):
    return render(request, 'contact.html')


