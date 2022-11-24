from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from . models import  Car, Service, Order, CarModel, OrderLine
from . import models
from . forms import OrderReviewForm
from django.urls import reverse, reverse_lazy

def index(request):
    return render(request, 'autoservice/index.html', {
        'cars_count': models.Car.objects.count(),
        'services_count': models.Service.objects.count(),
        'orders_count': models.Order.objects.count(),
    })

def index(request):
    car_count = Car.objects.count()
    service_count = Service.objects.count()
    order_count = Order.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    context = {
        'car_count':car_count,
        'service_count':service_count,
        'order_count': Order.objects.count(),
        'visits_count': visits_count, 
    }

    return render(request, 'autoservice/index.html', context)

def cars(request):
    car_list = models.Car.objects.all()
    search = request.GET.get('search')
    if search:
        print(search)
        car_list = car_list.filter(
            Q(client__icontains=search) |
            Q(plate__icontains=search) |
            Q(car_model__make__icontains=search) |
            Q(car_model__model__icontains=search)
        )
    paginator = Paginator(car_list, 2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'autoservice/cars.html', {'cars': paged_cars})

def car_info(request, car_id):
    return render(request, 'autoservice/car_info.html', {'car':get_object_or_404(Car, id=car_id)}
    )



class OrderListView(ListView):
    model = Order 
    paginate_by = 2
    template_name = 'autoservice/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = self.get_queryset().count()
        return context


class OrderDetailView(FormMixin, DetailView):
    model = Order
    form_class = OrderReviewForm
    template_name = 'autoservice/order_detail.html'

    def get_initial(self):
        return {
            'order': self.get_object(),
            'user': self.request.user
        }

    def post(self, *args, **kwargs):
        self.object = self.get_object() 
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Review posted')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('order', kwargs={'pk':self.object.id})

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'autoservice/user_order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-date')
        return queryset  
        
class UserOrderCreateView(CreateView):
    model = Order
    fields = ('car', 'estimate_date')
    template_name = 'autoservice/user_order_create.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
        
