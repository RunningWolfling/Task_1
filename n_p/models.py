from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum

class Author (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_rating = models.IntegerField(default = 0)


    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rate') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        print(author_posts_rating)
        print(author_post_comment_rating)
        print(author_post_comment_rating)
        self.rate = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] \
                    + author_post_comment_rating['comments_rating_sum']
        self.save()

    def __str__(self):
        return self.user.username

sport = 'SP'
political = 'PO'
weather = 'WE'
culture = 'CU'
THEMES = [
    (sport, 'Спорт'),
    (political, 'Политика'),
    (weather, 'Погода'),
    (culture, 'Культура')
]
class Category (models.Model):
    theme = models.CharField(
        max_length = 2,
        choices= THEMES,
        unique = True)

#    def __str__(self):
#        return self.name_category


news = 'NE'
article = 'AR'
POSITIONS = [
    (news, 'Новости'),
    (article, 'Статья')
]

class Post (models.Model):
    head = models.CharField (max_length = 100)
    text = models.TextField()
    position = models.CharField(
        max_length = 2,
        choices = POSITIONS,
        default = news)
    time_in = models.DateTimeField (auto_now_add = True)
    author = models.ForeignKey (Author, on_delete = models.CASCADE)
    post_category = models.ManyToManyField(Category, through = 'PostCategory')
    rating = models.IntegerField(default = 0)

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()


    def preview(self):
        prev = self.text[0:125] + "..."
        return prev


class PostCategory (models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    head = models.ForeignKey(Post, on_delete = models.CASCADE)


class Comment(models.Model):
    head = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text_comment = models.TextField()
    time_in_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()

