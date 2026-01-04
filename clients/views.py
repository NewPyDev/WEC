from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client

@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    orders = client.orders.all()
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'orders': orders
    })
