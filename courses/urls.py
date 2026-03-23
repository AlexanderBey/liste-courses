from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('liste/new/', views.creer_liste, name="creer_liste"),
    path('liste/<int:pk>/', views.detail_liste, name="detail_liste"),
    path('list/<int:pk>/supprimer/', views.supprimer_liste, name="supprimer_liste"),
    path('article/<int:pk>/toggle/', views.toggle_achete, name="toggle_achete"),
    path('article/<int:pk>/supprimer', views.supprimer_article, name="supprimer_article"),
    path('register/', views.register, name='register'),
    path('rejoindre-par-code', views.rejoindre_par_code, name="rejoindre_par_code"),
]