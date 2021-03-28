from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q

# Create your view here.
class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self,request,*args,**kwargs):
        appetizers=MenuItem.objects.filter(category__name__contains='Appetizer')
        desserts=MenuItem.objects.filter(category__name__contains='Dessert')
        drinks=MenuItem.objects.filter(category__name__contains='Drink')
        entres=MenuItem.objects.filter(category__name__contains='Entre')

        print(appetizers)
        print(desserts)
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        return render(request, 'customer/order.html',context)
    
    def post(self,request,*args,**kwargs):
        order_items={
            'items':[]
        }

        items=request.POST.getlist('items[]')
        name=request.POST.get('name')
        email=request.POST.get('email')
        street = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')


        for item in items:
            menu_item=MenuItem.objects.get(pk__contains=int(item))
            item_data={
                'id':menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price,
            }

            order_items['items'].append(item_data)
        
        price=0
        item_ids=[]
        for i in order_items['items']:
            price+=i['price']
            item_ids.append(i['id'])

        
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # order=OrderModel.objects.create(price=price)
        # order.items.add(*item_ids)

        
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to user
        body = ('Thank you for your order!  Your food is being made and will be delivered soon!\n'
        f'Your total: {price}\n'
        'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )


        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)

class Menu(View):
    def get(self,request,*args,**kwargs):
        menu=MenuItem.objects.all()

        context={
            'menu': menu
        }

        return render(request,'customer/menu.html',context)

class MenuSearch(View):
    def get(self,request,*args,**kwargs):
        query=request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu': menu_items
        }
        return render(request, 'customer/menu.html', context)




