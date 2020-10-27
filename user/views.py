from django.shortcuts import render,redirect
from .forms import UserCreationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

def register(request):
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
           new_user=form.save(commit=False)
           new_user.set_password(form.cleaned_data['password1'])
           new_user.save()
            #username=form.cleaned_data['username']
           messages.success(request,f'تهانينا{new_user}  لقد تمت عملية التسجيل')
           return redirect('login')
    else:
        form=UserCreationForm()
    return render(request,'user/register.html',{
        'title':'التسجيل',
        'form':form,
     })


def Login_user(request):
    if request.method =='POST':
        
        form=LoginForm(request.POST)
        username=request.POST['username']
        password=request.POST['password']
     
        uu=authenticate(request,username=username,password=password)        
        if uu is not None:    
            login(request,uu) 
            return redirect('profile')                   
        else:
            messages.warning(request,' هناك خطأ في كلمة المرور أو الاسم')  
       
    else:
        form=LoginForm()   
    
    return render(request,'user\login.html',{
                        'title':'تسجيل خروج',
                        'form':form,
            })


def Logout_user(request):
    logout(request)
    return render(request,'user/logout.html',{
        'title':'تسجيل الخروج',
    })



@login_required(login_url='login')
def profile(request):
    posts=Post.objects.filter(author=request.user)
    post_list=Post.objects.filter(author=request.user)
    paginator=Paginator( post_list,2)
    page=request.GET.get('page')
    try:
         post_list=paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_page)
    return render(request,'user/profile.html',{
        'title':'الملف الشخصي',
        'posts':posts,
        'post_list':post_list,
        'page':page,

    })    