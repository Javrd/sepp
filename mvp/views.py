from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

# Create your views here.


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
        print(formulario.errors)
        username = formulario.cleaned_data.get('username')
        password = formulario.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print(username +"........."+password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("/artinbar")
        else:
            context = {'formulario': formulario}
            return render(request, 'login.html', context)
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request,'login.html',context)
