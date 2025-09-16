from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Source(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    source_type = models.CharField(max_length=50, choices=[
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('other', 'Другое')
    ], verbose_name="Тип источника")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"


class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты")
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Источник")
    weight = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Вес (1-10)"
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        unique_together = ['text', 'source']


class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата")
    is_like = models.BooleanField(verbose_name="Лайк (True) или дизлайк (False)")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Лайк/Дизлайк"
        verbose_name_plural = "Лайки/Дизлайки"
        unique_together = ['quote', 'ip_address']