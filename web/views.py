from web.models import Password
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest



def index(request):
    
    return render_to_response('web/index.html', {'pass_count': Password.objects.all().count()},
                                                 context_instance=RequestContext(request))
    
def add(request):
    # This here is some really primitive error handling:
    # I would use trim() but there is probably someone out there with a password containing only spaces :)    
    if(request.method != "POST" or len(request.POST['pw_pass']) == 0):        
        return HttpResponseBadRequest("You have made a nono, <a href=\"/\">go back</a>.")        
    
    # Source_id should not be hardcoded but it's late:    
    p = Password(password=request.POST["pw_pass"], Source_id=1)
    p.save()
    
    return HttpResponseRedirect('/id/' + str(p.id))

def id(request, id):
    p = Password.objects.get(pk=id)
    # count() - 1 because the password we are looking for was already entered: 
    count = Password.objects.all().filter(password=p.password).count() - 1
    return render_to_response('web/id.html', {'pass_count': count},
                                                 context_instance=RequestContext(request))
                
    
               
    