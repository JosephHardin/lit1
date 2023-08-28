# Generated by Django 2.1.15 on 2023-08-22 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='NONE', max_length=2552),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(default='NONE', max_length=25),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='NONE@NONE.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='NONE', max_length=25),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='NONE', max_length=255, primary_key=True, serialize=False),
        ),
    ]