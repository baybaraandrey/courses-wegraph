import uuid

from django.db import models
from django.db.models import (
    CharField,
    ForeignKey,
    ImageField,
    TextField,
    UUIDField,
    JSONField,
)

from model_utils.models import TimeStampedModel


def category_icon_path(instance, filename):
    return 'hls/category/%s/images/%s' % (
        instance.uid.hex,
        filename,
    )


def sub_category_icon_path(instance, filename):
    return 'hls/category/%s/sub_category/%s/images/%s' % (
        instance.category.uid.hex,
        instance.uid.hex,
        filename,
    )


def course_icon_path(instance, filename):
    return 'hls/category/%s/sub_category/%s/course/%s/images/%s' % (
        instance.sub_category.category.uid.hex,
        instance.sub_category.uid.hex,
        instance.uid.hex,
        filename,
    )


class Category(TimeStampedModel):
    class Meta:
        ordering = ['id']

    uid = UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = CharField(max_length=256, null=False, blank=True, default='')
    slug = CharField(max_length=256, unique=True, null=False, blank=True)
    icon = ImageField(max_length=1024, null=True, upload_to=category_icon_path)
    description = TextField(null=False, blank=True, default='')

    def __repr__(self):
        return 'Category(id=%d, name="%s", slug="%s")' % (
            self.id,
            self.name,
            self.slug,
        )

    def __str__(self):
        return self.__repr__()


class SubCategory(TimeStampedModel):
    class Meta:
        ordering = ['id']

    uid = UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    category = ForeignKey(
        Category,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_categories',
    )
    name = CharField(max_length=256, null=False, blank=True, default='')
    slug = CharField(max_length=256, unique=True, null=False, blank=True)
    icon = ImageField(max_length=1024, null=True, upload_to=sub_category_icon_path)
    description = TextField(null=False, blank=True, default='')

    def __repr__(self):
        return 'SubCategory(id=%d, name="%s", slug="%s")' % (
            self.id,
            self.name,
            self.slug,
        )

    def __str__(self):
        return self.__repr__()


class Course(TimeStampedModel):
    class Meta:
        ordering = ['id']

    uid = UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    sub_category = ForeignKey(
        SubCategory,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    name = CharField(max_length=256, null=False, blank=True, default='')
    slug = CharField(max_length=256, unique=True, null=False, blank=True)
    icon = ImageField(max_length=1024, null=True, upload_to=course_icon_path)
    description = TextField(null=False, blank=True, default='')


    def __repr__(self):
        return 'Course(id=%d, name="%s", slug="%s")' % (
            self.id,
            self.name,
            self.slug,
        )

    def __str__(self):
        return self.__repr__()
