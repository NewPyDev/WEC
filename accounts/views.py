from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from inventory.models import Product
from orders.models import Order
from clients.models import Client

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    # Get statistics for the dashboard
    products = Product.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    clients = Client.objects.filter(user=request.user)
    
    # Calculate statistics
    total_products = products.count()
    low_stock_products = products.filter(pieces_left__lte=10).count()
    
    # Order statistics
    processing_orders = orders.filter(status='processing').count()
    completed_orders = orders.filter(status='done').count()
    cancelled_orders = orders.filter(status='cancelled').count()
    
    # Revenue calculations
    total_revenue = orders.filter(status='done').aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    # Calculate total inventory value
    inventory_value = sum(
        p.pieces_left * p.buying_price_per_piece for p in products
    )
    
    # Recent orders
    recent_orders = orders.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
        'inventory_value': inventory_value,
        'total_clients': clients.count(),
        'recent_orders': recent_orders,
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})
