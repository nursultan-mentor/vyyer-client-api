from django.db import models


class Identity(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=50)
    issued_at = models.DateField(null=True)
    expires_at = models.DateField(null=True)

    class Meta:
        db_table = 'identities'
        ordering = ['id']
        verbose_name = 'Identity'
        verbose_name_plural = 'Identities'

    def __str__(self):
        return f'{self.id} - {self.fullname}'


class Scan(models.Model):
    id = models.IntegerField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    flags = models.SmallIntegerField()
    verdict_type = models.SmallIntegerField()
    verdict_result = models.SmallIntegerField()
    verdict_name = models.CharField(max_length=10)
    verdict_value = models.CharField(max_length=10)

    class Meta:
        db_table = 'scans'
        ordering = ['id', ]
        verbose_name = 'Scan'
        verbose_name_plural = 'Scans'

    def __str__(self):
        return f'{self.user_id} - {self.verdict_name}'
