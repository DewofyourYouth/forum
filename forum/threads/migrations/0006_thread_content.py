# Generated by Django 4.0.3 on 2022-04-11 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0005_alter_comment_thread_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='content',
            field=models.TextField(null=True),
        ),
    ]