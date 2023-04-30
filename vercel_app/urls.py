"""vercel_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from website import views as website_views
from website.views import TelegramBotView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', website_views.index, name='home'),

    path('chat/', website_views.chat_page, name='chat_page'),
    path("api/messages/<int:user_id>", website_views.get_messages),
    path("api/messages/", website_views.insert_message),
    path("test/", website_views.test_endpoint),
    path('api/telegram_webhook/', csrf_exempt(TelegramBotView.as_view())),
    path('', include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)