from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from decimal import Decimal
import qrcode
import io
import base64
from datetime import datetime, timedelta
from .models import Order, OrderItem
from clients.models import Client
from inventory.models import Product
from .forms import OrderForm, OrderItemFormSet, OrderStatusForm

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, status='processing')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).exclude(status='processing')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                # Create or get client
                client = None
                if form.cleaned_data.get('client'):
                    client = form.cleaned_data['client']
                elif form.cleaned_data.get('new_client_name') and form.cleaned_data.get('new_client_phone'):
                    # Create new client
                    client = Client.objects.create(
                        user=request.user,
                        name=form.cleaned_data['new_client_name'],
                        phone=form.cleaned_data['new_client_phone'],
                        address=form.cleaned_data.get('new_client_address', ''),
                        email=form.cleaned_data.get('new_client_email', '')
                    )
                
                if not client:
                    messages.error(request, 'Please select an existing client or provide new client information.')
                    return render(request, 'orders/order_create.html', {
                        'form': form,
                        'products': Product.objects.filter(user=request.user)
                    })
                
                # Create order
                order = form.save(commit=False)
                order.user = request.user
                order.client = client
                order.total_amount = Decimal('0.00')  # Will be calculated from items
                order.save()
                
                # Handle order items from POST data
                total_amount = Decimal('0.00')
                product_ids = request.POST.getlist('product_id[]')
                quantities = request.POST.getlist('quantity[]')
                prices = request.POST.getlist('price[]')
                
                for i in range(len(product_ids)):
                    if product_ids[i] and quantities[i] and prices[i]:
                        try:
                            product = Product.objects.get(id=product_ids[i], user=request.user)
                            quantity = int(quantities[i])
                            price = Decimal(prices[i])
                            
                            # Check if enough stock
                            if product.pieces_left < quantity:
                                messages.error(request, f'Not enough stock for {product.name}. Available: {product.pieces_left}')
                                order.delete()
                                return render(request, 'orders/order_create.html', {
                                    'form': form,
                                    'products': Product.objects.filter(user=request.user)
                                })
                            
                            # Create order item
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                price=price
                            )
                            
                            total_amount += quantity * price
                            
                        except (Product.DoesNotExist, ValueError):
                            continue
                
                # Update order total
                order.total_amount = total_amount
                order.save()
                
                messages.success(request, f'Order #{order.id} created successfully!')
                return redirect('order_detail', pk=order.pk)
    
    else:
        form = OrderForm(user=request.user)
    
    products = Product.objects.filter(user=request.user, pieces_left__gt=0)
    return render(request, 'orders/order_create.html', {
        'form': form,
        'products': products
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        # Allow all valid status choices
        valid_statuses = ['processing', 'cancelled', 'done']
        if new_status in valid_statuses:
            old_status = order.status
            order.status = new_status
            order.save()  # This will trigger inventory update if status is 'done'
            
            if new_status == 'done':
                messages.success(request, f'Order #{order.id} marked as done! Inventory has been updated.')
            else:
                messages.success(request, f'Order status updated from {old_status.title()} to {new_status.title()}')
        else:
            messages.error(request, 'Invalid status selected')
    return redirect('order_detail', pk=pk)

@login_required
def order_shipping_label(request, pk):
    """Generate printable shipping label with QR code"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    # Generate QR code with order information
    qr_data = f"Order #{order.id}\nClient: {order.client.name}\nPhone: {order.client.phone}\nTotal: ${order.grand_total}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Suggested shipping date (3 days from now)
    shipping_date = datetime.now() + timedelta(days=3)
    
    # Get company name from user profile - use actual company name, not shipping company
    company_name = order.user.company_name or 'YOUR COMPANY NAME'
    
    context = {
        'order': order,
        'qr_code_base64': qr_code_base64,
        'shipping_date': shipping_date,
        'print_date': datetime.now(),
        'company_name': company_name,
    }
    
    return render(request, 'orders/shipping_label.html', context)

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

@login_required
def order_invoice_pdf(request, pk):
    """Generate PDF invoice"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    # Render template
    template_path = 'orders/invoice_pdf.html'
    context = {
        'order': order,
        'user': request.user,
        'company_logo': request.user.company_logo.url if request.user.company_logo else None,
    }
    
    # Create a file-like buffer to receive PDF data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    
    # Find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
    # Create PDF
    pisa_status = pisa.CreatePDF(
       html, dest=response)
       
    # If error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
