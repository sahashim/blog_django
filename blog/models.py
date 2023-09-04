from audioop import reverse
from datetime import timezone
from users.models import CustomUser
from django.db import models

# Create your models here.


#baseDate
class BaseDate(models.Model):
    publish = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

#category
class Category(BaseDate):
    title = models.CharField(max_length=20)
    slug = models.CharField(max_length=45)
    def __str__(self):
        return f"title: {self.title}"

    class Meta:
        verbose_name_plural = "categories"


#status
class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'
    REJECTED = 'RJ', 'Rejected'



class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_del=False)
    def get_deleted(self):
        return super().get_queryset().filter(is_del=True)
    def get_all(self):
        return super().get_queryset().all()


# post
class Post(BaseDate):
    # relations
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_posts",help_text="enter author name")
    # data fields
    title = models.CharField(max_length=250,help_text="enter title",blank=True,db_index=True)
    description = models.TextField(help_text="enter description")
    slug = models.SlugField(max_length=250,help_text="enter slug")
    is_del = models.BooleanField(default=False)
    views=models.PositiveIntegerField(default=0)
    # category
    category = models.ForeignKey(Category, on_delete=models.CASCADE,help_text="enter category")
    # choice fields
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    #objects = models.Manager()
    objects = BaseManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])]
        verbose_name_plural = "Posts"


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_list', args=[self.id])


class Comment(BaseDate):
    writer = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="user_comments",help_text="enter your name")
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.content[:5]} by {self.writer} on post {self.post.title}"

