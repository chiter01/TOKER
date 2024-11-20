from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Furniture(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="furniture", verbose_name="Категория")
    image = models.ImageField(upload_to="furniture_images/", verbose_name="Изображение товара")
    available = models.BooleanField(default=True, verbose_name="Доступен для продажи")
    popularity = models.PositiveIntegerField(default=0, verbose_name="Популярность") 
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0, 
        verbose_name="Средний рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )  

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def update_rating(self):
        """
        Пересчитывает средний рейтинг на основе связанных отзывов.
        """
        reviews = self.reviews.all() 
        total_rating = sum(review.stars for review in reviews)
        self.rating = total_rating / reviews.count() if reviews.exists() else 0
        self.save()

class Image(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="images", verbose_name="Товар")
    image = models.ImageField(upload_to="furniture_images/", verbose_name="Дополнительное изображение")  

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение для {self.furniture.name}"

class Review(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="reviews", verbose_name="Товар")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Пользователь")
    stars = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.furniture.name}"
