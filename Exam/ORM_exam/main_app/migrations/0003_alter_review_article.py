# Generated by Django 4.2.4 on 2023-11-26 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_review_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_reviews', to='main_app.article'),
        ),
    ]
