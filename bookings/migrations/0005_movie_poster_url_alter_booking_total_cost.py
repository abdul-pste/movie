# Generated by Django 5.1.3 on 2024-12-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_tickets_booking_total_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]