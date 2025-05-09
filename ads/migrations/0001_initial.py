# Generated by Django 5.2 on 2025-04-17 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('condition', models.CharField(choices=[('new', 'Новое'), ('used', 'Б/У')], default='new', max_length=4)),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('category', models.CharField(choices=[('tech', 'Техника'), ('wear', 'Одежда'), ('book', 'Книги')], max_length=4, verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExchangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('accepted', 'Принята'), ('rejected', 'Отклонена')], default='pending', max_length=8, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('ad_receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='received_proposals', to='ads.ad', verbose_name='Получатель')),
                ('ad_sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sent_proposals', to='ads.ad', verbose_name='Отправитель')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
