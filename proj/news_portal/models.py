from django.db import models
from django.contrib.auth.models import User
from news_portal.resources import NEWS_TYPES


class User(User):
    pass


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.author_rating = 0
        posts_self = Post.objects.filter(username_id=self.username_id).values("post_rating")
        for i in posts_self:
            self.author_rating += i.get("post_rating")
        self.author_rating *= 3

        comments_self = Comment.objects.filter(username_id=self.username_id).values("comment_rating")
        for i in comments_self:
            self.author_rating += i.get("comment_rating")

        comments_other = Comment.objects.filter(post__username_id=self.username_id).values("comment_rating")
        for i in comments_other:
            self.author_rating += i.get("comment_rating")

        self.save()


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)


class Post(models.Model):
    username = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=3, choices=NEWS_TYPES, default="***")
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
