from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('post/<slug>/', views.post, name = 'post'),
    path('post/<slug:slug>/', views.post, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/unlike/',views.unlike_post,name='unlike_post'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('postlist/<slug>/', views.postlist, name='postlist'),
    path('posts/', views.allposts, name='allposts'),
    path('kitabs/', views.kitabs, name='kitabs'),
    path('post/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('post/<int:post_id>/report/', views.report_post, name='report_post'),
    path('tag/<int:tag_id>/', views.posts_by_tag, name='posts_by_tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)