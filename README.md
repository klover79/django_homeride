# homeride Application Name
Boarding School Bus Booking System

# ==============================
# tailwind django installation
# ==============================
Installation
Step-by-step instructions
Install the django-tailwind package via pip:

python -m pip install django-tailwind
Alternatively, you can install the latest development version via:

python -m pip install git+https://github.com/timonweb/django-tailwind.git
Add 'tailwind' to INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
  # other Django apps
  'tailwind',
]
Create a Tailwind CSS compatible Django app, I like to call it theme:

python manage.py tailwind init
Add your newly created 'theme' app to INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme'
]
Register the generated 'theme' app by adding the following line to settings.py file:

TAILWIND_APP_NAME = 'theme'
Make sure that the INTERNAL_IPS list is present in the settings.py file and contains the 127.0.0.1 ip address:

INTERNAL_IPS = [
    "127.0.0.1",
]
Install Tailwind CSS dependencies, by running the following command:

python manage.py tailwind install
The Django Tailwind comes with a simple base.html template located at your_tailwind_app_name/templates/base.html. You can always extend or delete it if you already have a layout.

If you are not using the base.html template that comes with Django Tailwind, add {% tailwind_css %} to the base.html template:

{% load static tailwind_tags %}
...
<head>
   ...
   {% tailwind_css %}
   ...
</head>
The {% tailwind_css %} tag includes Tailwind’s stylesheet.

Let’s also add and configure django_browser_reload, which takes care of automatic page and css refreshes in the development mode. Add it to INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme',
  'django_browser_reload'
]
Staying in settings.py, add the middleware:

MIDDLEWARE = [
  # ...
  "django_browser_reload.middleware.BrowserReloadMiddleware",
  # ...
]
The middleware should be listed after any that encode the response, such as Django’s GZipMiddleware. The middleware automatically inserts the required script tag on HTML responses before </body> when DEBUG is True.

Include django_browser_reload URL in your root url.py:

from django.urls import include, path
urlpatterns = [
    ...,
    path("__reload__/", include("django_browser_reload.urls")),
]
Finally, you should be able to use Tailwind CSS classes in HTML. Start the development server by running the following command in your terminal:

python manage.py tailwind start
