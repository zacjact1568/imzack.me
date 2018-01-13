# Generated by Django 2.0.1 on 2018-01-13 09:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_excerpt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=200, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.CharField(max_length=50, verbose_name='文件'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='标题'),
        ),
    ]