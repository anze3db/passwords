from web.models import Password
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest



def index(request):
    # I don't really like .reverse()[:5] part but it will have to do for now
    latest_pass_list = Password.objects.all().order_by('id').reverse()[:5]
    return render_to_response('web/index.html', {'latest_pass_list': latest_pass_list},
                                                 context_instance=RequestContext(request))
    
def add(request):
    # This here is some really primitive error handling:
    # I would use trim() but there is probably someone out there with a password containing only spaces :)
    if(len(request.POST['passwords']) == 0):
        
        return HttpResponseBadRequest("You have mad a nono, <a href=\"/\">go back</a>.")        
        
    for pw in request.POST['passwords'].split('\n'):
        # This is probably really slow but django doesn't have a batch INSERT :/
        p = Password(password=pw)
        p.save()
        
    return HttpResponseRedirect('/')
                
    
               
    