from django.shortcuts import render, redirect
from django.http import HttpResponse
from http import HTTPStatus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View

from .models import Meal, OrderTransction
from .forms import UserLoginForms

# Create your views here.

def error_404_view(request, exception):
   return redirect('index')

class IndexVeiw(View):
   def get(self, request):
      if request.method == 'GET':
         meals = []
         temp_list = []
         all_meals = Meal.objects.all()

      for cnt in range(all_meals.count()):
         temp_list.append(all_meals[cnt])

         if (cnt +1) % 3 == 0 and cnt + 1 > 2:
            meals.append(temp_list)
            temp_list = []

      if temp_list:
         meals.append(temp_list)

      context = {
         "meals": meals,
      }

      return render(request=request, template_name='restaurant/index.html', context=context)


class OrderView(View):
   def get(self, request, pk=None):
      if pk:
         got_meal = Meal.objects.filter(id=pk).last()

         if got_meal and got_meal.stock > 0:
            OrderTransction.objects.create(
               meal=got_meal, customer=request.user, amount=got_meal.price
            )
            got_meal.stock -= 1

            got_meal.save()

            return redirect("index")

      return HttpResponse(HTTPStatus.BAD_REQUEST)


class DetailsView(View):
   def get(self, request):
      transactions = OrderTransction.objects.filter(customer=request.user)

      context = {
         "transactions": transactions,
      }

      return render(request=request, template_name="restaurant/detail.html", context=context)


class CustomLoginView(View):
   form_class = UserLoginForms
   template_name = "restaurant/login.html"

   def get(self, request):
      form = self.form_class()

      form.fields['password'].widget.attrs['placeholder'] = 'your password'

      context = {
         'login_form': form,
      }

      return render(request=request, template_name=self.template_name, context=context)

   def post(self, request):
      form = self.form_class(request.POST, request.FILES)

      if form.is_valid():
         username = form.cleaned_data.get('username')
         password = form.cleaned_data.get('password')

         authenticateuser = authenticate(request, username=username, password=password)
         if authenticateuser is not None:
            login(request, authenticateuser)
            return redirect('details')

         form.add_error('username', 'wrong username and password')
         form.add_error('password', 'wrong username and password')

      context = {
         'login_form': form,
      }

      return render(request=request, template_name=self.template_name, context=context)



def logout_user(request):
   logout(request)

   return redirect('index')