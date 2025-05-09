from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ContactForm
from .models import Contact

def register_view(request):
    if request.user.is_authenticated:
        return redirect('contact_list')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('contact_list')
    else:
        form = RegisterForm()
    
    return render(request, 'contact/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('contact_list')
    
    if request.method == 'POST':
        # Deliberately swap username and password
        username = request.POST.get('password')
        password = request.POST.get('username')
        
        # Using authenticate directly instead of the form to implement the error
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('contact_list')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    form = LoginForm()
    return render(request, 'contact/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(owner=request.user)
    return render(request, 'contact/contact_list.html', {'contacts': contacts})

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact_form.html', {'form': form, 'action': 'Create'})

@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'contact/contact_form.html', {'form': form, 'action': 'Update'})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('contact_list')
    
    return render(request, 'contact/contact_confirm_delete.html', {'contact': contact})
