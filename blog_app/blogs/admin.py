from django.contrib import admin
from blogs.models import Blog, Category, Tag, Comment


admin.site.register([Category, Tag, Blog, Comment])