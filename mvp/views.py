from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, redirect, render
from django.template import loader
from datetime import datetime

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
    if request.method=='POST':
        formulario=AuthenticationForm(data = request.POST)
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
    return render(request,'login.html',context)

@login_required(login_url='/login')
def chat(request, user_id=None):
    
    principal = request.user
    if not user_id:
        contacts = (User.objects.filter(receivers__in=[principal]) | User.objects.filter(senders__in=[principal])).distinct()
        return render(request,'contacts.html', {'contacts':contacts})
    
    else:
        if request.method == 'POST':
            contact = User.objects.get(id=user_id)
            form = request.POST
            Message.objects.create(sender=principal, receiver=contact, timeStamp=datetime.now(), text=form['text'])
            
        contact = User.objects.get(id=user_id)
        messages = Message.objects.filter(receiver=principal, sender=contact) | Message.objects.filter(receiver=contact, sender=principal)
                
        return render(request,'chat.html',{'messages':messages, 'contact':contact})

def chatForm(request):
    if request.method == 'POST':
        form = Message(request.POST)
        form.timeStamp = datetime.now()
        form.save()
        return HttpResponseRedirect('/chat/')
