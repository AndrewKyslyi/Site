# Scorpy Tale - Flower Shop

A beautiful flower shop website built with Django, featuring a dark mode theme and international language support.

## Features

- Responsive design with Bootstrap
- Dark/Light theme toggle
- Ukrainian language support with full translations
- Product catalog with categories
- User authentication and profiles
- Shopping cart and checkout functionality
- Comment system

## Internationalization

The application fully supports the following languages:
- English (default)
- Ukrainian (complete translations)

### Language Switching

The website includes a language switcher in the top navigation bar allowing users to easily switch between English and Ukrainian. All UI elements, product descriptions, and content are available in both languages.

For products, Ukrainian descriptions can be added separately in the admin panel, and they will automatically be displayed when Ukrainian language is selected.

### Working with Translations

1. Make sure you have GNU gettext tools installed:
   - For Windows: Download and install from https://mlocati.github.io/articles/gettext-iconv-windows.html
   - For Ubuntu/Debian: `sudo apt-get install gettext`
   - For macOS: `brew install gettext`

2. Extract messages for translation:
   ```
   python manage.py makemessages -l uk
   ```

3. Edit the translation files in `locale/uk/LC_MESSAGES/django.po`

4. Compile messages:
   ```
   python manage.py compilemessages
   ```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/scorpy-tale.git
   cd scorpy-tale
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Theme Support

The website supports both light and dark themes. The theme preference is stored in local storage and applied to subsequent visits.

## Language Support

The website automatically detects the user's preferred language and offers a language switcher for manual selection. 