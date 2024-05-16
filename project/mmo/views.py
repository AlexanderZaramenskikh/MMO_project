import datetime
import os

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.translation import get_language as lg
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from .forms import PostForm,CommentForm
from .models import Post,Comment


class MainView(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'main/posts.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.now()
        context['posts_quantity'] = len(Post.objects.all())
        return context


class PostView(ListView):
    model = Post
    template_name = 'main/post.html'
    context_object_name = 'post'

    # ordering = '-post_time'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        _id = self.kwargs.get('pk')
        context['time_now'] = datetime.datetime.utcnow()
        context['post'] = Post.objects.get(id=_id)
        return context


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    context_object_name = 'posts_today'
    template_name = 'main/create.html'
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.post_time = datetime.date.today()
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        return context


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'main/create.html'
    success_url = '/'


    def get_object(self, **kwargs):
        _id = self.kwargs.get('pk')
        return Post.objects.get(pk=_id)


class PostDeleteView(DeleteView):
    template_name = 'main/delete.html'
    model = Post
    queryset = Post.objects.all()
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context


def AboutView(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'static/main/txt/', Language(lg()))
    my_file = open(file_path, 'r+', encoding="UTF-8")
    txt = my_file.read()
    my_file.close()

    data = {
        'page': _('О нас'),
        'title': _('Мы очень крутые. Мы самые лучшие!!!!'),
        'text': txt,
    }
    return render(request, 'main/about.html', data)


def Language(cur_language):
    if cur_language == 'ru':
        return 'about_ru.txt'
    else:
        return 'about_en.txt'


class CommentView(CreateView):
    form_class = CommentForm
    model = Comment
    context_object_name = 'comment'
    template_name = 'main/comment.html'
    success_url = '/'

