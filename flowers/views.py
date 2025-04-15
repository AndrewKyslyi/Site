from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Category, Flower, Order, OrderItem, Comment, UserProfile
from .forms import CommentForm, FlowerForm
from django.conf import settings
from django.utils.translation import get_language
from django.urls import reverse
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'flowers/register.html', {'form': form, 'title': 'Register'})

def home(request):
    """Home page view"""
    # Get all featured flowers regardless of language
    featured_flowers = Flower.objects.filter(is_featured=True)[:6]
    
    categories = Category.objects.all()[:6]  # Get first 6 categories
    current_language = get_language()
    
    context = {
        'featured_flowers': featured_flowers,
        'categories': categories,
        'current_language': current_language
    }
    return render(request, 'flowers/home.html', context)

def about(request):
    return render(request, 'flowers/about.html', {'title': 'About Us'})

def contact(request):
    return render(request, 'flowers/contact.html', {'title': 'Contact Us'})

class FlowerListView(ListView):
    model = Flower
    template_name = 'flowers/flower_list.html'
    context_object_name = 'flowers'
    ordering = ['-date_added']
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Flowers'
        context['categories'] = Category.objects.all()
        return context

class CategoryFlowerListView(ListView):
    model = Flower
    template_name = 'flowers/category_flowers.html'
    context_object_name = 'flowers'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        return Flower.objects.filter(category=self.category).order_by('-date_added')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.category.name} Flowers'
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

class FlowerDetailView(DetailView):
    model = Flower
    template_name = 'flowers/flower_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['comments'] = Comment.objects.all().order_by('-date_posted')
        context['comment_form'] = CommentForm()
        return context

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('comments')
    else:
        form = CommentForm()
    
    comments = Comment.objects.all().order_by('-date_posted')
    context = {
        'title': 'Comments',
        'form': form,
        'comments': comments
    }
    return render(request, 'flowers/comments.html', context)

@login_required
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    
    # Get or create cart in session
    cart = request.session.get('cart', {})
    flower_id_str = str(flower_id)
    
    # Add or increment quantity
    if flower_id_str in cart:
        cart[flower_id_str]['quantity'] += 1
    else:
        cart[flower_id_str] = {
            'quantity': 1,
            'price': str(flower.price)
        }
    
    request.session['cart'] = cart
    messages.success(request, f'Added {flower.name} to your cart!')
    return redirect('flower-detail', pk=flower_id)

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for flower_id, item_data in cart.items():
        flower = get_object_or_404(Flower, id=int(flower_id))
        quantity = item_data['quantity']
        price = float(item_data['price'])
        subtotal = quantity * price
        total += subtotal
        
        cart_items.append({
            'flower': flower,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })
    
    context = {
        'title': 'Shopping Cart',
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'flowers/cart.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart')
        
        # Create order
        total_price = sum(
            float(item_data['price']) * item_data['quantity']
            for item_data in cart.values()
        )
        
        order = Order.objects.create(
            customer=request.user,
            total_price=total_price,
            shipping_address=request.POST.get('shipping_address')
        )
        
        # Create order items
        for flower_id, item_data in cart.items():
            flower = get_object_or_404(Flower, id=int(flower_id))
            OrderItem.objects.create(
                order=order,
                flower=flower,
                quantity=item_data['quantity'],
                price=float(item_data['price'])
            )
            
            # Update stock
            flower.stock -= item_data['quantity']
            flower.save()
        
        # Clear cart
        request.session['cart'] = {}
        
        messages.success(request, 'Ваше замовлення успішно оформлено!')
        return redirect('order-confirmation', order_id=order.id)
    
    return render(request, 'flowers/checkout.html', {'title': 'Checkout'})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'title': 'Order Confirmation',
        'order': order,
        'order_items': order_items
    }
    return render(request, 'flowers/order_confirmation.html', context)

class FlowerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Flower
    form_class = FlowerForm
    template_name = 'flowers/flower_form.html'
    success_url = '/'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Flower'
        return context

class FlowerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Flower
    form_class = FlowerForm
    template_name = 'flowers/flower_form.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Flower'
        return context
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class FlowerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Flower
    template_name = 'flowers/flower_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('flower-list')  # Default to flower list if no next URL

# User profile view
@login_required
def profile(request):
    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile information
        profile.full_name = request.POST.get('full_name', '')
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.bio = request.POST.get('bio', '')
        
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Save changes
        profile.save()
        user.save()
        
        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')
    
    context = {
        'title': 'My Profile',
        'profile': profile
    }
    return render(request, 'flowers/profile.html', context)

@login_required
def update_cart(request, flower_id):
    if request.method == 'POST':
        flower = get_object_or_404(Flower, id=flower_id)
        action = request.POST.get('action', '')
        
        # Get cart from session
        cart = request.session.get('cart', {})
        flower_id_str = str(flower_id)
        
        if flower_id_str in cart:
            # Handle different actions
            if action == 'increment':
                # Make sure we don't exceed stock
                if cart[flower_id_str]['quantity'] < flower.stock:
                    cart[flower_id_str]['quantity'] += 1
            elif action == 'decrement':
                if cart[flower_id_str]['quantity'] > 1:
                    cart[flower_id_str]['quantity'] -= 1
                else:
                    # Remove item if quantity reaches 0
                    del cart[flower_id_str]
            elif action == 'remove':
                del cart[flower_id_str]
            
            # Update session
            request.session['cart'] = cart
            
            # Calculate new subtotal and total
            if flower_id_str in cart:
                subtotal = float(cart[flower_id_str]['price']) * cart[flower_id_str]['quantity']
            else:
                subtotal = 0
                
            total = sum(
                float(item_data['price']) * item_data['quantity']
                for item_data in cart.values()
            )
            
            return JsonResponse({
                'success': True,
                'subtotal': subtotal,
                'total': total,
                'quantity': cart.get(flower_id_str, {}).get('quantity', 0)
            })
            
    return JsonResponse({'success': False}, status=400)
