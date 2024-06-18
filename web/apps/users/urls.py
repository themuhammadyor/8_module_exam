from django.urls import path

from apps.users.views import UserLoginView, register_view, UserProfileView, logout_view, user_update_view, UserUpdateView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    # path('register/', UserRegisterView.as_view(), name="register"),
    path('register/', register_view, name="register"),
    path('user-profile/', UserProfileView.as_view(), name="user-profile"),
    path('user-update/', UserUpdateView.as_view(), name="user-update"),
    # path('user-update/', user_update_view, name="user-update"),
    # path('user-update/<int:id>', UserUpdateView.as_view(), name="user-update"),
    path('logout/', logout_view, name="logout"),
]
