# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contracts(models.Model):
    con_id = models.AutoField(primary_key=True)
    con_name = models.CharField(max_length=40)
    path_to_file = models.CharField(max_length=100)
    added_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, db_column='added_by')
    test_only = models.IntegerField(blank=True, default=0)
    reg_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'contracts'


class Modality(models.Model):
    modal_id = models.SmallIntegerField(primary_key=True)
    modality = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modality'


class Clauses(models.Model):
    clause_id = models.AutoField(primary_key=True)
    con = models.ForeignKey(Contracts, on_delete=models.CASCADE, db_column='con_id')
    clause_range = models.CharField(max_length=10)
    modal = models.ForeignKey(Modality, on_delete=models.CASCADE, blank=True, null=True, db_column='modal_id')
    reg_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clauses'


class Conflicts(models.Model):
    conf_id = models.AutoField(primary_key=True)
    con = models.ForeignKey(Contracts, on_delete=models.CASCADE, db_column='con_id')
    clause_id_1 = models.ForeignKey(Clauses, on_delete=models.CASCADE, db_column='clause_id_1', related_name='first_clause')
    clause_id_2 = models.ForeignKey(Clauses, on_delete=models.CASCADE, db_column='clause_id_2', related_name='second_clause')
    generated = models.IntegerField(blank=True, null=True)
    added_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, db_column='added_by')
    reg_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conflicts'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ModalCorrections(models.Model):
    id_modal = models.IntegerField(primary_key=True)
    id_clause = models.ForeignKey(Clauses, on_delete=models.CASCADE, db_column='id_clause')
    id_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, db_column='id_user')
    id_modality = models.ForeignKey(Modality, models.CASCADE, db_column='id_modality')
    reg_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'modal_corrections'


# class Users(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=60)
#     email = models.CharField(max_length=40)
#     username = models.CharField(max_length=40)
#     password = models.CharField(max_length=64)
#     reg_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'users'
