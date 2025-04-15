import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scorpy_tale.settings')
django.setup()

from flowers.models import Comment

def clear_all_comments():
    print("Clearing all comments from the database...")
    
    # Count comments before deleting
    comment_count = Comment.objects.count()
    
    # Delete all comments
    Comment.objects.all().delete()
    
    print(f"✓ Successfully deleted {comment_count} comments")
    print("All comments have been removed from the database.")

if __name__ == "__main__":
    clear_all_comments() 