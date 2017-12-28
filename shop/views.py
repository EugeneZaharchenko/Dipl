from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Авторизация успешна')
                    # return HttpResponseRedirect('../cart/templates/cart/detail.html')
                else:
                    return HttpResponse('Пользователь отсутствует')
            else:
                return HttpResponse('Неверный login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    HttpResponseRedirect('shop/base.html')

# @login_required
# def dashboard(request):
#     return render(request, 'registration/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            return render(request,
                          'shop/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'user_form': user_form})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products_list = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

        page = request.GET.get('page')
        paginator = Paginator(products_list, 2)

        try:
            products_list = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products_list = paginator.page(paginator.num_pages)


    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products_list})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = auth.authenticate(username=username, password=password)
#     if user is not None and user.is_active:
#         # Правильный пароль и пользователь "активен"
#         auth.login(request, user)
#         # Перенаправление на "правильную" страницу
#         return HttpResponseRedirect("/account/loggedin/")
#     else:
#         # Отображение страницы с ошибкой
#         return HttpResponseRedirect("/account/invalid/")


