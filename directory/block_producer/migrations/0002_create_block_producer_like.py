# Generated by Django 2.2.3 on 2019-07-23 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('block_producer', '0001_create_block_producer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockProducerLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block_producer.BlockProducer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
