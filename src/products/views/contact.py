from django.views import generic
from django.core.mail import BadHeaderError
from django.http import JsonResponse, HttpResponse

from ..tasks import send_mail

class ProductsContactView(generic.TemplateView):
    template_name = 'products/contact.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        try:
            send_mail.delay(name, email, subject, message)
            
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        
        except Exception:
            #! logger.warning('User cannot send a message.', exc_info=True)                       XXXXXXXXXXXXXXXXXXXXXX
            return JsonResponse({'message': 'fail'}, status=500)
        
        return JsonResponse({'message': 'success'}, status=200)
