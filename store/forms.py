
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product


# ==========================================
# USER REGISTRATION FORM
# ==========================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if CustomUser.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email


# ==========================================
# PRODUCT MANAGEMENT FORM
# ==========================================

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        # Seller is intentionally excluded.
        # The logged-in seller will be assigned in the view.

        fields = [
            'category',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
        ]

        widgets = {
            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter product name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter product description'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01',
                    'placeholder': 'Enter product price'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Enter available quantity'
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None or price <= 0:
            raise forms.ValidationError(
                "Product price must be greater than zero."
            )

        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock is None or stock < 0:
            raise forms.ValidationError(
                "Stock cannot be negative."
            )

        return stock

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Image size must not exceed 5 MB."
            )

        return image
