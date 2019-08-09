from django.shortcuts import render, redirect, get_object_or_404
from .models import CodeShare, CodeAsk, ShareComment, ShareRe, AskComment, AskRe, Like
from .forms import ShareNew, AskNew, ShareCommentForm, ShareReForm, AskCommentForm, AskReForm
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse



# Create your views here.

def index(request):
    return render(request, 'index.html')

# share관련 함수

def share(request):

        sharecodes = CodeShare.objects.all()
        search = 'Search..'

        if request.method == 'POST':
                search = request.POST.get('search')
                sharecodes = sharecodes.filter(title__contains=search)

        paginator = Paginator(sharecodes, 10)
        page = request.GET.get('page')
        try:
                posts = paginator.get_page(page)
        except PageNotAnInteger:
                posts = paginator.get_page(1)

        return render(request, 'share.html', {'sharecodes':sharecodes, 'posts':posts})



def search(request):     
    if request.method == 'POST':     
        bds = CodeShare.objects.all()
        b = request.POST.get('search')
        bds = CodeShare.objects.filter(title__contains=b)
        
        return render(request, 'share.html', {'bds' : bds})
    else:
        return render(request, 'share.html')
     

def sharedetail(request, codeshare_id):

    sharedetail = get_object_or_404(CodeShare, pk = codeshare_id)

    return render(request, 'sharedetail.html', {'sharedetail':sharedetail})

def sharedelete(reqeust, codeshare_id):
    
    sharedetail = get_object_or_404(CodeShare, pk = codeshare_id)
    sharedetail.delete()

    return redirect('share')

def sharenew(request):

    if request.method == 'POST':
        share_post =  CodeShare()
        share_form = ShareNew(request.POST, request.FILES)
        if share_form.is_valid(): 
            share_post = share_form.save(commit=False)

            share_post.pub_date = timezone.now()
            share_post.writer = request.user


            share_post.save()
        return redirect('share')
            
    else:

        share_form = ShareNew()

        return render(request, 'sharenew.html', {'share_form': share_form})

def shareedit(request, codeshare_id):

    shareedit = get_object_or_404(CodeShare, pk = codeshare_id)

    if request.method == 'POST':
        shareedit.title = request.POST['title']
        shareedit.body = request.POST['body']
        shareedit.codes = request.POST['codes']
        shareedit.subject = request.POST['subject']
        shareedit.university = request.POST['university']
        shareedit.score = request.POST['score']
        shareedit.writer = request.POST['writer']
        shareedit.save()

        return redirect('/share/'+str(shareedit.id))

    else:

        return render(request, 'shareedit.html', {'shareedit':shareedit})

def sharecomment_create(request, codeshare_id):
        if request.method=='POST':                
                post = get_object_or_404(CodeShare,pk=codeshare_id)
                form = ShareCommentForm(request.POST)               
                if form.is_valid():
                        comment=form.save(commit=False) 
                        comment.post=post                                              
                        comment.com_writer = request.user
                        comment.save()
                        return redirect('/share/'+str(post.id))
                        
        else:
                form=ShareCommentForm()
        paginator = Paginator(sharecodes, 3)
        page = request.GET.get('page')
        try:
                posts = paginator.get_page(page)
        except PageNotAnInteger:
                posts = paginator.get_page(1)
        
               # return render(request, 'share.html', {'sharecodes':sharecodes, 'posts':posts})
                
        return render(request,'sharedetail.html', {'form':form,'posts':posts})

def sharecomment_delete(request, codeshare_id, sharecomment_id):
        post = get_object_or_404(CodeShare, pk = codeshare_id)
        comment = get_object_or_404(ShareComment, pk = sharecomment_id)
        comment.delete()
        return redirect('/share/' + str(post.id))

def sharereplay_create(request, codeshare_id, sharecomment_id):        
        if request.method=='POST':
                post = get_object_or_404(CodeShare, pk = codeshare_id)
                comments = get_object_or_404(ShareComment, pk = sharecomment_id)
                re = ShareRe()
                form = ShareReForm(request.POST)
                if form.is_valid():
                        re = form.save(commit=False)
                        re.comment = comments
                        re.re_writer = request.user
                        re.save()
                        return redirect('/share/'+str(post.id))
        else:
                form = ReForm()
                return render(request,'sharedetail.html', {'form':form, 'comment': comments})

def sharereplay_delete(request, codeshare_id, sharecomment_id, sharere_id):
        post = get_object_or_404(CodeShare, pk = codeshare_id)
        comment = get_object_or_404(ShareComment, pk = sharecomment_id)
        re = ShareRe.objects.get(pk = sharere_id)
        re.delete()
        return redirect('/share/'+str(post.id))

