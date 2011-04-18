from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.comments.signals import comment_was_posted
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from tagging.models import Tag, TaggedItem
from django.template import RequestContext
from snipt.snippet.models import Snippet, Referer
from django.utils.html import escape
from django.utils import simplejson
from tagging.utils import get_tag
from snipt.snippet.utils import *
from django.http import Http404
from settings import DEBUG
from snipt.forms import *
import md5

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def dispatcher(request, user, slug, snipt_id):
    if not user and not slug and not snipt_id:
        return home_page(request)
    elif user and snipt_id:
        if snipt_id == 'feed':
            return user_page(request, user, slug, True)
        else:
            return snipt_page(request, user, snipt_id)
    else:
        return user_page(request, user, slug)

def search(request):
    query_string = ''
    found_snipts = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['code', 'description', 'tags',])
        snipts = Snippet.objects.filter(entry_query).filter(Q(public=1) | Q(user=request.user.id)).order_by('-created')
        disable_wrap = request.session.get('disable_wrap')
        disable_message = request.session.get('disable_message')
        snipts_count = snipts.count()
    search = True
    return render_to_response('search.html', locals(), context_instance=RequestContext(request))

def feed(request, user, slug):
    return render_to_response('feed.html', locals(), context_instance=RequestContext(request))

def embed(request, snipt):
    try:
        snipt = Snippet.objects.get(key=snipt)
        snipt.code_stylized = highlight(snipt.code.replace("\\\"","\\\\\""), get_lexer_by_name(snipt.lexer, encoding='UTF-8'), HtmlFormatter(style="native", noclasses=True, prestyles="-moz-border-radius: 5px; border-radius: 5px; -webkit-border-radius: 5px; margin: 0; display: block; font: 11px Monaco, monospace !important; padding: 15px; background-color: #1C1C1C; overflow: auto; color: #D0D0D0;"))
        snipt.code_stylized = snipt.code_stylized.split('\n')
        snipt.referer = request.META.get('HTTP_REFERER', '')
        i = 0;
        for sniptln in snipt.code_stylized:
            snipt.code_stylized[i] = snipt.code_stylized[i].replace(" font-weight: bold", " font-weight: normal").replace('\'','\\\'').replace('\\n','\\\\n').replace("\\x", "\\\x")
            i = i + 1
    except Snippet.DoesNotExist:
        raise Http404
    
    if(snipt.referer):
        try:
            Referer.objects.get(url=snipt.referer, snippet=snipt.id)
        except Referer.DoesNotExist:
            referrer = Referer(None, snipt.referer, snipt.id)
            referrer.save()
        
    return render_to_response('embed.html', locals(), context_instance=RequestContext(request), mimetype="application/javascript")

def password_reset(request):
  request.session['msg'] = "";
  if request.POST:
    try:
      # check to see if a user by the email address exists in the system
      email = request.POST['email']
      user = User.objects.get(email=email)
    
      # generate a new password
      from random import choice
      new_password = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(16)])

      # assign the new password to the user account
      user.set_password(new_password)
      user.save()

      # send the new password to that e-mail address & tell them to change their pass immediately!
      from django.core.mail import send_mail
      
      subject = '[Snipt] Here\'s a temporary password'
      message = 'Log-in using %s\r\n\r\nPlease update your password immediately after that!\r\n\r\n- Snipt.net admins' % new_password
      
      send_mail(subject, message, 'no-reply@snipt.net', [email], fail_silently=False)
      
      request.session['msg'] = "We've sent you a temporary password. Check your e-mail!"
      
    except User.DoesNotExist:
      request.session['msg'] = "We didn't find anyone registered under %s" % request.POST['email']
    
    # or asset false
    # assert False
    
  return render_to_response('password_reset.html', locals(), context_instance=RequestContext(request))
  # request.session.msg = 'your password is being worked on by the locals.'
  # home_page(request)

