# Generated by Django 4.0 on 2021-12-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorymodel',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='category_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='published_date'),
        ),
    ]