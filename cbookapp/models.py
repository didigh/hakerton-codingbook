from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
import re


# Create your models here.

class CodeShare(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'shareimage/', blank = True, null = True)
    body = models.TextField()
    codes = models.TextField(default='코드 없음')
    pub_date = models.DateTimeField(default=datetime.now,blank=True)    
    subject = models.CharField(max_length=50) 
    university = models.CharField(max_length=50,default='없음') #대학교는 옵션이기때문에
    score = models.CharField(max_length=50,default='없음')
    writer = models.CharField(max_length=50,default='any_user')

    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_user_set', through='Like')

    @property
    def like_count(self):
        return self.like_user_set.count()
   
    def __str__(self):
        return self.title

    def sum(self):
        return self.body[:100]

    def codesum(self):
        return self.codes[:30]

class ShareComment(models.Model):
    post=models.ForeignKey(CodeShare,on_delete=models.CASCADE,null=True,related_name='comments')
    contents=models.CharField(max_length=200)
    com_writer = models.CharField(max_length=50,default='any_user')
   
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.contents

class ShareRe(models.Model):
    comment=models.ForeignKey(ShareComment,on_delete=models.CASCADE,null=True,related_name='replies')
    contents=models.CharField(max_length=200)
    re_writer = models.CharField(max_length=50,default='any_user')

    class Meta:
        ordering = ['-id']

    def __str__(self):  
        return self.contents


    
class CodeAsk(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'askimage/', blank = True, null = True)
    body = models.TextField()
    codes = models.TextField(default='코드 없음')
    pub_date = models.DateTimeField(default=datetime.now,blank=True)    
    subject = models.CharField(max_length=50)
    #질문게시판은 학교에 상관없이 누구나 글을 쓸 수 있는 열린공간이기때문에 학교를 없앰.
    writer = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def sum(self):
        return self.body[:100]

    def codesum(self):
        return self.codes[:30]

class AskComment(models.Model):
    post=models.ForeignKey(CodeAsk,on_delete=models.CASCADE,null=True,related_name='comments')
    contents=models.CharField(max_length=200)
    com_writer = models.CharField(max_length=50,default='any_user')
    # likeask_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likeask_user_set', through='Like')

    # @property
    # def like_count(self):
    #     return self.likeask_user_set.count()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.contents

class AskRe(models.Model):
    comment=models.ForeignKey(AskComment,on_delete=models.CASCADE,null=True,related_name='replies')
    contents=models.CharField(max_length=200)
    re_writer = models.CharField(max_length=50,default='any_user')
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.contents

class Like(models.Model):
    post = models.ForeignKey(CodeShare, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)    

# class AskLike(models.Model):
#     post = models.ForeignKey(AskComment, on_delete = models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)    