from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from subscriptions.models import Follow


class FollowerInLine(admin.TabularInline):
    model = Follow
    fk_name = 'user'
    extra = 0


class CustomUserAdmin(UserAdmin):

    def followers_count(self, obj):
        return obj.follower.all().count()

    followers_count.short_description = 'Число подписчиков'
    list_display = ('id', 'username', 'email', 'followers_count')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    inlines = (FollowerInLine, )


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
