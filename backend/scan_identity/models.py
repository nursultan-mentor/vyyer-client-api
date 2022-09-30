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


scan = {"ID": 62251,
        "UserID": "auth0|60c4ddb2612d820070a5e2f6",
        "IdentityID": 16061,
        "CreatedAt": "2022-09-25 06:09:04",
        "Flags": 0,
        "VerdictType": 0,
        "VerdictResult": 0,
        "VerdictName": "Valid",
        "VerdictValue": "Valid",
        "VIP": 0,
        "Ban": 0}

identity = {
    "ID": 101,
    "UID": "yXQ/fAjUn8WCa86L9bnsKSOPodmivread8GwkGsHQKE=",
    "UserID": "{{Auth0UserID}}",
    "OrgID": "{{Auth0OrgID}}",
    "Orientation": 0,
    "LicenseNumber": "000000000",
    "Birthday": "1991-08-17",
    "IssuedAt": "2018-01-17",
    "ExpiresAt": "2023-08-17",
    "Height": "5ft 7in",
    "Weight": "ddd",
    "EyeColor": "BRO",
    "HairColor": "",
    "Address": "0000 Xxxxxxxx Xxxx, Denver, CO, 802200000, USA",
    "Street": "0000 XXXXXXXX XXXX",
    "City": "DENVER",
    "PostalCode": "802200000",
    "FullName": "Haylee Jean Wiggert",
    "FirstName": "Haylee",
    "MiddleName": "Jean",
    "LastName": "Wiggert",
    "Gender": "f",
    "Ban": 0,
    "BannedBy": "auth0|61608698f5a4030068cf636e",
    "BanStartAt": "1970-01-01 00:00:00",
    "BanEndAt": "2021-11-09 17:06:49",
    "VIP": 1,
    "VIPBy": "auth0|60c4ddb2612d820070a5e2f6",
    "VIPStartAt": "2022-09-28 16:38:10",
    "VIPEndAt": "2022-05-21 14:55:23",
    "Visits": 0,
    "State": "CO",
    "CreatedAt": "2021-08-03 17:00:08",
    "LastScannedAt": "",
    "ScansInPeriod": 0
}
