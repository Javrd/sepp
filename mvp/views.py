from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.shortcuts import get_list_or_404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

# Create your views here.


def offerList(request):
    offer_list = get_list_or_404(Offer)
    context = {'offer_list': offer_list}
    return render(request, './offerList.html', context)


def offerForm(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/offerList/')
    else:
        form = OfferForm()

    return render(request, './offerForm.html', {'form': form})


def indexRedir(request):
    return redirect("/artinbar")


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
