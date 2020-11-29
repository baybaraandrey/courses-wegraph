from django.views.generic import TemplateView, DetailView
from django.core import paginator

from .models import Category, Course, SubCategory


class IndexView(TemplateView):
    template_name = 'hls/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('id').all()
        # SEO
        context['title'] = 'Видеокурсы по программированию'
        context['description'] = 'Видеокурсы по программированию'

        return context


class SubCategoryListView(DetailView):
    template_name = 'hls/subcategory_detail.html'

    model = SubCategory
    context_object_name = 'subcategory'
    slug_url_kwarg = 'subcategory'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('id').all()

        context['is_paginated'] = True
        courses = Course.objects.filter(
            sub_category=kwargs['object'],
        ).order_by('id').select_related('sub_category')

        paging = paginator.Paginator(
                courses,
                self.request.GET.get('page_size', self.paginate_by),
            )
        try:
            context['courses'] = paging.page(self.request.GET.get('page', 1))
        except paginator.InvalidPage:
            context['courses'] = paging.page(1)

        # SEO
        context['title'] = 'Видеокурсы по программированию'
        context['description'] = 'Видеокурсы по программированию'

        return context


class CourseDetailView(DetailView):
    template_name = 'hls/course_detail.html'

    model = Course
    context_object_name = 'course'
    slug_url_kwarg = 'course'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('id').all()

        context['title'] = 'Видеокурсы по программированию'
        context['description'] = 'Видеокурсы по программированию'

        return context
