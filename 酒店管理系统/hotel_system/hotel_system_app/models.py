from django.db import models


# Create your models here.


class Room(models.Model):
    RoomID = models.IntegerField(

        verbose_name="房间号"
    )
    RoomType = models.CharField(
        max_length=10,
        verbose_name="房间类型"
    )
    RoomArea = models.FloatField(
        verbose_name="房间面积"
    )
    RoomBed = models.IntegerField(
        verbose_name="房间床位"
    )
    RoomPrice = models.FloatField(
        verbose_name="房间单价"
    )
    RoomWifi = models.BooleanField(
        default=True,
        verbose_name="是否有宽带"
    )
    RoomRemarks = models.CharField(
        null=True,
        max_length=100,
        verbose_name="房间备注"
    )
    Is_Reservation = models.BooleanField(
        default=False,
        verbose_name="是否预定"
    )
    Is_Check_in = models.BooleanField(
        default=False,
        verbose_name="是否入住"
    )
    Is_Stop = models.BooleanField(
        default=False,
        verbose_name="是否停用"
    )

    def __str__(self):
        self.RoomID = str(self.RoomID)
        return self.RoomID


class Reservation(models.Model):
    ReservationID = models.CharField(
        max_length=20,
        verbose_name="订单号",
    )
    User_name = models.CharField(
        max_length=20,
        verbose_name="用户姓名"
    )
    User_sex = models.BooleanField(
        verbose_name="用户性别"
    )
    User_cred_type = models.CharField(
        max_length=10,
        verbose_name="证件类型"
    )
    User_cred_num = models.CharField(
        max_length=30,
        verbose_name="证件号"
    )
    User_phone = models.CharField(
        max_length=15,
        verbose_name="用户电话"
    )
    Check_time = models.DateField(
        verbose_name="入住时间"
    )
    Check_days = models.IntegerField(
        verbose_name="入住天数"
    )
    Reservation_roomID = models.OneToOneField(
        Room,
        verbose_name="房间号",

    )
    Deposit_money = models.FloatField(
        verbose_name="押金"
    )
    Is_Check_in = models.BooleanField(
        default=False,
        verbose_name="是否入住"
    )

    def __str__(self):
        self.ReservationID = str(self.ReservationID)
        return self.ReservationID


class CheckIn(models.Model):
    CheckID = models.CharField(
        max_length=20,
        verbose_name="订单号",
    )
    User_name = models.CharField(
        max_length=20,
        verbose_name="用户姓名"
    )
    User_sex = models.BooleanField(
        verbose_name="用户性别"
    )
    User_cred_type = models.CharField(
        max_length=10,
        verbose_name="证件类型"
    )
    User_cred_num = models.CharField(
        max_length=30,
        verbose_name="证件号"
    )
    User_phone = models.CharField(
        max_length=15,
        verbose_name="用户电话"
    )
    Check_time = models.DateField(
        verbose_name="入住时间"
    )
    Check_days = models.IntegerField(
        verbose_name="入住天数"
    )
    Check_roomID = models.OneToOneField(
        Room,
        verbose_name="房间号",

    )
    Deposit_money = models.FloatField(
        verbose_name="押金"
    )

    def __str__(self):
        self.CheckID = str(self.CheckID)
        return self.CheckID
