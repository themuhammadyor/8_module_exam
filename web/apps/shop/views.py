from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib import messages

from apps.shop.forms import ProductForm
from apps.shop.models import Product, Category, Favorite, Card
from apps.users.models import User


# class Category:
#     def get_categories(self):
#         return Category.objects.all()


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()

        context = {
            "products": products, "categories": categories,
        }
        return render(request, "shop/index.html", context=context)


class ProductDetailPageView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        products = Product.objects.all()
        context = {
            "product": product,
            "products": products
        }
        return render(request, 'shop/product-detail.html', context)


class ProductCreatePageView(View):
    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'shop/product-create.html', context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            # name = form.cleaned_data.get('name'),
            # description = form.cleaned_data.get('description'),
            # available_color = form.cleaned_data.get('available_color'),
            # price = form.cleaned_data.get('price'),
            # brand = form.cleaned_data.get('brand'),
            # category = form.cleaned_data.get('category'),
            # cover = form.cleaned_data.get('cover'),
            # size = form.cleaned_data.get('size'),
            # count = form.cleaned_data.get('count'),
            # is_active = form.cleaned_data.get('is_active')
            # product = Product.objects.create(name=name,
            #                                  description=description,
            #                                  available_color=available_color,
            #                                  price=price,
            #                                  brand=brand,
            #                                  category=category,
            #                                  cover=cover,
            #                                  size=size,
            #                                  count=count,
            #                                  is_active=is_active,
            #                                  seller=request.user)
            # product.save()
            # form.save()
            return redirect('users:user-profile')
        else:
            form = ProductForm()
        context = {'form': form}
        return render(request, 'shop/product-create.html', context)


class FavoritesPageView(View):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        context = {f"favorites": favorites}
        return render(request, 'shop/favourites-list.html', context)


class BaseView(View):
    def get(self, request):
        products = Product.objects.all()
        user = request.user
        categories = Category.objects.all()
        cards = Card.objects.filter(user=user)
        favorites = Favorite.objects.filter(user=user)
        context = {'products': products, 'user': user, 'categories': categories, 'cards': cards, 'favorites': favorites}
        return render(request, 'base.html', context)


class AboutPageView(TemplateView):
    template_name = 'shop/about.html'


class ContactPageView(TemplateView):
    template_name = 'shop/contact.html'


class ShopPageView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products': products, 'categories': categories, 'page_obj': page_obj}
        return render(request, 'shop/shop.html', context)


class CategoryPageView(View):
    def get(self, request, id):
        products = Product.objects.filter(category=id)
        categories = Category.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products': products, 'categories': categories, 'page_obj': page_obj}
        return render(request, 'shop/shop.html', context)


class SearchView(ListView):
    template_name = 'shop/shop.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class FavouritesView(ListView):
    template_name = 'shop/favourites-list.html'
    model = Favorite
    context_object_name = 'favourites'


class FavouritesAddView(View):
    def get(self, request, product_id):
        user = request.user
        current_page = request.META.get('HTTP_REFERER')
        product = Product.objects.get(id=product_id)
        favourites = Favorite.objects.filter(user=user, product=product)

        if not favourites.exists():
            Favorite.objects.create(user=user, product=product, quantity=1)
            # favourite = Favorite(user=request.user, product=product, quantity=1)
            # favourite.save()
            return HttpResponseRedirect(current_page)
        else:
            favourite = favourites.first()
            favourite.quantity += 1
            favourite.save()
            return HttpResponseRedirect(current_page)


class FavouriteDeleteView(View):
    def get(self, request, favourite_id):
        favourite = Favorite.objects.get(id=favourite_id)
        favourite.delete()
        return redirect('shop:favourites-list')


class CardView(ListView):
    template_name = 'shop/card-list.html'
    model = Card
    context_object_name = 'cards'


class CardAddView(View):
    def get(self, request, product_id):
        user = request.user
        current_page = request.META.get('HTTP_REFERER')
        product = Product.objects.get(id=product_id)
        cards = Card.objects.filter(user=user, product=product)

        if not cards.exists():
            Card.objects.create(user=user, product=product, quantity=1)
            return HttpResponseRedirect(current_page)
        else:
            card = cards.first()
            card.quantity += 1
            card.save()
            return HttpResponseRedirect(current_page)


class CardDeleteView(View):
    def get(self, request, card_id):
        current_page = request.META.get('HTTP_REFERER')
        card = Card.objects.get(id=card_id)
        card.delete()
        return HttpResponseRedirect(current_page)


class FilterProductsPageView(View):
    def get_queryset(self):
        categories = Category.objects.all()
        queryset = Product.objects.filter(category=self.request.GET.getlist('category'))
        return queryset
    # def get(self):
    #     products = Product.objects.filter(category_id=self.kwargs['category_id'])
    #     return products


class ShopSinglePageView(TemplateView):
    template_name = 'shop/product-detail.html'
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid:
#             # product = Product(name=form.cleaned_data.get('name'),
#             #                   description=form.cleaned_data.get('description'),
#             #                   available_color=form.cleaned_data.get('available_color'),
#             #                   price=form.cleaned_data.get('price'),
#             #                   brand=form.cleaned_data.get('brand'),
#             #                   category=form.cleaned_data.get('category'),
#             #                   cover=form.cleaned_data.get('cover'),
#             #                   size=form.cleaned_data.get('size'),
#             #                   count=form.cleaned_data.get('count'),
#             #                   is_active=form.cleaned_data.get('is_active'), )
#             # product = Product(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
#             #                   is_active=form.cleaned_data['is_active'])
#             # product.seller = request.user
#             # product.save()
#             form.save()
#             messages.success(request, 'Post successfully created!')
#             return redirect('blog:user-profile')
#         else:
#             return render(request, 'shop/product-create.html', {'form': form})
#     else:
#         form = ProductForm()
#
#     return render(request, 'shop/product-create.html', {'form': form})
