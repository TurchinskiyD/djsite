from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView

from .forms import AddPostForm
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


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


class AddPage(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додавання статті')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowPost(DataMixin, DeleteView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
