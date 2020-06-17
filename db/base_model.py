from django.db import models


class BaseModel(models.Model):
    """
    模型抽象基类
    """
    create_time = models.DateTimeField(verbose_name='创建用户时间', help_text='创建用户时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='删除标记', help_text='删除标记', default=False)

    class Meta:
        # 说明是一个抽象模型类(migrate时不会生成数据表)
        abstract = True
