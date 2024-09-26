# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customers
from .serializers import CustomersSerializer
from .forms import CustomersForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


class UserCustomersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        customers = Customers.objects.filter(user=request.user)
        serializer = CustomersSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CustomersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customers = Customers.objects.filter(pk=pk, user=request.user).first()
        if customers:
            serializer = CustomersSerializer(customers)
            return Response(serializer.data)
        return Response(status=404)

    def put(self, request, pk):
        customers = Customers.objects.filter(pk=pk, user=request.user).first()
        if customers:
            serializer = CustomersSerializer(customers, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=404)

    def delete(self, request, pk):
        customers = Customers.objects.filter(pk=pk, user=request.user).first()
        if customers:
            customers.delete()
            return Response(status=204)
        return Response(status=404)


# Create customers
@login_required
def create_customers_view(request):
    if request.method == "POST":
        create_customers = CustomersForm(request.POST)
        if create_customers.is_valid():
            customers = create_customers.save(commit=False)
            customers.user = request.user
            customers.save()
            return redirect("user_customers_view")
        else:
            # return render(request, 'create_customers.html', {'form': create_customers})
            context = {
                "form": create_customers,
            }
            return render(request, "customers/create.html", context=context)
    else:
        create_customers = CustomersForm()
        context = {
            "form": create_customers,
        }
        return render(request, "customers/create.html", context=context)


# view customers
@login_required
def user_customers_view(request):
    customers = Customers.objects.filter(user=request.user)
    context = {
        "customers": customers,
    }
    return render(request, "customers/get_data.html", context=context)


# customers detail
@login_required
def detail_customers(request, pk):
    try:
        customers = Customers.objects.get(pk=pk, user=request.user)
        context = {
            "customers": customers,
        }
        return render(request, "customers/detail.html", context=context)
    except Customers.DoesNotExist:
        return redirect("user_customers_view")


# update customers
@login_required
def update_customers(request, pk):
    try:
        customers = Customers.objects.get(pk=pk, user=request.user)
        if request.method == "POST":
            update_form = CustomersForm(request.POST, instance=customers)
            if update_form.is_valid():
                update_form.save()
                return redirect("user_customers_view")
            else:
                context = {
                    "form": update_form,
                }
                return render(request, "customers/update.html", context=context)
        else:
            update_form = CustomersForm(instance=customers)
            context = {
                "form": update_form,
            }
            return render(request, "customers/update.html", context=context)
    except Customers.DoesNotExist:
        return redirect("user_customers_view")


# delete customers


@login_required
def delete_customers(request, pk):
    try:
        customers = Customers.objects.get(pk=pk, user=request.user)
        customers.delete()
        return redirect("user_customers_view")
    except Customers.DoesNotExist:
        return redirect("user_customers_view")
