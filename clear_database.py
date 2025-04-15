import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scorpy_tale.settings')
django.setup()

from django.contrib.auth.models import User
from flowers.models import UserProfile, Customer, Order, OrderItem, Comment

def clear_database_except_flowers():
    print("Clearing database while preserving Flower and Category models...")
    
    # Clear Comments
    comment_count = Comment.objects.count()
    Comment.objects.all().delete()
    print(f"✓ Deleted {comment_count} comments")
    
    # Clear OrderItems and Orders
    order_item_count = OrderItem.objects.count()
    OrderItem.objects.all().delete()
    print(f"✓ Deleted {order_item_count} order items")
    
    order_count = Order.objects.count()
    Order.objects.all().delete()
    print(f"✓ Deleted {order_count} orders")
    
    # Clear Customer profiles
    customer_count = Customer.objects.count()
    Customer.objects.all().delete()
    print(f"✓ Deleted {customer_count} customer profiles")
    
    # Clear UserProfiles
    profile_count = UserProfile.objects.count()
    UserProfile.objects.all().delete()
    print(f"✓ Deleted {profile_count} user profiles")
    
    # Don't delete the superuser, just regular users
    user_count = User.objects.filter(is_superuser=False).count()
    User.objects.filter(is_superuser=False).delete()
    print(f"✓ Deleted {user_count} regular users (preserved superuser accounts)")
    
    print("\nDatabase has been cleared while preserving Flower and Category models!")
    print("You can continue using the application with your existing flowers and categories.")

if __name__ == "__main__":
    clear_database_except_flowers() 