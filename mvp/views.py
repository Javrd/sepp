from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from .forms import *


def nuevoVenue(request):
    if request.method=='POST':
        formulario = VenueForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('principal.views.inicio'))
    else:
        formulario = VenueForm(request.POST)
    context = {'formulario':formulario}
    return render(request, 'venueForm.html', context)