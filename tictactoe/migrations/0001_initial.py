# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Active'), (b'F', b'First Player Wins'), (b'S', b'Second Player Wins'), (b'D', b'Draw')])),
                ('first_player', models.ForeignKey(related_name='games_first_player', to=settings.AUTH_USER_MODEL)),
                ('next_to_move', models.ForeignKey(related_name='games_to_move', to=settings.AUTH_USER_MODEL)),
                ('second_player', models.ForeignKey(related_name='games_second_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('comment', models.CharField(max_length=300)),
                ('game', models.ForeignKey(to='tictactoe.Game')),
            ],
        ),
    ]
