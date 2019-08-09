from django.contrib import admin
from django.urls import path
import cbookapp.views
import account.views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cbookapp.views.index, name="index"),

    # share
    path('share', cbookapp.views.share, name="share"),
    path('share', cbookapp.views.search, name='search'),
    path('sharenew', cbookapp.views.sharenew, name="sharenew"),
    path('share/<int:codeshare_id>', cbookapp.views.sharedetail, name="sharedetail"),
    path('share/delete/<int:codeshare_id>', cbookapp.views.sharedelete, name="sharedelete"),
    path('share/edit/<int:codeshare_id>', cbookapp.views.shareedit, name="shareedit"),
   
    path('share/<int:codeshare_id>/sharecomment/comment_create', cbookapp.views.sharecomment_create,name="share_comment_create"),
    path('share/<int:codeshare_id>/sharecomment/<int:sharecomment_id>/delete', cbookapp.views.sharecomment_delete, name="share_comment_delete"),
    path('share/<int:codeshare_id>/sharecomment/<int:sharecomment_id>/replay_create',cbookapp.views.sharereplay_create,name="share_replay_create"),
    path('share/<int:codeshare_id>/sharecomment/<int:sharecomment_id>/<int:sharere_id>/replay_delete', cbookapp.views.sharereplay_delete, name="share_replay_delete"),

    # ask
    path('ask', cbookapp.views.ask, name="ask"),
    path('ask', cbookapp.views.searchAsk, name='searchAsk'),
    path('asknew', cbookapp.views.asknew, name="asknew"),
    path('ask/<int:codeask_id>', cbookapp.views.askdetail, name="askdetail"),
    path('ask/delete/<int:codeask_id>', cbookapp.views.askdelete, name="askdelete"),
    path('ask/edit/<int:codeask_id>', cbookapp.views.askedit, name="askedit"),

    path('ask/<int:codeask_id>/askcomment/comment_create', cbookapp.views.askcomment_create,name="ask_comment_create"),
    path('ask/<int:codeask_id>/askcomment/<int:askcomment_id>/delete', cbookapp.views.askcomment_delete, name="ask_comment_delete"),
    path('ask/<int:codeask_id>/askcomment/<int:askcomment_id>/replay_create',cbookapp.views.askreplay_create,name="ask_replay_create"),
    path('ask/<int:codeask_id>/askcomment/<int:askcomment_id>/<int:askre_id>/replay_delete', cbookapp.views.askreplay_delete, name="ask_replay_delete"),

    # accout
    path('account/signin', account.views.signin, name = "signin"),
    path('account/signup', account.views.signup, name = 'signup'),
    path('account/logout', account.views.logout, name= "logout"),

    # like
    path('share/<int:codeshare_id>/share_like', cbookapp.views.share_like, name="share_like"),
    # path('ask/<int:codeask_id>/ask_like/<int:askcomment.id>/ask_like', cbookapp.views.ask_like, name="ask_like"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
