from django.contrib import admin
from .models import Operator, Customer, Order, OrderItem

# Define a simple inline for OrderItem to be displayed within the Order admin page
class OrderItemInline(admin.TabularInline):
    """Inline view for order items within the main Order admin view."""
    model = OrderItem
    extra = 0 # Don't show extra empty forms by default
    fields = ['product', 'quantity', 'price']
    readonly_fields = ['price'] # Price snapshot should not be edited after creation

# Define the Order Admin view
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Custom admin display for the Order model."""
    list_display = ('id', 'customer', 'operator', 'order_date', 'status', 'total_amount', 'get_customer_email')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'id')
    inlines = [OrderItemInline]
    date_hierarchy = 'order_date'
    readonly_fields = ('order_date', 'total_amount', 'shipping_cost')
    # Use fieldsets to organize the display (optional but recommended)
    fieldsets = (
        (None, {
            'fields': ('customer', 'operator', 'status', 'total_amount', 'shipping_cost')
        }),
        ('Dates', {
            'fields': ('order_date',),
            'classes': ('collapse',)
        }),
    )

    def get_customer_email(self, obj):
        return obj.customer.email
    get_customer_email.short_description = 'Customer Email'


# Register remaining models
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    """Custom admin display for the Operator model."""
    list_display = ('user', 'full_name', 'contact_number')
    search_fields = ('full_name', 'user__username')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Custom admin display for the Customer model."""
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email', 'phone')