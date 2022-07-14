from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe, Favorite, Cart


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color')
    search_fields = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


class IngredientDropAdmin(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    max_num = 20


class RecipeAdmin(admin.ModelAdmin):

    def favorite_count(self, obj):
        return obj.favorited_users.all().count()

    favorite_count.short_description = 'Добавлений в избранное'
    inlines = (IngredientDropAdmin, )
    list_display = (
        'name',
        'author',
        'favorite_count'
    )
    search_fields = (
        'name',
        'author__username',
        'author__email',
        'tags__slug'
        'tags__name'
    )
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, FavoriteAdmin)
