from django.urls import path
from .views import post_list, post_detail, post_create, post_update, post_delete, add_comment_to_post, comment_delete

urlpatterns = [
    path('', post_list, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
]
