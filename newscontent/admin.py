from django.contrib import admin
from .models import Publisher, Author, Newscontent, SiteUser

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')

class NewscontentAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    fields = ('authors','title', 'publisher','publication_date')
    filter_horizontal = ('authors',)
    # raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Newscontent,NewscontentAdmin)
admin.site.register(SiteUser)