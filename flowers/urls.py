from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    FlowerListView,
    CategoryFlowerListView,
    FlowerDetailView,
    FlowerCreateView,
    FlowerUpdateView,
    FlowerDeleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('flowers/', FlowerListView.as_view(), name='flower-list'),
    path('category/<int:category_id>/', CategoryFlowerListView.as_view(), name='category-flowers'),
    path('flower/<int:pk>/', FlowerDetailView.as_view(), name='flower-detail'),
    path('flower/new/', FlowerCreateView.as_view(), name='flower-create'),
    path('flower/<int:pk>/update/', FlowerUpdateView.as_view(), name='flower-update'),
    path('flower/<int:pk>/delete/', FlowerDeleteView.as_view(), name='flower-delete'),
    path('flower/<int:flower_id>/add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('flower/<int:flower_id>/update-cart/', views.update_cart, name='update-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order-confirmation'),
    path('comments/', views.add_comment, name='comments'),
    path('profile/', views.profile, name='profile'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='flowers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='flowers/logout.html', http_method_names=['get', 'post']), name='logout'),
] 