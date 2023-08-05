from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *

# Create your views here.
menu = [
    {'title': 'Про сайт', 'url_name': 'about'},
    {'title': 'Додати статтю', 'url_name': 'add_page'},
    {'title': "Зворотній зв'язок", 'url_name': 'contact'},
    {'title': 'Увійти', 'url_name': 'login'}
]


def index(request):
    posts = Women.objects.all()
    cats = Category.objects.all()
    context = {'posts': posts,
               'cats': cats,
               'menu': menu,
               'title':'Головна сторінка',
               'cat_selected': 0
               }

    return render(request,'women/index.html', context=context)


def about(request):
    return render(request,'women/about.html',
                  {'menu': menu, 'title': 'Про сайт'})


def categories(request, cat_id):
    return HttpResponse(f"<h1>Сторінка вибору категорій</h1><p>{cat_id}</p>")


def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent = False)

    return HttpResponse(f'<h1>Архів по рокам</h1><p>{year}</p>')


def contact(request):
    return HttpResponse("Зворотній зв'язок")


def login(request):
    return HttpResponse("Авторизація")


def add_page(request):
    return HttpResponse("Додати статтю")


def show_post(request, post_id):
    return HttpResponse(f"Відображення статті з id = {post_id}")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'cats': cats,
               'menu': menu,
               'title': 'Відображення по рубрикам',
               'cat_selected': cat_id
               }

    return render(request, 'women/index.html', context=context)
