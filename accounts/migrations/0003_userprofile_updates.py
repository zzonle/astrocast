from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='unit_system',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='temperature_unit',
            field=models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit'), ('K', 'Kelvin')], default='C', max_length=1),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription_plan',
            field=models.CharField(choices=[('free', 'Gratuito'), ('premium', 'Premium'), ('pro', 'Profesional')], default='free', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription_expires',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('es', 'Español'), ('en', 'English'), ('fr', 'Français'), ('pt', 'Português')], default='es', max_length=10),
        ),
    ]
