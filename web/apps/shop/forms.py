from django.forms import ModelForm, IntegerField, Widget, Textarea, FileField, ImageField, FileInput

from apps.shop.models import Product, ProductReview


class ProductForm(ModelForm):
    cover = FileField(widget=FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if str(field) != "is_active":
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control', 'placeholder': f'Enter the {str(field)}'}
                )

    class Meta:
        model = Product
        fields = (
            'name', 'price', 'description', 'category_slug', 'brand_slug', 'color', 'sub_category', 'published_date', 'cover', 'is_active', 'slug')


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ('body', 'rating')
        widgets = {
            'body': Textarea(attrs={'class': 'form-control'}),
            'rating': IntegerField()
        }
