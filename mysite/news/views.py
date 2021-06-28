import django.views
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import News, Category
from django.urls import reverse_lazy
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('homes')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homes')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(requset):
    logout(requset)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'Hello World'
    paginate_by = 3

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('homes')
    # login_url = '/admin/'
    raise_exception = True

# def index(request):
#     # news = News.objects.order_by('-created_at') # получить все записи из базы данных с сортирвокой
#     news = News.objects.all()  # получить все записи из базы данных
#     # categories = Category.objects.all()
#
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         # 'categories': categories,
#
#     }
#     return render(request, template_name='news/index.html', context=context)

# old way for adding and rendering data
# res = '<h1>List of news</h1>'
# for item in news:
#     res += f'<div>\n<p>{item.title}</p>\n<p>{item.content}</p>\n</div>\n<hr>\n'
# return HttpResponse(res)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     # categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     return render(request, template_name='news/category.html', context={'news': news,
#                                                                         'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, template_name='news/view_news.html', context={'news_item': news_item})
#
#
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
