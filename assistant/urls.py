from django.urls import path
from .views import index_view, generate_ai_response

urlpatterns = [
    path('', index_view, name='home'),
    path('api/generate/', generate_ai_response, name='generate_ai'),
]