from django.contrib.auth.models import User

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc

from snippet.models import Snippet

from tagging.models import Tag, TaggedItem

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class TagHandler(BaseHandler):

    def read(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except:
            resp = rc.NOT_HERE
            resp.write(": Tag does not exist.")
            return resp
        
        snipts = TaggedItem.objects.get_by_model(Snippet.objects.filter(public='1'), tag)
        tag_count = snipts.count()
        snipt_ids = []
        
        for snipt in snipts:
            snipt_ids.append(snipt.id)
        
        users_with_tag = []
        users_tag_list = []
        
        for snipt in snipts:
            users_with_tag.append(snipt.user.id)
        
        users_with_tag = set(users_with_tag)
        
        for user in users_with_tag:
            users_tag_list.append(user)
        
        data = {
            'id': tag.id,
            'name': tag.name,
            'count': tag_count,
            'snipts': snipt_ids,
            'users_with_tag': users_tag_list
        }
        return data

class TagsHandler(BaseHandler):
    
    def read(self, request):
        tags = Tag.objects.usage_for_queryset(Snippet.objects.filter(public='1'), counts=True)
        tags_list = []
        for tag in tags:
            tags_list.append({
                'id': tag.id,
                'name': tag.name,
                'count': tag.count
            })
        data = {
            'tags': tags_list
        }
        return data

class UserHandler(BaseHandler):
    
    def read(self, request, username):
        try:
            user = User.objects.get(username=username)
        except:
            resp = rc.NOT_HERE
            resp.write(": User does not exist.")
            return resp
        
        snipts = Snippet.objects.filter(user=user.id, public='1')
        tags = Tag.objects.usage_for_queryset(snipts, counts=True)
        tags_list = []
        snipts_list = []
        
        for tag in tags:
            tags_list.append({'id': tag.id, 'name': tag.name, 'count': tag.count})
        
        for snipt in snipts:
            snipts_list.append(snipt.id)
        
        data = {
            'username': user.username,
            'id': user.id,
            'tags': tags_list,
            'snipts': snipts_list,
            'count': snipts.count()
        }
        return data

class SniptHandler(BaseHandler):
    
    def read(self, request, snipt_id):
        try:
            snipt = Snippet.objects.get(id=snipt_id)
        except:
            resp = rc.NOT_HERE
            resp.write(": Snipt does not exist.")
            return resp
    
        if snipt.public == False:
            resp = rc.FORBIDDEN
            resp.write(": You don\'t have permission to access this snipt.")
            return resp
    
        snipt_tags = Tag.objects.get_for_object(snipt)
        tags_list = []
    
        for tag in snipt_tags:
            tags_list.append({'id': tag.id, 'name': tag.name})
    
        try:
            style = request.GET['style']
        except:
            style = 'default'
    
        try:
            formatted_code = highlight(snipt.code.replace("\\\"","\\\\\""), get_lexer_by_name(snipt.lexer, encoding='UTF-8'), HtmlFormatter(style=style, noclasses=True))
        except:
            formatted_code = highlight(snipt.code.replace("\\\"","\\\\\""), get_lexer_by_name(snipt.lexer, encoding='UTF-8'), HtmlFormatter(style='default', noclasses=True))
    
        data = {
            'id': snipt.id,
            'code': snipt.code,
            'description': snipt.description,
            'created': snipt.created,
            'user': snipt.user.username,
            'tags': tags_list,
            'lexer': snipt.lexer,
            'public': snipt.public,
            'key': snipt.key,
            'slug': snipt.slug,
            'formatted_code': formatted_code,
        }
        return data

