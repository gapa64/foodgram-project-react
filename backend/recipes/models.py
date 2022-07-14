from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Тэг',

    )
    image = models.ImageField(
        blank=True,
        verbose_name='Картинка',
        upload_to='recipes_images'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='В рецептах'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Соответствующий Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиента 1')
        ],
        verbose_name='Количество'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_ingredient_recipe')
        ]

    def __str__(self) -> str:
        return f'{self.recipe}_{self.ingredient}'


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        related_name='carted_recipes',
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='buyers',
        on_delete=models.CASCADE,
        verbose_name='Рецепты в корзине'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='cart_user_recipe')
        ]

    def __str__(self):
        return f'{self.user}:{self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorited_recipes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorited_users',
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='favorite_user_recipe')
        ]

    def __str__(self):
        return f'{self.user}:{self.recipe}'
