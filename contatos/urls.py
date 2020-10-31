from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda, name='agenda'),
    path('busca/', views.busca, name='busca'),
    path('novo_contato/', views.novo_contato, name='novo_contato'),
    path('<int:contato_id>', views.ver_contato, name='ver_contato'),
]
