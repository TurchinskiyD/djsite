from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse

from .forms import AddPostForm
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

    context = {'posts': posts,

               'menu': menu,
               'title': 'Головна сторінка',
               'cat_selected': 0
               }

    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html',
                  {'menu': menu, 'title': 'Про сайт'})


def categories(request, cat_id):
    return HttpResponse(f"<h1>Сторінка вибору категорій</h1><p>{cat_id}</p>")


def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=False)

    return HttpResponse(f'<h1>Архів по рокам</h1><p>{year}</p>')


def contact(request):
    return HttpResponse("Зворотній зв'язок")


def login(request):
    return HttpResponse("Авторизація")


def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Помилка додавання посту')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {
        'form': form,
        'menu': menu,
        'title': "Додавання статті",
    })


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {'post': post,
               'menu': menu,
               'title': post.title,
               'cat_selected': post.cat_id,
               }

    return render(request, 'women/post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


def show_category(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat.id)

    # if len(posts) == 0:
    #     raise Http404()

    context = {'posts': posts,
               'menu': menu,
               'title': 'Відображення по рубрикам',
               'cat_selected': cat.id
               }

    return render(request, 'women/index.html', context=context)
