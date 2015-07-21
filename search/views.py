from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from fuzzywuzzy import fuzz

from .models import Name


def search_form(request):
    return render(request, 'search/search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        names = Name.objects.filter(name__icontains=q)
        names = sorted(names, key=lambda x: fuzz.ratio(q, x.name), reverse=True)
        return render(request, 'search/search_results.html',
                      {'names': names, 'query': q})
    else:
        return HttpResponseRedirect(reverse('search-form'))
