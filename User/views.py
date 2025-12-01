from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home_page(request):
    template = loader.get_template("home.html")
    context = {}
    return HttpResponse(template.render({},request))# render(request,"templates/home.html")#

def about_page(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({},request))


def login_page(request):
    template = loader.get_template('login.html')
    """
    Handles user authentication for the login page.
    Checks the provided credentials against the Django database.
    """
    if request.method == 'POST':
        # --- 1. Get Form Data ---
        username = request.POST.get('username')
        password = request.POST.get('password')

        # --- 2. Attempt Authentication (REAL DB CHECK) ---
        # authenticate() checks the credentials against the database using Django's backend settings.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful

            # --- 3. Log the user in and establish a session ---
            login(request, user)
            print(f"User {username} successfully logged in and session established.")

            # --- 4. Redirect on Success ---
            # Flashing a success message is optional but good practice
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('orders_dashboard')
        else:
            # Authentication failed (User does not exist or password was incorrect)
            # --- Use messages.error to flash the message ---
            messages.error(request, "Invalid credentials. Please check your email and password.")
            print(f"Login failed for user: {username} (Credentials mismatch)")

            # Re-render the login template, but now without passing the error message via context.
            # We still pass last_username to pre-fill the form.
            context = {
                'last_username': username  # Pre-fill the username field
            }
            # Note: The template must be updated to display messages using the {% for message in messages %} loop.
            return render(request, 'login.html', context)

    return HttpResponse(template.render({},request))
