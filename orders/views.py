from django.shortcuts import render, redirect
from  django.template import loader
from django.http import HttpResponse
from .models import Customer, Order, OrderItem, Operator
from products.models import Product
from django.contrib import messages
from django.db import transaction

# Create your views here.
def orders_dashboard(request):
    template = loader.get_template('orders_dashboard.html')
    custormer = Customer.objects.all()
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    operators = Operator.objects.all()

    context = {"custormer": custormer,"orders": orders,"orderitems": orderitems,"operators": operators}

    return HttpResponse(template.render(context, request))

def orders_details(request):
    templates = loader.get_template('orders_details.html')
    return HttpResponse(templates.render({}, request))


def create_order(request):
    template = loader.get_template('create_orders.html')
    custormer = Customer.objects.all()
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    operators = Operator.objects.all()
    products = Product.objects.all().order_by('name')
    context ={"products": products, "orders": orders, "orderitems": orderitems, "operators": operators}

    if request.method == 'POST':
        try:
            # 1. Extract Customer and Shipping Data (Simple Fields)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')

            address_line_1 = request.POST.get('address_line_1')
            address_line_2 = request.POST.get('address_line_2', '')  # Optional
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip_code')
            country = request.POST.get('country')

            # Convert shipping cost to decimal/float
            try:
                shipping_cost = float(request.POST.get('shipping_cost', 0))
            except ValueError:
                shipping_cost = 0.00

            # 2. Extract Dynamic Product Line Items using an index loop
            order_items_data = []
            item_index = 0

            while True:
                product_id_key = f'products[{item_index}][id]'
                product_id = request.POST.get(product_id_key)

                # Stop the loop if the primary identifier for the line item is missing
                if product_id is None:
                    break

                quantity = request.POST.get(f'products[{item_index}][quantity]')
                price_snapshot = request.POST.get(f'products[{item_index}][price_snapshot]')

                # --- Data Cleaning and Validation ---
                try:
                    product_id_int = int(product_id)
                    quantity_int = int(quantity)
                    price_snapshot_float = float(price_snapshot)
                except (TypeError, ValueError) as e:
                    messages.error(request, f"Validation failed for product item {item_index + 1}: {e}")
                    item_index += 1
                    continue

                if quantity_int <= 0:
                    messages.error(request, f"Quantity must be positive for product item {item_index + 1}.")
                    item_index += 1
                    continue

                # --- REAL-TIME DATABASE ACCESS & VALIDATION ---
                try:
                    # UNCOMMENT THIS AND THE MODEL IMPORT WHEN YOUR DB IS READY
                    db_product = Product.objects.get(pk=product_id_int)

                    # TEMPORARY PLACEHOLDER for logic flow:
                    db_product = {'name': f'Product {product_id_int}'}

                    order_items_data.append({
                        'product_id': product_id_int,
                        'product_name': db_product.get('name'),  # Use name from fetched object
                        'price_snapshot': price_snapshot_float,
                        'quantity': quantity_int,
                        'line_total': price_snapshot_float * quantity_int
                    })
                # except Product.DoesNotExist: # UNCOMMENT when ORM is active
                except Exception:
                    messages.error(request, f"Product ID {product_id_int} not found in database.")

                item_index += 1

            # --- 3. Business Logic: Create 1 Order Per Product Item ---

            if not order_items_data:
                messages.error(request, "Order creation failed: No valid product items were submitted.")
                return redirect('orders:create_orders')  # Redirect back to the form

            # Use a transaction to ensure all related orders are saved or none are
            with transaction.atomic():
                total_orders_created = 0
                for item in order_items_data:
                    # --- DB SAVING LOGIC (Using ORM Placeholders) ---

                    # 1. Save Customer (or retrieve existing)
                    customer, created = Customer.objects.get_or_create(
                        email=email,address=address_line_1,
                        defaults={'first_name': first_name, 'last_name': last_name}
                    )

                    # 2. Calculate Total (Item Cost + Shipping)
                    order_total = item['line_total'] + shipping_cost

                    # 3. Create the Order object
                    order = Order.objects.create(
                        customer=customer,
                        total_amount=order_total,
                        shipping_cost=shipping_cost,

                        # ... other shipping fields ...
                    )

                    # 4. Create the OrderItem object for this specific product
                    OrderItem.objects.create(
                        order=order,
                        product_id=item['product_id'],
                        quantity=item['quantity'],
                        price=item['price_snapshot']
                    )

                    # MOCK LOGGING
                    print(f"DB ACTION: Created Order for Product: {item['product_name']} (Total: ${order_total:.2f})")

                    total_orders_created += 1

            messages.success(request, f"Successfully created {total_orders_created} order(s).")
            # Redirect to the dashboard or a success page
            return redirect('orders:orders_dashboard')

        except Exception as e:
            messages.error(request, f"A system error occurred during order processing: {e}")
            print(f"Critical error: {e}")
            return redirect('orders:create_orders')  # Redirect back to the form

    else:
        pass
    return HttpResponse(template.render(context, request))



