from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Recipe, Tag, Ingredient, IngredientRecipe, Favorite, Follow, Cart

User = get_user_model()

'''
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active',
                    'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
'''

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    search_fields = ('name', )
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'

class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient', )
    list_filter = ('recipe', 'ingredient', )
    empty_value_display = '-пусто-'

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'

class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', )
    search_fields = ('buyer', 'recipes')
    list_filter = ('buyer', 'recipes')
    empty_value_display = '-пусто-'

#admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)

