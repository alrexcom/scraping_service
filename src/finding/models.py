from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Наименование населённого пункта", unique=True)
    slug = models.CharField(max_length=50, blank=True, verbose_name='хрен знает что это')

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Наименование населённых пунктов"

        ordering = ['name']

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
