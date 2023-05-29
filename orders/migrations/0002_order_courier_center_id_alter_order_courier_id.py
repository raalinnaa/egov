# Generated by Django 4.1.3 on 2023-04-15 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courier', '0002_couriercouriercenter'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='courier_center_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courier.couriercenter', verbose_name='Courier center'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='courier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Courier'),
        ),
    ]
