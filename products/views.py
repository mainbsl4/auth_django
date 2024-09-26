# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


class UserProductsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = Product.objects.filter(pk=pk, user=request.user).first()
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        return Response(status=404)

    def put(self, request, pk):
        product = Product.objects.filter(pk=pk, user=request.user).first()
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=404)

    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk, user=request.user).first()
        if product:
            product.delete()
            return Response(status=204)
        return Response(status=404)


# Create product
@login_required
def create_product_view(request):
    if request.method == "POST":
        create_product = ProductForm(request.POST)
        if create_product.is_valid():
            product = create_product.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("user_products_view")
        else:
            # return render(request, 'create_product.html', {'form': create_product})
            context = {
                "form": create_product,
            }
            return render(request, "products/create.html", context=context)
    else:
        create_product = ProductForm()
        context = {
            "form": create_product,
        }
        return render(request, "products/create.html", context=context)


# view product
@login_required
def user_products_view(request):
    products = Product.objects.filter(user=request.user)
    context = {
        "products": products,
    }
    return render(request, "products/get_data.html", context=context)


# product detail
@login_required
def detail_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
        context = {
            "product": product,
        }
        return render(request, "products/detail.html", context=context)
    except Product.DoesNotExist:
        return redirect("user_products_view")


# update product
@login_required
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
        if request.method == "POST":
            update_form = ProductForm(request.POST, instance=product)
            if update_form.is_valid():
                update_form.save()
                return redirect("user_products_view")
            else:
                context = {
                    "form": update_form,
                }
                return render(request, "products/update.html", context=context)
        else:
            update_form = ProductForm(instance=product)
            context = {
                "form": update_form,
            }
            return render(request, "products/update.html", context=context)
    except Product.DoesNotExist:
        return redirect("user_products_view")


# delete product


@login_required
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
        product.delete()
        return redirect("user_products_view")
    except Product.DoesNotExist:
        return redirect("user_products_view")
