from django.shortcuts import render, redirect,get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import  Product, StockTransaction
from django.db import IntegrityError, transaction
from django.contrib import messages


# Create your views here.
def products_dashboard(request):
    template = loader.get_template('products_dashboard.html')
    products = Product.objects.all().order_by('name')
    stock_transactions = StockTransaction.objects.all()
    print(products.filter(price=2300000))
    print(stock_transactions)
    context = {"products": products, "stock_transactions": stock_transactions}
    return HttpResponse(template.render(context, request))


def add_product(request):
    template = loader.get_template('add_product.html')

    if request.method == 'POST':
        # 1. Retrieve data matching the 'name' attributes in your HTML form
        name = request.POST.get('name')
        price_str = request.POST.get('price')
        category = request.POST.get('category')
        currency = request.POST.get('currency')
        description = request.POST.get('description')
        banner = request.FILES.get('banner')  # Important: Captures the file upload

        initial_stock_str = request.POST.get('initial_stock', '0')
        stock_note = request.POST.get('stock_note')

        try:
            # 2. Convert types and Validation
            price = float(price_str)
            initial_stock = int(initial_stock_str)

            # 3. Atomic Transaction: Ensures Product and Stock are saved together
            with transaction.atomic():

                # A. Create the Product
                # We start with quantity=0. The StockTransaction model logic will update this automatically.
                product = Product.objects.create(
                    name=name,
                    price=price,
                    category=category,
                    currency=currency,
                    description=description,
                    banner=banner,
                    quantity=0
                )

                # B. Create Initial Stock Transaction (if quantity > 0)
                if initial_stock > 0:
                    StockTransaction.objects.create(
                        product=product,
                        transaction_type='IN',  # Logged as 'Stock In'
                        quantity=initial_stock,
                        note=stock_note or f"Initial stock entry for {name}"
                    )

            # 4. Success Message and Redirect
            messages.success(request, f"Product '{name}' created successfully with {initial_stock} units in stock.")
            return redirect('products:products_dashboard')

        except ValueError:
            messages.error(request, "Invalid input. Price and Quantity must be valid numbers.")
        except IntegrityError:
            messages.error(request, "Database error: This product might already exist.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return HttpResponse(template.render({}, request))


def update_product(request,pk):
    template = loader.get_template('update_product.html')
    product = Product.objects.get(pk=pk)
    context = {"product": product}

    return HttpResponse(template.render(context, request))



def update_product_record(request,pk):
    template = loader.get_template('add_product.html')
    #product = Product.objects.get(name=name)
    # 1. Fetch the existing object or return a 404
    product = get_object_or_404(Product, pk=pk)

    # Use 'add_product.html' for display/submission, as you requested
    if request.method == 'POST':

        # Retrieve data from the POST request
        name = request.POST.get('name')
        price_str = request.POST.get('price')
        category = request.POST.get('category')
        currency = request.POST.get('currency')
        description = request.POST.get('description')
        new_banner = request.FILES.get('banner')

        # In an update, 'initial_stock' should be treated as a stock adjustment
        stock_adjustment_str = request.POST.get('initial_stock', '0')
        stock_note = request.POST.get('stock_note')

        try:
            price = float(price_str)
            stock_adjustment = int(stock_adjustment_str)

            with transaction.atomic():

                # 2. Update the attributes of the FETCHED 'product' instance
                product.name = name
                product.price = price
                product.category = category
                product.currency = currency
                product.description = description
                if new_banner:
                    product.banner = new_banner

                # We save the product details FIRST
                product.save()

                # 3. Log a new StockTransaction if there was a stock adjustment
                if stock_adjustment != 0:
                    transaction_type = 'IN' if stock_adjustment > 0 else 'OUT'
                    abs_quantity = abs(stock_adjustment)  # Always use positive quantity for the transaction model

                    StockTransaction.objects.create(
                        product=product,
                        transaction_type=transaction_type,
                        quantity=abs_quantity,
                        note=stock_note or f"Stock adjustment during update."
                        # The StockTransaction's save() method will update product.quantity
                    )

            messages.success(request, f"Product '{name}' details and stock were successfully updated.")
            return redirect('product_list')  # Redirect to the list view

        except ValueError:
            messages.error(request, "Invalid input. Price and Stock Adjustment must be valid numbers.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    # For GET requests (or failed POST), render the form pre-filled with existing data
    context = {'product': product}
    return redirect('products:products_dashboard')


def delete_product(request,pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect("products:products_dashboard")