from web.models import Password, PasswordUnique
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

def index(request):
    
    common_passwords = PasswordUnique.objects.all().order_by('count').reverse()[:5]
    
    return render_to_response('web/index.html', {'pass_count': Password.objects.all().filter(processed=True).count(),
                                                 'common_passwords' : common_passwords,},
                                                 
                                                 context_instance=RequestContext(request))
    
def add(request):
    # This here is some really primitive error handling:
    # I would use trim() but there is probably someone out there with a password containing only spaces :)    
    if(request.method != "POST" or len(request.POST['pw_pass']) == 0):       
        raise Http404("Trying to add without using POST")   
    
    # Source_id should not be hardcoded but it's late:    
    p = Password(password=request.POST["pw_pass"], source_id=1)
    p.save()
    
    return HttpResponseRedirect('/id/' + str(p.id))

    
def id(request, id):
    p = get_object_or_404(Password, pk=id)
    # count() - 1 because the password we are looking for was already entered: 
    count = Password.objects.all().filter(password=p.password).count() - 1
    return render_to_response('web/id.html', {'pass_count': count, 'password': p},
                                                 context_instance=RequestContext(request))    
 
                
    
               
    
