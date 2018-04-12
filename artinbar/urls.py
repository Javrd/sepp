"""artinbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import logout
from mvp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lista_ofertas/',  views.lista_ofertas, name='lista_ofertas'),
    path('', views.indexRedir, name='index'),
    path('artinbar',  views.index, name='index'),
    path('formulario_oferta/',  views.formulario_oferta, name='formulario_oferta'),
    path('logout', logout, {'next_page': '/artinbar'}, name='logout'),
    path('login', views.login, name='login'),
    path('vista_artista/<int:id_artista>/',views.vista_artista, name='vista_artista'),
    path('vista_local/<int:id_local>/', views.vista_local, name='vista_local'),
    path('chat/', views.chat, name='chat'),
    path('chat/<user_id>/', views.chat, name='chat'),
    path('chat/<user_id>/sync', views.chat_sync, name='chat_sync'),
    path('paypal_test/<int:contact_id>', views.paypal_test, name='paypal_test'),
    path('payment', views.payment, name='payment'),
    path('executePayment', views.executePayment, name='executePayment'),
    path('paymentConfirmation', views.paymentConfirmation,
         name='paymentConfirmation'),
    path('registerVenue', views.register_venue.as_view(), name='register_venue'),
    path('registerArtist', views.register_artist.as_view(), name='register_artist'),
    path('editar_local', views.formulario_perfil_venue, name='formulario_perfil_venue'),
    path('editar_artista', views.formulario_perfil_artist, name='formulario_perfil_artist'),
    path('vote', views.vote, name='vote')
]
