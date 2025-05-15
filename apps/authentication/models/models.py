from django.db import models


class User(models.Model):
    STATUS_CHOICES = (
        ('NORMAL', '正常'),
        ('DELETED', '删除'),
        ('DISABLED', '禁用'),
    )
    USER_TYPE_CHOICES = (
        ('ADMIN', '管理員'),
        ('USER', '普通用戶'),
    )
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像')
    dn = models.CharField(max_length=255, null=True, blank=True, )
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True, )
    gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    name = models.CharField(max_length=95, null=False, blank=True, verbose_name='姓名')
    password = models.CharField(max_length=95, null=False, blank=True, verbose_name='密码')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='电话')
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name='职位')
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES, default='NORMAL',
                              verbose_name='状态')
    user_type = models.CharField(max_length=255,
                                 choices=USER_TYPE_CHOICES, default='USER',
                                 verbose_name='用户类型')
    username = models.CharField(max_length=95, unique=True, verbose_name='用户名')
    api_key = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户openai的key值')
    secret_key = models.CharField(max_length=255, null=True, blank=True, verbose_name='2FA的密钥')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    last_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class UserExternal(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    given_name = models.CharField(max_length=255, verbose_name='名(first_name)')
    last_name = models.CharField(max_length=255, verbose_name='姓(last_name)')
    display_name = models.CharField(max_length=255, verbose_name='显示名(full_name)')
    ou = models.CharField(max_length=255, null=True, blank=True, verbose_name='所属组织单位')
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='关联的用户id')
    created_date = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    last_modified_date = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 't_user_external'
        verbose_name = 'AD用户拓展表'
        verbose_name_plural = 'AD用户拓展表'


class Group(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='分组名称，例如：手术医师组')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    scope_type = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name='作用域类型：DEPARTMENT、MODULE、SYSTEM')
    scope_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='作用域的具体ID')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    last_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')
    creator_id = models.CharField(max_length=255, verbose_name='创建者id')

    class Meta:
        db_table = 't_group'
        verbose_name = '分组表'
        verbose_name_plural = '分组表'


class GroupUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    group_id = models.CharField(max_length=255, verbose_name='分组id')
    user_id = models.CharField(max_length=255, verbose_name='用户id')

    class Meta:
        db_table = 't_group_user'


class Permission(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='权限名称')
    description = models.TextField(null=True, blank=True, verbose_name='权限描述')
    route = models.CharField(max_length=255, verbose_name='对应的系统路由或模块')
    detail = models.TextField(null=True, blank=True,
                              verbose_name='查看术前访视列表：previsit:get，术前访视评估：previsit:evaluate')

    class Meta:
        db_table = 't_permission'
        verbose_name = '权限表'
        verbose_name_plural = '权限表'


class GroupPermission(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    group_id = models.CharField(max_length=255, verbose_name='分组id')
    permission_id = models.CharField(max_length=255, verbose_name='权限id')

    class Meta:
        db_table = 't_group_permission'


class UserPermission(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    user_id = models.CharField(max_length=255, verbose_name='用户id')
    permission_id = models.CharField(max_length=255, verbose_name='权限id')

    class Meta:
        db_table = 't_user_permission'
