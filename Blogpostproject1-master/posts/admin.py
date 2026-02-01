from django.contrib import admin

from .models import Author, Category, Post, Comment, Report, Tag, Kitab, Tag1, About

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Kitab)
admin.site.register(About)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reason", "created_at")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("title", "created_at", "updated_at")
    filter_horizontal = ("tags",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


@admin.register(Tag1)
class TagAdmin(admin.ModelAdmin) :
    list_display = ('id' , 'name' , 'created_at')
