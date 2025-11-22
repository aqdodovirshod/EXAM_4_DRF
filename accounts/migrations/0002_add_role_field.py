# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('seeker', 'Seeker'), ('employer', 'Employer')], default='seeker', max_length=10),
        ),
    ]

