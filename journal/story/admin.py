from django.contrib import admin
from .models import Entry

class ArticleAdmin(admin.ModelAdmin):

    actions = ['make_published']

    @admin.action(description='Save As Json')
    def make_published(self, request, queryset):
        queryset.update(status='p')




admin.site.register(Entry, ArticleAdmin)



# admin.site.register(Entry)
