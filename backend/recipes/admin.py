from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe, Favorite, Cart


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'ingredient', 'recipe')
    search_fields = ('recipe', 'ingredient', )
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


class IngredientDropAdmin(admin.StackedInline):
    model = Recipe.ingredients.through
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientDropAdmin, )
    list_display = ('name', 'author',)
    search_fields = ('name', )
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
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
