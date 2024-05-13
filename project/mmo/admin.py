from django.contrib import admin
from .models import Post, Comment, Author

admin.site.register(Comment)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ('user', 'nickname',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('pk', 'author', 'title', 'post_time')
    list_filter = ('author', 'post_time')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)



