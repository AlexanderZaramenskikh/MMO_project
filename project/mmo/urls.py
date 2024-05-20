from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('comment/<int:pk>', CommentView.as_view(), name='comment'),

    path('account/<int:pk>', CommentPk.as_view(), name='commentpk'),
    path('account/', AccountList.as_view(), name='account'),
    path('account/<int:pk>/delete', delete_response, name='delete_response'),
    path('account/<int:pk>/accept', accept_response, name='accept_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)