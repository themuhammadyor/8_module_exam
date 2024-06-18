from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from apps.shop.models import Product


def register_view(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User successfully registered')
            return redirect("users:login")
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        return render(request, 'users/register.html', {'form': form})


# class UserRegisterView(View):
#     def get(self, request):
#         form = UserRegisterForm()
#         return render(request, "users/register.html", context={"form": form})
#
#     def post(self, request):
#         create_form = UserRegisterForm(request.POST, request.FILES)
#         if create_form.is_valid():
#             create_form.save()
#             return redirect("users:login")
#         else:
#             context = {
#                 "form": create_form
#             }
#             return render(request, "users/register.html", context=context)


from apps.users.models import User


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You have logged in as {username}")
                return redirect('shop:home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            return render(request, "users/login.html", {"form": form})


def user_update_view(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            form = UserUpdateForm(request.POST or None, request.FILES, instance=user)
            if form.is_valid():
                form.save()

                login(request, user)
                messages.success(request, 'User successfully updated')
                return redirect("users:user-profile")
            return render(request, 'users/user-update.html', {'form': form})
        else:
            messages.error(request, "You Must be Logged in To Access This Page!")
            return redirect("shop:home")
    else:
        form = UserUpdateForm()
        return render(request, 'users/user-update.html', {'form': form})


@login_required
def logout_view(request):
    messages.info(request, f"{request.user.username} user successfully loged out")
    logout(request)
    return redirect("shop:home")


class UserProfileView(View):
    def get(self, request):
        products = Product.objects.filter(seller__username=request.user.username)
        user = get_object_or_404(User, username=request.user.username)
        first_name = user.first_name
        last_name = user.last_name
        return render(request, 'users/user-profile.html', {"products": products,
                                                           'first_name': first_name,
                                                           'last_name': last_name,
                                                           'user': user})


class UserUpdateView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        form = UserUpdateForm
        return render(request, 'users/user-update.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            form = UserUpdateForm(request.POST or None, request.FILES, instance=user)
            if form.is_valid():
                form.save()

                login(request, user)
                messages.success(request, 'User successfully updated')
                return redirect("users:user-profile")
            return render(request, 'users/user-update.html', {'form': form})
        else:
            messages.error(request, "You Must be Logged in To Access This Page!")
            return redirect("shop:home")
