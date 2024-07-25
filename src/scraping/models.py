from django.db import models
from django.utils import timezone

from scraping.utils import from_cyrillic_to_eng


class City(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Наименование населённого пункта", unique=True)
    slug = models.CharField(max_length=60, blank=True, verbose_name='Тэги')

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
    slug = models.CharField(max_length=60, blank=True, verbose_name='Тэги')

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
    url = models.URLField(unique=True)
    site = models.URLField(max_length=250, verbose_name="Сайт", default=None, null=True)
    company = models.CharField(max_length=250, verbose_name="Работодатель")
    salary = models.CharField(max_length=250, verbose_name="Вознаграждение", default=None, null=True)
    opyt = models.CharField(max_length=150, verbose_name="Опыт", default=None, null=True)
    skills = models.CharField(max_length=250, verbose_name="Требования", default=None, null=True)
    address = models.CharField(max_length=250, verbose_name="Адрес компании", default=None, null=True)
    date_public = models.CharField(max_length=250, verbose_name="Опубликовано", default=None, null=True)
    errors_url = models.URLField(max_length=250, verbose_name="Ошибочный детальный url", default=None, null=True)
    logo_url = models.URLField(max_length=250, verbose_name="Ссылка лого компании", default=None, null=True)
    company_url = models.URLField(max_length=250, verbose_name="Ссылка на фирму", default=None, null=True)
    job_day = models.CharField(max_length=150, verbose_name="Занятость", default=None, null=True)
    description = models.TextField(verbose_name="Описание вакансии")
    # default date
    timestamp = models.DateField(default=timezone.now)

    # timestamps = models.DateField(auto_now_add=True, default=django.utils.timezone.now)

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(default=timezone.now)
    data = models.JSONField(default=dict)
