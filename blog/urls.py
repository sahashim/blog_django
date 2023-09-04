
from django.urls import path
from blog.views import *


urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('list/<slug>', PostListView.as_view(), name='post_list'),
    path('detail/<slug>', PostDetailView.as_view(), name='post_detail')
]