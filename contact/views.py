from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Message

# views for contact.html
def contactview(request):
    
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        massage = request.POST.get('massage', None)

        contact = Message.objects.create(name=name,
                                        email= email,
                                        phone=phone,
                                        massage= massage,
                    )
        contact.save()
        messages.success(request, 'Your massage has been submitted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        messages.error(request, 'something went wrong while sending your massage!')

    return render(request, 'pages/contact.html')
