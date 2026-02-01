from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    favorites = models.ManyToManyField(User, blank=True, related_name='favorite_posts')
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField('Tag', blank=True)


    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')

    def total_likes(self):
        return self.likes.count()
    

    unlikes = models.ManyToManyField(User, blank=True, related_name='unliked_posts')

    def total_unlikes(self):
        return self.unlikes.count()


    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}-{self.post}"

class Report(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Uyğun deyil'),
        ('spam', 'Spam'),
        ('hate_speech', 'Nifrət nitqi'),
        ('violence', 'Şiddet'),
        ('copyright', 'Müəllif hüquqları'),
        ('other', 'Digər'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')  
 
    def __str__(self):
        return f"{self.post.id} - {self.user.username} - {self.reason}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Kitab (models.Model):
    name = models.CharField(max_length=100)
    writername = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    @property
    def get_avatar_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/no-image.png' 
    
class About(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    thumbnail = models.ImageField(blank=True, null=True)  

    def __str__(self):
        return self.title