def home_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/' + request.user.username)
    else:
        is_home = True
        return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def all_public_tags(request):
    tags = Tag.objects.usage_for_queryset(Snippet.objects.filter(public='1'), counts=True)
    return render_to_response('all-public-tags.html', locals(), context_instance=RequestContext(request))

    from django.contrib.comments.signals import comment_was_posted

def email_owner_on_comment(sender, comment, request, *args, **kwargs):
    from django.core.mail import EmailMultiAlternatives
    snipt = Snippet.objects.get(id=request.POST['object_pk'])
    if snipt.user.username != comment.name:
        text_content = """
            %s has posted a comment on your snipt "%s" at http://snipt.net%s#comment-%s.
        
            Just thought you'd like to know!
        
            The Snipt team at Lion Burger.
        """ % (comment.name, snipt.description, snipt.get_absolute_url(), comment.id)
        html_content = """
            <a href="http://snipt.net/%s">%s</a> has posted a comment on your snipt "<a href="http://snipt.net%s#comment-%s">%s</a>".<br />
            <br />
            Just thought you'd like to know!<br />
            <br />
            The <a href="http://snipt.net">Snipt</a> team at <a href="http://lionburger.com">Lion Burger</a>.
        """ % (comment.name, comment.name, snipt.get_absolute_url(), comment.id, snipt.description)
        msg = EmailMultiAlternatives("""A new comment on "%s".""" % snipt.description, text_content, 'Snipt <info@snipt.net>', [snipt.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

comment_was_posted.connect(email_owner_on_comment)

def snipt_page(request, user, snipt_id):
    try:
        snipt = Snippet.objects.get(slug=snipt_id)
        if 'c' in request.GET:
            return HttpResponseRedirect(snipt.get_absolute_url() + '#comment-' + request.GET['c'])
    except:
        return HttpResponseRedirect('/' + user + '/tag/' + snipt_id)
    context_user = User.objects.get(id=snipt.user.id)
    
    if request.user.id == context_user.id:
        mine = True
    else:
        mine = False
    
    if not snipt.public and not mine:
        try:
            if request.GET['key'] != snipt.key:
                raise Http404()
            else:
                key = True
        except:
            raise Http404()
    
    disable_wrap = request.session.get('disable_wrap')
    disable_message = request.session.get('disable_message')
    
    return render_to_response('snipt.html', locals(), context_instance=RequestContext(request))

def user_page(request, user, slug, feed=False):
    
    # Set disable message to false.
    # request.session['disable_message'] = False
    
    # If the user has requested a tag listing page, handle accordingly, otherwise serve latest snipts.
    if request.user.username != user:
        mine = False
        try:
            context_user = User.objects.get(username=user)
            if context_user.username == 'public':
                public = True
            else:
                public = False
        except:
            raise Http404()
    else:
        mine = True
        context_user = request.user
    if slug is not None:
        slug = slug.replace('tag/','')

        """
        Attempt to retrieve the tag for this particular slug.  In the event that there is no tag
        associated with this slug, set tag to 'None'.
        """
        try:
            tag = Tag.objects.get(name = slug)
        except:
            tag = None

        # If the tag exists, retrieve the snipts that this user has tagged with this particular tag.
        if tag is not None:
            if mine:
                snipts = TaggedItem.objects.get_by_model(Snippet.objects.filter(user=context_user.id).order_by('-created'), tag)
                
                from snipt.favsnipt.models import FavSnipt
                favsnipts = FavSnipt.objects.filter(user=context_user.id)
                favrd = []
                for fs in favsnipts:
                    fs.snipt.favrd = True
                    fs.snipt.created = fs.created
                    if str(tag) in fs.snipt.tags:
                        favrd.append(fs.snipt)

                from operator import attrgetter
                from itertools import chain
                snipts = sorted(
                    chain(snipts, favrd),
                    key=attrgetter('created'), reverse=True)
                
            elif not public:
                snipts = TaggedItem.objects.get_by_model(Snippet.objects.filter(user=context_user.id, public='1').order_by('-created'), tag)
            else:
                snipts = TaggedItem.objects.get_by_model(Snippet.objects.filter(public='1').order_by('-created'), tag)

        # If the tag does not exist, raise 404.
        else:
            raise Http404()

        # If the tag exists, but the user has no snipts for this particular tag, raise 404.
        if len(snipts) == 0:
            raise Http404()

    # If the user is at the homepage (no tag specified).
    else:

        # Retrieve latest 20 snipts for user.
        if mine:
            snipts = Snippet.objects.filter(user=context_user.id).order_by('-created')
            
            from snipt.favsnipt.models import FavSnipt
            favsnipts = FavSnipt.objects.filter(user=context_user.id)
            favrd = []
            for fs in favsnipts:
                fs.snipt.favrd = True
                fs.snipt.created = fs.created
                favrd.append(fs.snipt)
            
            from operator import attrgetter
            from itertools import chain
            snipts = sorted(
                chain(snipts, favrd),
                key=attrgetter('created'), reverse=True)
            
        elif not public:
            snipts = Snippet.objects.filter(user=context_user.id, public='1').order_by('-created')
        else:
            snipts = Snippet.objects.filter(public='1').order_by('-created')[:100]

    # Compile the list of tags that this user has used.
    if mine:
        user_tags_list = Tag.objects.usage_for_queryset(Snippet.objects.filter(user=context_user.id).order_by('-created'), counts=True)
    elif not public:
        user_tags_list = Tag.objects.usage_for_queryset(Snippet.objects.filter(user=context_user.id, public='1').order_by('-created'), counts=True)
    else:
        user_tags_list = Tag.objects.usage_for_queryset(Snippet.objects.filter(public='1'), counts=True)
        if not DEBUG:
            user_tags_list.sort(key=lambda x: x.count, reverse=True)
        user_tags_list = user_tags_list[:40]
    
    for usertag in user_tags_list:
        usertag.slug = str(usertag)

    disable_wrap = request.session.get('disable_wrap')
    disable_message = request.session.get('disable_message')

    if mine:
        total_count = Snippet.objects.filter(user=context_user.id).count()
    elif not public:
        total_count = Snippet.objects.filter(user=context_user.id, public='1').count()
    else:
        total_count = Snippet.objects.filter(public='1').count()

    if total_count > 0:
        # Get the last lexer used so we can auto-select that one.
        if mine:
            last_lexer = Snippet.objects.filter(user=context_user.id).order_by('-created')[0].lexer
            
    snipts_count = len(snipts)
    
    # Send a modified version of the request path so we may compare it to the list of tag slugs (to identify current page).
    if mine:
        request_tag = request.path.replace('/' + request.user.username + '/tag/','')
    else:
        request_tag = request.path.replace('/' + context_user.username + '/tag/','')

    if feed:
        try:
            snipts = TaggedItem.objects.get_by_model(Snippet.objects.filter(user=context_user.id, public='1').order_by('-created'), tag)
        except:
            snipts = Snippet.objects.filter(user=context_user.id, public='1').order_by('-created')
        real_path = request.path.replace('/feed', '')
        if '/all' not in request.path:
            snipts = snipts.filter()[:20]
        return render_to_response('feed.xml', locals(), context_instance=RequestContext(request), mimetype="application/rss+xml")
    else:
        return render_to_response('home_user.html', locals(), context_instance=RequestContext(request))

def signup(request):
    """
    Handle new user signups.
    """
    signup_form = UserCreationForm(request.POST)
    
    # If the signup form has been submitted and is valid, save the new user and log the user in, otherwise present the form (with errors, if necessary).
    if signup_form.is_valid():
        signup_form.save()
        
        # Go ahead and log the new user in after we've created them.  Convenience!
        user = authenticate(username=request.POST['username'], password=request.POST['password1'])
        auth_login(request, user)

        return HttpResponseRedirect('/')
    else:
        return render_to_response("registration/signup.html", {
            'signup_form' : signup_form,
            'signup' : True,
            'data': request.POST
        }, context_instance=RequestContext(request))

@login_required
def tags(request):
    """
    Return a list of tags that the user has used.
    """
    user_tags_list = Tag.objects.usage_for_queryset(Snippet.objects.filter(user=request.user.id).order_by('-created'), counts=True)
    
    """
    For each tag, append the details of this tag to a new list which will be appended to the JSON response.
    
    Why?  Because if we simply send along the list of tag objects, simplejson won't know how to serialize it (rightly so).
    """
    tags_list = []
    for tag in user_tags_list:
        tags_list.append({
            'id': tag.id,
            'tag': escape(str(tag)),
            'count': escape(str(tag.count))
        })
    data = {
        'tags_list': tags_list
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def save(request):
    """
    An AJAX view for saving new snipts.
    
    If we sent along an id of '0', it means we're adding a new snipt, so use the appropriate form.
    Otherwise, create an instance form from the model for that specific id.
    """
    try:
        request.POST['id']
    except:
        raise Http404()
    if request.POST['id'] != '0':
        submitted_snippet = SnippetForm(request.POST, instance=Snippet.objects.get(id=request.POST['id'], user=request.user.id))
    else:
        submitted_snippet = SnippetForm(request.POST)
    if submitted_snippet.is_valid():
        
        # Halt the form submission until we add the proper user to the values.
        submitted_snippet = submitted_snippet.save(commit=False)
        submitted_snippet.user = request.user
        if request.POST['id'] == '0':
            submitted_snippet.slug = SlugifyUniquely(submitted_snippet.description, Snippet)
            submitted_snippet.key = md5.new(submitted_snippet.slug).hexdigest()
        
        submitted_snippet.save()
        
        """
        Grab the tags for the newly created snippet.
        For each tag, append the details of this tag to a new list which will be appended to the JSON response.
        
        Why?  Because if we simply send along the list of tag objects, simplejson won't know how to serialize it (rightly so).
        """
        submitted_snippet.tags_list = []
        tags_list = submitted_snippet.get_tags()
        for tag in tags_list:
            submitted_snippet.tags_list.append({
                'id': tag.id,
                'tag': escape(str(tag)),
            })
        
        # Construct the data object we'll send back to the client so the new snipt can appear immediately.
        data = {
            'success': True,
            'id': submitted_snippet.id,
            'code': escape(submitted_snippet.code),
            'code_stylized': stylize(submitted_snippet.code, submitted_snippet.lexer),
            'description': escape(submitted_snippet.description),
            'tags': escape(submitted_snippet.tags),
            'tags_list': submitted_snippet.tags_list,
            'lexer': submitted_snippet.lexer,
            'public': submitted_snippet.public,
            'key': submitted_snippet.key,
            'slug': submitted_snippet.slug,
            'username': request.user.username,
            'created_date': submitted_snippet.created.strftime("%b %d"),
            'created_time': submitted_snippet.created.strftime("%I:%M %p").replace("AM","a.m.").replace("PM","p.m.")
        }
    else:
        data = {
            'success': False
        }
        
    # Use simplejson to convert the Python object to a true JSON object (though it's already pretty close).
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def stylize(code, lexer):
    return highlight(code, get_lexer_by_name(lexer, encoding='UTF-8'), HtmlFormatter())

def wrap(request):
    if request.session.get('disable_wrap') == True:
        request.session['disable_wrap'] = False
    else:
        request.session['disable_wrap'] = True
    data = {
        'disable_wrap': str(request.session['disable_wrap'])
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def message(request):
    if request.session.get('disable_message') == True:
        request.session['disable_message'] = False
    else:
        request.session['disable_message'] = True
    data = {
        'disable_message': str(request.session['disable_message'])
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def delete(request):
    """
    An AJAX view for deleting snipts.
    """
    deleting = Snippet.objects.get(id=request.POST['id'])
    
    # Make sure no one's trying to pull a fast one on us (or another user).
    if deleting.user_id == request.user.id:
        delid = deleting.id
        deleting.delete()
        
        # Return the deleted id to the client so that the snipt can be deleted from the page immediately.
        data = {
            'success': True,
            'id': delid
        }
    else:
        data = {
            'success': False
        }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
