from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_weatherquery'),
    ]

    operations = [
        # Agregar deleted_at a Location
        migrations.AddField(
            model_name='location',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
