from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import get_object_or_404

from snipt.snippet.models import Snippet

from snipt.favsnipt.models import FavSnipt

def toggle_fav(request, snipt):
    """
    An AJAX view for adding favorite snipts.
    """
    
    try:
        favsnipt = FavSnipt.objects.get(user=request.user, snipt=snipt)
        favsnipt.delete()
        data = { 'success': True, 'favorited': False }
    except:
        snipt = get_object_or_404(Snippet, id__exact=snipt)
        if snipt.user != request.user:
            favsnipt = FavSnipt(user=request.user, snipt=snipt)
            favsnipt.save()
            data = { 'success': True, 'favorited': True }
        else:
            data = { 'success': False, 'error': 'Cannot favorite your own snipts.', 'favorited': False }
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
