from django.contrib import admin

from .models import Author, Category, Post, Tag, Kitab, Comment, About, Report
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Kitab)
admin.site.register(Comment)
admin.site.register(About)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("title", "created_at", "updated_at")
    filter_horizontal = ("tags",)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reason", "created_at")
