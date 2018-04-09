from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.template import loader
from datetime import datetime
from requests.auth import HTTPBasicAuth
import requests

from .forms import *
from .models import *


# Create your views here.
def lista_ofertas(request):
    offer_list = Offer.objects.all()
    context = {'offer_list': offer_list}
    return render(request, './lista_ofertas.html', context)


@permission_required('mvp.venue', login_url="/login")
def formulario_oferta(request):
    if request.method == 'POST':
        form = OfferForm(request.user, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.venue = Venue.objects.get(id=request.user.id)
            offer.save()
            return HttpResponseRedirect('/lista_ofertas/')
    else:
        form = OfferForm(request.user)

    return render(request, './formulario_oferta.html', {'form': form})


def indexRedir(request):
    return redirect("/artinbar")


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def login(request):
    if request.user.is_authenticated:
        return redirect("/artinbar")
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect("/artinbar")
        else:
            context = {'formulario': formulario}
            return render(request, 'login.html', context)
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)


def vista_artista(request, id_artista):
    artista = get_object_or_404(Artist, pk=id_artista)
    fotos = Photo.objects.filter(user=artista)
    multimedia = Media.objects.filter(artist=artista)

    context = {'artista': artista, 'fotos': fotos, 'multimedia': multimedia}
    return render(request, './vista_artista.html', context)


def vista_local(request, id_local):
    local = get_object_or_404(Venue, pk=id_local)
    fotos = Photo.objects.filter(user=local)
    geolocalizacion = Geolocation.objects.get(venue=local)

    context = {'local': local, 'fotos': fotos,
               'geolocalizacion': geolocalizacion}
    return render(request, './vista_local.html', context)


@login_required(login_url='/login')
def chat(request, user_id=None):

    principal = request.user
    if not user_id:
        contacts = (User.objects.filter(receivers__in=[principal]) | User.objects.filter(
            senders__in=[principal])).distinct()
        return render(request, 'contacts.html', {'contacts': contacts})

    else:
        contact = User.objects.get(id=user_id)

        if request.method == 'POST':
            form = request.POST
            msg = Message.objects.create(
                sender=principal, receiver=contact, timeStamp=datetime.now(), text=form['text'])
            data = {}
            data['date'] = msg.timeStamp.strftime("%d/%m/%Y %H:%m")
            data['text'] = msg.text
            return JsonResponse(data)

        messages = Message.objects.filter(receiver=principal, sender=contact) | Message.objects.filter(
            receiver=contact, sender=principal).order_by('timeStamp')
        last_contact_message = Message.objects.filter(
            receiver=principal, sender=contact).order_by('-timeStamp')
        if last_contact_message:
            last_contact_message = last_contact_message[0].id
        else:
            last_contact_message = -1
        return render(request, 'chat.html', {'messages': messages, 'contact': contact, 'last_contact_message': last_contact_message})


@login_required(login_url='/login')
def chat_sync(request, user_id=None):
    if request.method == 'POST':
        principal = request.user
        contact = User.objects.get(id=user_id)
        form = request.POST
        msg = Message.objects.filter(
            receiver=principal, sender=contact).order_by('-timeStamp')
        data = {}
        if msg:
            data['date'] = msg[0].timeStamp.strftime("%d/%m/%Y %H:%m")
            data['text'] = msg[0].text
            data['id'] = msg[0].id
        else:
            data['id'] = -1
        return JsonResponse(data)


@login_required(login_url='/login')
def paypal_test(request):
    venue = get_object_or_404(Venue, pk=201)
    principal = request.user
    context = {'venue': venue, 'user': principal}
    return render(request, './paypalTest.html', context)


@login_required(login_url='/login')
def payment(request):
    print('============ Requesting access token ============')
    payee = request.POST.get('payee')
    amount = request.POST.get('amount')
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'accept': 'application/json',
        'Accept-Language': 'en_US'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    paypalResponse = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(
        'AYsiuq3v0vkhTIZrJA-pMAC-NJFG4LUG0AOphhoU52D0YHP1WiXpZ1ENIV_tcks6qutqVn99ZjR38lWg', 'ELZ-zqNT0hsVDUA5fjgguhlMIJTNjvu0A7y0_LqeBg_gChO9Ndjpy4gW-gpWbOZWnehZFCOlnco7Av_h'))
    json = paypalResponse.json()
    accessToken = json['access_token']

    print('Access Token obtained, expires in '+str(json['expires_in']))
    print('Access Token: '+accessToken)

    print('============ Creating payment ============')
    print('Payee: '+payee)
    print('Amount: '+amount)
    fee = float(amount)*0.05  # TODO: Fee?
    totalAmount = float(amount) + fee
    print('Fee: '+str(fee))
    print('Total amount: '+str(totalAmount))

    bearerToken = 'Bearer '+accessToken

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }

    amount1 = {
        'total': str(totalAmount),
        'currency': 'EUR',
        'details': {
            'subtotal': str(amount),
            'handling_fee': str(fee)
        }
    }

    transaction1 = {
        'amount': amount1,
        'description': 'Pago a Art in Bar',
        'payment_options': {
            'allowed_payment_method': 'IMMEDIATE_PAY'
        }
    }

    transactions = [transaction1]

    data = {
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': transactions,
        'note_to_payer': 'Puedes contactar con nosotros para cualquier duda en pagosartinbar@gmail.com',
        'redirect_urls': {
            'return_url': 'http://localhost:8000/artinbar',
            'cancel_url': 'http://localhost:8000/artinbar'
        }
    }

    saleUrl = 'https://api.sandbox.paypal.com/v1/payments/payment'

    payment = requests.post(saleUrl, headers=headers, json=data).json()

    if (payment['id'] is not None):
        print('Payment id: '+payment['id'])
        print('============ Payment created succesfully ============')

    return JsonResponse(payment)


def executePayment(request):
    paymentId = request.POST.get('paymentId')
    payerId = request.POST.get('payerId')
    print('============ Requesting access token ============')

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'accept': 'application/json',
        'Accept-Language': 'en_US'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    paypalResponse = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(
        'AYsiuq3v0vkhTIZrJA-pMAC-NJFG4LUG0AOphhoU52D0YHP1WiXpZ1ENIV_tcks6qutqVn99ZjR38lWg', 'ELZ-zqNT0hsVDUA5fjgguhlMIJTNjvu0A7y0_LqeBg_gChO9Ndjpy4gW-gpWbOZWnehZFCOlnco7Av_h'))
    json = paypalResponse.json()
    accessToken = json['access_token']

    print('Access Token obtained, expires in '+str(json['expires_in']))
    print('Access Token: '+accessToken)

    print('============ Building payment execution request ============')    
    print('Payment ID: '+paymentId)
    print('Payer ID: '+payerId)

    executeUri = 'https://api.sandbox.paypal.com/v1/payments/payment/'+paymentId+'/execute/'

    bearerToken = 'Bearer '+accessToken

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }

    data = {
        'payer_id': payerId
    }

    payment = requests.post(executeUri, headers=headers, data=data)

    if (payment['state'] == 'approved'):
        return 'OK'
    else:
        return 'ERROR'
