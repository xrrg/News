from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Article(models.Model):
    category = models.ForeignKey(Category)
    article_text = models.TextField()
    pub_date = models.DateTimeField('article was published')
    author_nickname = models.CharField(max_length=50)
    article_title = models.CharField(max_length=50)
    was_liked = models.BooleanField(default=False)
    likes_number = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

class Comment(models.Model):
     article = models.ForeignKey(Article)
     com_nickname = models.CharField(max_length=50)
     comment_text = models.TextField()
     comment_pub_date = models.DateTimeField('comment was published')
     c_likes_number = models.IntegerField(default=0)
     c_was_liked = models.BooleanField(default=False)

     def __str__(self):
        return self.comment_text


