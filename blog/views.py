
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from blog.models import Post, Category
from django.views.generic import ListView, DetailView
# rest framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog.serializers import PostSerializer


# templates views
class CategoryView(ListView):
    queryset = Category.objects.filter()
    template_name = 'blog/category.html'


class PostListView(ListView):
    model =  Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = (str(self.kwargs['slug']))
        category1 = category.replace("-"," ")
        return Post.objects.filter(category__title=category1)



class PostDetailView(DetailView):
    queryset = Post.objects.filter(status='PB')
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        print(post)
        session_key = 'viewed_post_{}'.format(post.id)
        if not request.session.get(session_key, False):
            post.views +=1
            post.save()

        context = {
            'post' : post,
            'post_dict': {
                'title':post.title,
                'description':post.description,
                'author':post.author,
                'views':post.views,
                'date_published':post.publish,
            }

        }
        return render(request, 'blog/detail.html',context)



# rest views
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views +=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
