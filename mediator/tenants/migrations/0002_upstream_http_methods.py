from django.db import migrations, models
import tenants.models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstream',
            name='http_methods',
            field=models.CharField(
                default='',
                max_length=200,
                validators=[tenants.models.validate_http_methods]
            ),
        ),
    ]
