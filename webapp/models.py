from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models.deletion import get_candidate_relations_to_delete


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Product(models.Model):
    CATEGORIES = [
        ('did not apply', 'Не задано'),
        ('drinks', 'Лимонады'),
        ('cakes', 'Торты'),
    ]
    product = models.CharField(max_length=20, null=False, blank=False)
    category = models.CharField(null=False, blank=False, choices=CATEGORIES, verbose_name='Категория', max_length=20)
    description = models.TextField(max_length=100, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='product_pics', verbose_name='Картинка')
    is_deleted = models.BooleanField(default=False)
    objects = CustomModelManager()
    user = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name='Пользователь')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for rel in delete_candidates:
                if rel.on_delete.__name__ == 'CASCADE' and rel.one_to_many and not rel.hidden:
                    for item in getattr(self, rel.related_name).all():
                        item.delete()
        self.save(update_fields=['is_deleted', ])

    def __str__(self):
        return f'{self.product}'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор')
    product = models.ForeignKey('webapp.Product',
                                related_name='reviews',
                                on_delete=models.CASCADE,
                                verbose_name='Продукт')
    text = models.TextField(max_length=400,
                            verbose_name='Комментарий', blank=False)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)

    is_deleted = models.BooleanField(default=False)
    objects = CustomModelManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted', ])

    def __str__(self):
        return self.text[:20]
