from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import OrderModel
from django.utils.timezone import datetime
# Create your views here.

class Dashboard(LoginRequiredMixin, UserPassesTestMixin,View):
    def get(self,request,*args,**kwargs):
        today=datetime.today()
        orders=OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        tot=0
        unshipped=[]
        for i in orders:
            tot+=(i.price)
            if not i.is_shipped:
                unshipped.append(i)
        
        context = {
            'orders': orders,
            'total_revenue': tot,
            'total_orders': len(orders),
            'unshipped': unshipped
        }
        return render(request,'restaurant/dashboard.html',context)

    def test_func(self):
            return self.request.user.groups.filter(name='Staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order=OrderModel.objects.get(pk=pk)
        context={
            'order': order
        }

        return render(request, 'restaurant/order_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()
        
        context = {'order': order}
        return render(request, 'restaurant/order_detail.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()