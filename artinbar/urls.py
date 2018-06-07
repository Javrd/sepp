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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lista_ofertas/',  views.lista_ofertas, name='lista_ofertas'),
    path('mis_ofertas/',  views.mis_ofertas, name='mis_ofertas'),
    path('borrar_oferta/<offer_id>/',  views.borrar_oferta, name='borrar_oferta'),
    path('artinbar',  views.indexRedir, name='index'),
    path('',  views.index, name='index'),
    path('formulario_oferta/',  views.formulario_oferta, name='formulario_oferta'),
    path('logout', logout, {'next_page': '/'}, name='logout'),
    path('login', views.login, name='login'),
    path('vista_artista/<int:id_artista>/',
         views.vista_artista, name='vista_artista'),
    path('vista_local/<int:id_local>/', views.vista_local, name='vista_local'),
    path('chat/', views.chat, name='chat'),
    path('chat/<user_id>/', views.chat, name='chat'),
    path('paypal/<int:contact_id>', views.paypal, name='paypal'),
    path('payment', views.payment, name='payment'),
    path('executePayment', views.executePayment, name='executePayment'),
    path('paymentConfirmation', views.paymentConfirmation,
         name='paymentConfirmation'),
    path('registerVenue', views.register_venue.as_view(), name='register_venue'),
    path('registerArtist', views.register_artist.as_view(), name='register_artist'),
    path('editar_local', views.formulario_perfil_venue, name='formulario_perfil_venue'),
    path('editar_artista', views.formulario_perfil_artist, name='formulario_perfil_artist'),
    path('feedback', views.formulario_feedback.as_view(), name='formulario_feedback'),
    path('vote', views.vote, name='vote'),
    path('T&C', views.termsAndConditions, name='termsAndConditions'),
    path('lista_artistas/',  views.lista_artistas, name='lista_artistas'),
    path('lista_locales/',  views.lista_locales, name='lista_locales')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
