# Generated by Django 2.1.7 on 2019-04-23 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_auto_20190416_2229'),
        ('accounts', '0013_auto_20190416_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='quizes',
            field=models.ManyToManyField(blank=True, default=None, to='courses.Quiz'),
        ),
    ]