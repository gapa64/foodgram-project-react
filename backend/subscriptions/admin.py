from django.contrib import admin

from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user')
    search_fields = ('author', 'user')
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