@login_required
def share_like(request, codeshare_id):
    # 좋아요 구현 코드 작성
    # 구글링 시 '새로고침이 필요한 좋아요'로 찾으면 바로 나옵니다 !
    codeshare = get_object_or_404(CodeShare, pk=codeshare_id)
    # 중간자 모델 Like 를 사용하여, 현재 post와 request.user에 해당하는 Like 인스턴스를 가져온다.
    codeshare_like, codeshare_like_created = codeshare.like_set.get_or_create(user=request.user)
    
    if not codeshare_like_created:
        codeshare_like.delete()
        
    return redirect('/share/' + str(codeshare.id))

# ask관련 함수

def ask(request):

        askcodes = CodeAsk.objects.all()
        searchAsk = 'Search...'

        if request.method == 'POST':
                searchAsk = request.POST.get('searchAsk')
                askcodes = askcodes.filter(title__contains=searchAsk)

        paginator = Paginator(askcodes, 10)
        page = request.GET.get('page')
        try:
                posts = paginator.get_page(page)
        except PageNotAnInteger:
                posts = paginator.get_page(1)

        return render(request, 'ask.html', {'askcodes':askcodes, 'posts':posts})

def searchAsk(request):     
        bds = Board.objects.all()
        search = 'Search..'

        if request.method == 'POST':
                search = request.POST.get('search')
                bds = board_list.filter(title__contains=search)
                return render(request, 'ask.html', {'bds' : bds})
        else:
                return render(request, 'ask.html')



def askdetail(request, codeask_id):
    
    askdetail = get_object_or_404(CodeAsk, pk = codeask_id)

    return render(request, 'askdetail.html', {'askdetail':askdetail})

def askdelete(reqeust, codeask_id):

    askdetail = get_object_or_404(CodeAsk, pk = codeask_id)
    askdetail.delete()

    return redirect('ask')

def asknew(request):

    if request.method == 'POST':
        ask_post = CodeAsk()
        ask_form = AskNew(request.POST, request.FILES)
        if ask_form.is_valid(): 
            ask_post = ask_form.save(commit=False)

            ask_post.pub_date = timezone.now()
            ask_post.writer = request.user
            
            ask_post.save()
        return redirect('ask')
            
    else:

        ask_form = AskNew()

        return render(request, 'asknew.html', {'ask_form': ask_form})

def askedit(request, codeask_id):
    
    askedit = get_object_or_404(CodeAsk, pk = codeask_id)

    if request.method == 'POST':
        askedit.title = request.POST['title']
        askedit.body = request.POST['body']
        askedit.codes = request.POST['codes']
        askedit.subject = request.POST['subject']
        askedit.writer = request.POST['writer']
        askedit.save()

        return redirect('/ask/'+str(askedit.id))

    else:

        return render(request, 'askedit.html', {'askedit':askedit})

def askcomment_create(request, codeask_id):
        if request.method=='POST':
                post = get_object_or_404(CodeAsk,pk=codeask_id)
                form = AskCommentForm(request.POST)
                if form.is_valid():
                        comment=form.save(commit=False)
                        comment.post = post
                        comment.com_writer = request.user
                        comment.save()
                        return redirect('/ask/'+str(post.id))
        else:
                form = AskCommentForm()
                return render(request,'askdetail.html', {'form':form})

def askcomment_delete(request, codeask_id, askcomment_id):
        post = get_object_or_404(CodeAsk, pk = codeask_id)
        comment = get_object_or_404(AskComment, pk = askcomment_id)
        comment.delete()
        return redirect('/ask/' + str(post.id))

def askreplay_create(request, codeask_id, askcomment_id):        
        if request.method=='POST':
                post = get_object_or_404(CodeAsk, pk = codeask_id)
                comments = get_object_or_404(AskComment, pk = askcomment_id)
                re = AskRe()
                form = AskReForm(request.POST)
                if form.is_valid():
                        re = form.save(commit=False)
                        re.comment = comments
                        re.re_writer = request.user
                        re.save()
                        return redirect('/ask/'+str(post.id))
        else:
                form = AskReForm()
                return render(request,'askdetail.html', {'form':form, 'comment': comments})

def askreplay_delete(request, codeask_id, askcomment_id, askre_id):
        post = get_object_or_404(CodeAsk, pk = codeask_id)
        comment = get_object_or_404(AskComment, pk = askcomment_id)
        re = AskRe.objects.get(pk = askre_id)
        re.delete()
        return redirect('/ask/'+str(post.id))


        
# @login_required
# def ask_like(request, codeask_id, askcomment_id):
#     post = get_object_or_404(CodeAsk, pk = codeask_id)
#     comment = get_object_or_404(AskComment, pk = askcomment_id)
#     codeAsk_like, codeAsk_like_created = codeAsk.likeask_set.get_or_create(user=request.user)
    
#     if not codeAsk_like_created:
#         codeAsk_like.delete()
        
#     return redirect('/share/' + str(post.id))
