from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import  Car, Service, Order, CarModel

def index(request):
    #return HttpResponse('Welcome to autoservice!')
    car_count = Car.objects.count()
    service_count = Service.objects.count()
    order_count = Order.objects.count()

    context = {
        'car_count':car_count,
        'service_count':service_count,
        'order_count': Order.objects.count()
    }

    return render(request, 'autoservice/index.html', context)

def cars(request):
    return render(request, 'autoservice/cars.html', {'cars': Car.objects.all()})

def car_info(request, car_id):
    return render(request, 'autoservice/car_info.html', {'car':get_object_or_404(Car, id=car_id)})


class OrderListView(ListView):
    model = Order 
    template_name = 'autoservice/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = self.get_queryset().count()
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'autoservice/order_detail.html'

