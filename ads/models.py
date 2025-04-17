from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/У')
    ]
    CATEGORY_CHOICES = [
        ('tech', 'Техника'),
        ('wear', 'Одежда'),
        ('book', 'Книги')
    ]

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, default='new')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"(id {self.pk})  {self.title}"

    def get_absolute_url(self):
        return reverse('ad_details', kwargs={'ad_pk': self.pk})


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена')
    ]
    ad_sender = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, related_name='sent_proposals', verbose_name='Отправитель')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, related_name='received_proposals', verbose_name='Получатель')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Комментарий')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('proposal_details', kwargs={'proposal_pk': self.pk})
