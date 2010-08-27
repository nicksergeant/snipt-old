from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    api = True
    return render_to_response('api/home.html', locals(), context_instance=RequestContext(request))
