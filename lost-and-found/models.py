# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsBadge(models.Model):
    name = models.CharField(max_length=255)
    points_required = models.IntegerField()
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'accounts_badge'


class AccountsFaculty(models.Model):
    faculty_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'accounts_faculty'


class AccountsReward(models.Model):
    points = models.IntegerField()
    created_at = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_reward'


class AccountsRewardBadges(models.Model):
    reward = models.ForeignKey(AccountsReward, models.DO_NOTHING)
    badge = models.ForeignKey(AccountsBadge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_reward_badges'
        unique_together = (('reward', 'badge'),)


class AccountsUserprofile(models.Model):
    faculty = models.ForeignKey(AccountsFaculty, models.DO_NOTHING)
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)
    avatar = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'accounts_userprofile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


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


class ChatsChat(models.Model):
    theme = models.CharField(max_length=255)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'chats_chat'


class ChatsMessage(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    seen = models.BooleanField()
    chat = models.ForeignKey(ChatsChat, models.DO_NOTHING)
    to = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'chats_message'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

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


class PostsAssettype(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'posts_assettype'


class PostsComment(models.Model):
    msg = models.CharField(max_length=255)
    post = models.ForeignKey('PostsPost', models.DO_NOTHING)
    create_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts_comment'


class PostsPost(models.Model):
    is_active = models.BooleanField()
    type = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    create_at = models.DateTimeField()
    desc = models.TextField()
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact1 = models.CharField(max_length=255)
    contact2 = models.CharField(max_length=255)
    key = models.CharField(unique=True, max_length=255, blank=True, null=True)
    take_information = models.CharField(max_length=255, blank=True, null=True)
    assettype = models.ForeignKey(PostsAssettype, models.DO_NOTHING, db_column='assetType_id')  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts_post'


class PostsPostpicture(models.Model):
    picture = models.CharField(max_length=100)
    post = models.ForeignKey(PostsPost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'posts_postpicture'
