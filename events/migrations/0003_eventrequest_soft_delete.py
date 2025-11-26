from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventrequest_weather_query_and_more'),
    ]

    operations = [
        # Agregar deleted_at a EventRequest
        migrations.AddField(
            model_name='eventrequest',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        # Remover opción 'deleted' del status de EventRequest ya que usamos deleted_at
        migrations.AlterField(
            model_name='eventrequest',
            name='status',
            field=models.CharField(
                choices=[('created', 'Creado'), ('processed', 'Procesado'), ('cancelled', 'Cancelado'), ('error', 'Error')],
                default='created',
                max_length=20
            ),
        ),
    ]
