from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logar/', views.logar, name="logar"),
    path('recuperar_senha/', views.recuperar_senha, name="recuperar_senha"),
    path('redefinir_senha/<str:token>/', views.redefinir_senha, name="redefinir_senha"),
    path('sair/', views.sair, name="sair"),
]
