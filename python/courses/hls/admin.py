from django.contrib import admin


from .models import Category, Course, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'name', 'slug']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'name', 'slug', 'category']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'name', 'slug', 'sub_category']
