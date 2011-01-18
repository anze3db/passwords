from web.models import Password
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

ERROR_NOT_FOUND = "You seem to have stumbled upon a page that does not exist. Head back to <a href=\"/\">charted waters</a> as soon as you are ready."
ERROR_BAD_REQUEST = "I see what you did there."

def index(request):
    
    return render_to_response('web/index.html', {'pass_count': Password.objects.all().count()},
                                                 context_instance=RequestContext(request))
    
def add(request):
    # This here is some really primitive error handling:
    # I would use trim() but there is probably someone out there with a password containing only spaces :)    
    if(request.method != "POST" or len(request.POST['pw_pass']) == 0):       
        # TODO: Should set status code 400 
        return render_to_response('web/error.html', {'error_msg': ERROR_BAD_REQUEST},
                                                 context_instance=RequestContext(request))     
    
    # Source_id should not be hardcoded but it's late:    
    p = Password(password=request.POST["pw_pass"], Source_id=1)
    p.save()
    
    return HttpResponseRedirect('/id/' + str(p.id))
    
def pass_strength(passwd):
    # Matic: I should probably put this method elsewhere?
    # http://stackoverflow.com/questions/75057/what-is-the-best-way-to-check-the-strength-of-a-password
    conditions_met = 0
    if len(passwd) >= 6: 
        if passwd.lower() != passwd: conditions_met += 1
        if len([x for x in passwd if x.isdigit()]) > 0: conditions_met += 1
        if len([x for x in passwd if not x.isalnum()]) > 0: conditions_met += 1
    
    return conditions_met
    
def id(request, id):
    p = Password.objects.get(pk=id)
    # count() - 1 because the password we are looking for was already entered: 
    count = Password.objects.all().filter(password=p.password).count() - 1
    return render_to_response('web/id.html', {'pass_count': count, 'pass_strength': pass_strength(p.password)},
                                                 context_instance=RequestContext(request))    
def error(request):
    # TODO: Should set status code 404
    return render_to_response('web/error.html', {'error_msg': ERROR_NOT_FOUND},
                                                 context_instance=RequestContext(request))    
                
    
               
    
