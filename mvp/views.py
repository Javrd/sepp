from django.shortcuts import render
from .models import *
from django.shortcuts import get_list_or_404

# Create your views here.
def offerList(request):
    offer_list = get_list_or_404(Offer)
    context = {'offer_list': offer_list}
    return render(request, './offerList.html', context)