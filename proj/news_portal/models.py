from django.db import models
from django.contrib.auth.models import User
from news_portal.resources import TYPES


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_ratings = Post.objects.filter(username=self.username).values("post_rating")
        for pr in posts_ratings:
            self.author_rating += posts_ratings[pr]
            self.save()
        comments_ratings_self = Comment.objects.filter(username=self.username).values("comment_rating")
        for crs in comments_ratings_self:
            self.author_rating += comments_ratings_self[crs]
            self.save()
        posts_self = Post.objects.filter(username=self.username).values("post_id")
        for ps in posts_self:
            comments_ratings_other = Comment.objects.filter(post_id=posts_self[ps]).values("comment_rating")
            for cro in comments_ratings_other:
                self.author_rating += comments_ratings_other[cro]
            self.save()


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)


class Post(models.Model):
    username = models.CharField(max_length=30)
    post_type = models.CharField(max_length=3, choices=TYPES, default="Тип")
    created = models.DateTimeField(auto_now_add=True)
    post_cat = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=50, default="Title")
    text = models.TextField(default="Text")
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:123] + "..."  # Выводит первые 124 символа с многоточием в конце


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_cat = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="Text")
    created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
