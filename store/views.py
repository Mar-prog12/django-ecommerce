
from django.shortcuts import render, redirect
from .models import Product, Category
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def product_list(request):
    query = request.GET.get('q', '')  # Get search query
    category_filter = request.GET.get('category', '')  # Get selected category

    products = Product.objects.all()

    if category_filter:
        products = products.filter(category__name__iexact=category_filter.strip())  # Case-insensitive and strip spaces

    if query:
        products = products.filter(name__icontains=query)

    categories = Category.objects.all()  # Get all categories

    return render(request, "store/product_list.html", {
        "products": products,
        "categories": categories,
        "selected_category": category_filter,
        "query": query
    })


def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/product_list.html', {'products': products, 'query': query})

def add_to_cart(request, product_id):
    """Add a product to the cart (stored in session)."""
    product = Product.objects.get(id=product_id)

    # Get the cart from session, or create an empty one
    cart = request.session.get('cart', {})

    # Add or update the product quantity
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart  # Save cart in session
    return redirect('product_list')

def view_cart(request):
    """Display the shopping cart."""
    cart = request.session.get('cart', {})
    return render(request, 'store/cart.html', {'cart': cart})

def remove_from_cart(request, product_id):
    """Remove an item from the cart."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart  # Update session
    return redirect('view_cart')

def clear_cart(request):
    """Remove all items from the shopping cart."""
    request.session['cart'] = {}  # Set cart to an empty dictionary
    return redirect('view_cart')
from .models import Category

def categories_context(request):
    """Fetch categories for the navigation menu in all templates."""
    categories = Category.objects.all()
    return {'categories': categories}


def contact_page(request):
    """Handles Contact Form Submission"""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Message from {name}"
        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,  # Sender (your Gmail)
                [settings.RECIPIENT_EMAIL],  # Recipient (Marjola's email)
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

    return render(request, "store/contact.html")

