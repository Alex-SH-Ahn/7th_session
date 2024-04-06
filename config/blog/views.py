from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.core.paginator import Paginator #페이지네이터를 사용할 수 있도록 import

# READ
def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3) #3개의 게시글까지 조회 가능
    page_number = request.GET.get('page') #쿼리 파라미터에 page가 뜸 (url이동 위해
    page_obj = paginator.get_page(page_number) #페이지 넘버를 가지고 오는 함수
    return render(request, 'home.html', {'page_obj': page_obj})

    #만든 요리를 바로 주면 안되고, 그릇(template)에 담아야함
    #home.html에 blog를 'blogs'라는 이름으로 바인딩할거야

# DETAIL READ
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog})

# CREATE
def new(request):
    return render(request, 'new.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.content = request.POST['content']
    new_blog.image = request.FILES.get('image')
    new_blog.save()
    return redirect('detail', new_blog.id) 

    #post요청을 get요청으로 바꿔버린 것 
    # return render(request, 'detail.html', {'blog': new_blog})
    # render를 사용하지 않는 이유는?
    # 손님이 post요청을 보냄, 렉이 걸림 -> 새로고침 연타, redirect를 사용했다면 get요청으로 변경되었을텐데, post는 새로고침해도 post => 100만원 송금시엔 새로고침 할때마다 100만원 다시 보내짐
    # 그럼 왜 render를 사용하는가?
    # 렌더요청은 url은 안바뀌고, html은 변경됨.
    # redirect는 하나만 주는데, 렌더는 딕셔너리형식으로 보내줌. html에서 {{blog.title}}이 가능하게끔 함.

# UPDATE
def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'edit.html', {'edit_blog':edit_blog})

def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)
    # return render(request, 'detail.html', {'blog': old_blog})

# DELETE
def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')