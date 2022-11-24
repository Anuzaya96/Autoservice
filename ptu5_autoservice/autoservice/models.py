from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from tinymce.models import HTMLField
from django.utils.timezone import datetime


class CarModel(models.Model):
    YEARS_CHOICES = ((year, str(year)) for year in reversed(range(1899, date.today().year+1)))

    make = models.CharField(_("make"), max_length=50)
    model = models.CharField(_("model"), max_length=50)
    year = models.IntegerField(_("year"), choices=YEARS_CHOICES)
    engine = models.CharField(_("engine"), max_length=50)
    

    def __str__(self) -> str:
        return f"{self.make} {self.model} ({self.year}), {self.engine}"

    # class Meta:
    #     ordering = ['make', 'model', 'year', 'engine']
    #     verbose_name = "model"
    #     verbose_name_plural = "models"


class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel, 
        verbose_name=_("car model"), 
        on_delete=models.CASCADE,
        related_name='cars',
    )
    plate = models.CharField(_("license plate"), max_length=10)
    vin = models.CharField(_("VIN number"), max_length=30)
    client = models.CharField(_("client name"), max_length=100)
    non_standart_parts = HTMLField(_('non standart parts'), blank=True, null=True)

    cover = models.ImageField(_("cover"), upload_to="covers", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.car_model.make} {self.car_model.model}, {self.plate}, {self.client}"


class Service(models.Model):
    name = models.CharField(_("name"), max_length=50)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('n', _('new')),
        ('a', _('advance payemnt taken')),
        ('o', _('ordered parts')),
        ('w', _('working')),
        ('d', _('done')),
        ('c', _('cancelled')),
        ('p', _('paid')),
    )
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    total = models.DecimalField(_("total amount"), max_digits=18, decimal_places=2, default=0)
    date = models.DateField(_("date"), auto_now_add=True)
    status = models.CharField(_("status"), max_length=1, choices=STATUS_CHOICES, default='n')
    estimate_date = models.DateField(_("estimate date"), null=True, blank=True)

    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("user"),
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
    )

    return_date = models.DateField('return date', null=True, blank=True)

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total
        return total

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.total = self.get_total()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.date}: {self.total}"

    @property
    def is_overdue(self):
        if self.return_date and self.return_date < datetime.date(datetime.now()):
            return True
        return False



class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='order_lines',
    )
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service"), 
        on_delete=models.CASCADE,
        related_name='order_lines',
    )
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.save()

    def __str__(self) -> str:
        return f"{self.service.name}: {self.quantity} x {self.price}"


class OrderReview(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE, related_name='order_reviews')
    notes = models.TextField(_('notes'), max_length=10000)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self):
        return f"{self.order} {self.user}"
