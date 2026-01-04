from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from inventory.models import Product
from orders.models import Order
from clients.models import Client

@login_required
def reports_view(request):
    # Get user's data
    products = Product.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    
    # Calculate metrics
    total_buying_cost = sum(p.total_buying_cost for p in products)
    total_revenue = orders.filter(status='done').aggregate(
        total=Sum('total_amount'))['total'] or 0
    total_shipping = orders.aggregate(total=Sum('shipping_cost'))['total'] or 0
    profit = total_revenue - total_buying_cost - total_shipping
    
    # Product statistics
    top_products = products.order_by('-pieces_sold')[:5]
    
    # Monthly statistics (simplified)
    monthly_orders = orders.filter(status='done').count()
    
    context = {
        'total_buying_cost': total_buying_cost,
        'total_revenue': total_revenue,
        'total_shipping': total_shipping,
        'profit': profit,
        'top_products': top_products,
        'monthly_orders': monthly_orders,
        'total_products': products.count(),
        'total_orders': orders.count(),
        'total_clients': Client.objects.filter(user=request.user).count(),
    }
    
    return render(request, 'reports/reports.html', context)
