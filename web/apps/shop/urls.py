from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, ShopPageView, ProductDetailPageView, \
    ProductCreatePageView, FilterProductsPageView, CategoryPageView, SearchView, FavouritesView, FavouritesAddView, \
    CardView, CardAddView, CardDeleteView, FavouriteDeleteView

app_name = 'shop'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about-us/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('filter/', FilterProductsPageView.as_view(), name='filter'),
    path('shop/search/', SearchView.as_view(), name='search'),
    path('shop/category/<int:id>', CategoryPageView.as_view(), name='category'),
    path('shop/', ShopPageView.as_view(), name='shop'),
    path('products/<int:pk>', ProductDetailPageView.as_view(), name='product-detail'),
    path('product-create/', ProductCreatePageView.as_view(), name='product-create'),
    path('favourites/', FavouritesView.as_view(), name='favourite-list'),
    path('favourite-add/<int:product_id>/', FavouritesAddView.as_view(), name='favourite-add'),
    path('favourite-delete/<int:product_id>/', FavouriteDeleteView.as_view(), name='favourite-delete'),
    path('cards/', CardView.as_view(), name='card-list'),
    path('card-add/<int:product_id>/', CardAddView.as_view(), name='card-add'),
    path('card-delete/<int:product_id>/', CardDeleteView.as_view(), name='card-delete'),
]