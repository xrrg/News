from django.db import models
# from django.contrib.auth.forms import User
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Article(models.Model):
    category = models.ForeignKey(Category)
    article_text = models.TextField()
    pub_date = models.DateTimeField('article was published')
    author_nickname = models.CharField(max_length=50)
    article_title = models.CharField(max_length=150)
    likes_number = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

class Comment(models.Model):
     article = models.ForeignKey(Article)
     com_nickname = models.CharField(max_length=50)
     comment_text = models.TextField()
     comment_pub_date = models.DateTimeField('comment was published')
     c_likes_number = models.IntegerField(default=0)
     author_id = models.IntegerField(default=0)

     def __str__(self):
        return self.comment_text


class ArticleLikeList(models.Model):
    related_article = models.ForeignKey(Article)
    user_nick = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user_nick

class CommentLikeList(models.Model):
    related_article = models.ForeignKey(Article)
    related_comment = models.ForeignKey(Comment)
    user_nick = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user_nick

class PrivateMessage(models.Model):

    author = models.ForeignKey(User, verbose_name='Author', db_column='author', related_name='author', max_length=30)
    reciever = models.ForeignKey(User, verbose_name='Reciever', db_column='reciever', related_name='reciever', max_length=30)
    header = models.CharField(max_length=200)
    message = models.TextField()
    was_send = models.DateTimeField("message was send")
    was_read = models.BooleanField(default=False)

    def __str__(self):
        return self.header