from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.shortcuts import get_list_or_404

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