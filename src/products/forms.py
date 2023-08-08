from django import forms

from products.models import Review


class ProductsReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                attrs={
                    "form": "RatingForm",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "form": "RatingForm",
                    "id": "message",
                    "cols": "30",
                    "rows": "5",
                }
            ),
        }
