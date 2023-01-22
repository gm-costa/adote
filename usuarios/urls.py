from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.logar, name="login"),
    path('recuperar_senha/<str:email>/', views.recuperar_senha, name="recuperar_senha"),
    path('redefinir_senha/<int:id>/', views.redefinir_senha, name="redefinir_senha"),
    path('sair/', views.sair, name="sair"),
]
