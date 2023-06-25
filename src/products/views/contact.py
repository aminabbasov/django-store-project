from django.views import generic
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse, HttpResponse
from django.conf import settings

class ProductsContactView(generic.TemplateView):
    template_name = 'products/contact.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        try:
            body = f"""
                You have received a new message from your website contact form.\n\n
                Here are the details:\n\n
                Name: {name}\n\n
                Email: {email}\n\n
                Subject: {subject}\n\n
                Message: {message}
            """
            send_mail(subject, body, email, [email for name, email in settings.ADMINS], fail_silently=False)
            
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        
        except Exception:
            #! logger.warning('User cannot send a message.', exc_info=True)                       XXXXXXXXXXXXXXXXXXXXXX
            return JsonResponse({'message': 'fail'}, status=500)
        
        return JsonResponse({'message': 'success'}, status=200)
