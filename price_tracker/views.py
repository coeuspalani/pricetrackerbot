# tracker/views.py

from django.shortcuts import render
from django.http import HttpResponse
from tracker.models import TrackedProduct
import random
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        url = request.POST['url']
        price = request.POST['price']

        TrackedProduct.objects.create(
            email=email,
            product_url=url,
            target_price=price
        )

        messages.success(request, "Tracking Started! You'll be notified via email.")
        return redirect('index')

    return render(request, 'index.html')

