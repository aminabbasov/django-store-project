from typing import Any

from django.core.mail import BadHeaderError
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic

from products.tasks import send_mail


class ProductsContactView(generic.TemplateView):
    template_name = "products/contact.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: dict[str, Any]) -> JsonResponse | HttpResponse:
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        try:
            send_mail.delay(name, email, subject, message)

        except BadHeaderError:
            return HttpResponse("Invalid header found.")

        except Exception:  # noqa: PIE786
            return JsonResponse({"message": "fail"}, status=500)

        return JsonResponse({"message": "success"}, status=200)
