from django.contrib.auth import login  as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

# Create your views here.
def lista_ofertas(request):
    offer_list = Offer.objects.all()
    context = {'offer_list': offer_list}
    return render(request, './lista_ofertas.html', context)

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

