from django.contrib import admin
from .models import CodeShare, CodeAsk, ShareComment, ShareRe, AskComment, AskRe, Like
# , AskLike
# Register your models here.
admin.site.register(CodeShare)
admin.site.register(CodeAsk)

admin.site.register(ShareComment)
admin.site.register(ShareRe)

admin.site.register(AskComment)
admin.site.register(AskRe)
admin.site.register(Like)
# admin.site.register(AskLike)
