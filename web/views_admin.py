from web.models import Password, PasswordUnique, Source
from web.forms import PasswordsForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.db import transaction

@transaction.commit_manually
def batch(request):

    if request.POST:
        
        
        
        # Insert the passwords:
        
        for chunk in request.FILES['passwords']:
            
            ps = Password(password=chunk.rstrip('\r\n'), source_id=request.POST['source'])            
            ps.save(batch = True)            
    
        # Update source count:                    
        src = Source.objects.get(pk = request.POST['source'])
        src.update_count()
        src.save()


        transaction.commit()


        return HttpResponseRedirect('/admin/web/password')
       
    return render_to_response('admin/web/password/batch.html', {'form': PasswordsForm(),
                                                                'num_unprocessed': Password.objects.all().filter(processed = False).count()},
                                                 
                                                 context_instance=RequestContext(request))

                
    
               
    
