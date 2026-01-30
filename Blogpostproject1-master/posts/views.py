from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 
from .models import Category, Post, Author, Tag, Kitab, Comment, About, Report
from django.contrib.auth.decorators import login_required


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)

    post.views += 1
    post.save(update_fields=['views'])
    
    
    latest = Post.objects.order_by('-timestamp')[:3]
    comments=post.comments.filter(active=True)
    if request.method == 'POST' :
        if request.user.is_authenticated:
            content=request.POST.get('content')
            if content:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content
                )
                return redirect('post', slug=post.slug)
    context = {
        'post': post,
        'latest': latest,
        'comments': comments,
    }
    return render(request, 'post.html', context)

def about(request, slug=None):
    if slug:
        about_post = About.objects.get(slug=slug)
    else:
        about_post = About.objects.first()  
    
    context = {
        'about_post': about_post,
    }
    return render(request, 'about_page.html', context)

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)


def kitabs(request):
    q = request.GET.get('q')
    kitabs = Kitab.objects.all()

    if q:
        kitabs = kitabs.filter(
            Q(name__icontains=q) |
            Q(writername__icontains=q)
        )

    return render(request, 'kitabs.html', {'kitabs': kitabs})
 


def posts_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag)

    return render(request, "post_list.html", {
        "posts": posts,
        "tags": Tag.objects.all(),
        "active_tag": tag
    })



@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post', slug=slug)

@login_required
def unlike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.unlike.all():
        post.unlike.remove(request.user)
    else:
        post.unlike.add(request.user)
    return redirect('post', slug=slug)

@login_required
def toggle_favorite(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

@login_required
def favorite_list(request):
    posts = request.user.favorite_posts.all()
    return render(request, 'favorites.html', {'posts': posts})


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        report, created = Report.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'reason': reason, 'description': description}
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Şikayət göndərildi'})
        
        return redirect('post_detail', slug=post.slug)
    