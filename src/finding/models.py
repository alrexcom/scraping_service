
from django.db import models
from django.utils import timezone

from finding.utils import from_cyrillic_to_eng


class City(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Наименование населённого пункта", unique=True)
    slug = models.CharField(max_length=50, blank=True, verbose_name='Тэги')

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Наименование населённых пунктов"

        ordering = ['name']

    def save(self, *args, **kwargs):
        """Переопределим сохранение slug"""
        if not self.slug:
            # Сохраним name в slug английскими буквами
            self.slug = from_cyrillic_to_eng(self.name)
        # Продолжим первоначальную функцию save
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Язык программирования", unique=True)
    slug = models.CharField(max_length=50, blank=True, verbose_name='Тэги')

    class Meta:
        verbose_name = "Язык программирования"
        verbose_name_plural = "Языки программирования"

        ordering = ['name']

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    """
    Для сохранения вакансий
    """
    title = models.CharField(max_length=250, verbose_name="Наименование вакансии")
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name="Язык программирования")
    url = models.URLField(max_length=500, unique=True)
    company = models.CharField(max_length=250, verbose_name="Работодатель")
    description = models.TextField(verbose_name="Описание вакансии")
    # default date
    timestamp = models.DateField(default=timezone.now)

    # timestamps = models.DateField(auto_now_add=True, default=django.utils.timezone.now)

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title
