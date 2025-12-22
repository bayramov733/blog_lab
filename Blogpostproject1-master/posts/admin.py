from django.contrib import admin

from .models import Author, Category, Post, Tag, Car, Comment, About

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Car)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(About)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin) :
    list_display = ('id' , 'name' , 'created_at')

