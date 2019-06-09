import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import *


# 测试 主页
def home(req):
    return render(req, "base.html")


# 客房查询
def query(req, param):
    # 判断请求方式为GET
    if req.method == "GET":
        page = req.GET.get("page", 1)
        # 判断参数，选择方法
        if param == "2":
            # 查找Room表中没有预约或没有入住或没有停用的数据对象
            Room_empty_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))
            # 创建一个分页器对象
            Paginator_empty_object = Paginator(Room_empty_object, 10)
            # 创建一个Page对象
            Page_empty_object = Paginator_empty_object.page(page)

            # 找出Page对象中的数据
            result = Page_empty_object.object_list
            # 返回的数据参数
            path = req.path
            data = {
                "result": result,
                "path": path,
                "page_range": Paginator_empty_object.page_range,
                "has_prev": Page_empty_object.has_previous(),
                "has_next": Page_empty_object.has_next(),
                "end_page": Paginator_empty_object.num_pages,
                "Page": Page_empty_object
            }
            # 渲染
            return render(req, "query.html", data)
        elif param == "3":
            # 查找Room表中已经入住的数据对象
            Room_checkin_object = Room.objects.filter(Is_Check_in=True)
            # 创建一个分页器对象
            Paginator_checkin_object = Paginator(Room_checkin_object, 10)
            # 创建一个Page对象
            Page_checkin_object = Paginator_checkin_object.page(page)
            # 找出Page对象中的数据
            result = Page_checkin_object.object_list
            # 返回数据参数
            path = req.path
            data = {
                "result": result,
                "path": path,
                "page_range": Paginator_checkin_object.page_range,
                "has_prev": Page_checkin_object.has_previous(),
                "has_next": Page_checkin_object.has_next(),
                "end_page": Paginator_checkin_object.num_pages,
                "Page": Page_checkin_object,
                "paginate": True
            }
            # 渲染
            return render(req, "query.html", data)
        elif param == "4":
            # 查找Room表中已经预约的数据对象
            Room_reservation_object = Room.objects.filter(Is_Reservation=True)
            # 创建一个分页器对象
            Paginator_reservation_object = Paginator(Room_reservation_object, 10)
            # 创建一个Page对象
            Page_reservation_object = Paginator_reservation_object.page(page)
            # 找出Page对象中的数据
            result = Page_reservation_object.object_list
            # 返回数据参数
            path = req.path
            data = {
                "result": result,
                "path": path,
                "page_range": Paginator_reservation_object.page_range,
                "has_prev": Page_reservation_object.has_previous(),
                "has_next": Page_reservation_object.has_next(),
                "end_page": Paginator_reservation_object.num_pages,
                "Page": Page_reservation_object,
                "paginate": True
            }
            # 渲染
            return render(req, "query.html", data)
        elif param == "5":
            # 查找Room表中已经停用的数据对象
            Room_stop_object = Room.objects.filter(Is_Stop=True)
            # 创建一个分页器对象
            Paginator_stop_object = Paginator(Room_stop_object, 10)
            # 创建一个Page对象
            Page_stop_object = Paginator_stop_object.page(page)
            # 找出Page对象中的数据
            result = Page_stop_object.object_list
            # 返回数据参数
            path = req.path
            data = {
                "result": result,
                "path": path,
                "page_range": Paginator_stop_object.page_range,
                "has_prev": Page_stop_object.has_previous(),
                "has_next": Page_stop_object.has_next(),
                "end_page": Paginator_stop_object.num_pages,
                "Page": Page_stop_object,
                "paginate": True
            }
            # 渲染
            return render(req, "query.html", data)
        else:
            # 查找Room表中所有的数据对象
            Room_all_object = Room.objects.all()
            # 创建一个分页器对象
            Paginator_all_object = Paginator(Room_all_object, 10)
            # 创建一个Page对象
            Page_all_object = Paginator_all_object.page(page)
            # 找出Page对象中的数据
            result = Page_all_object.object_list
            # 返回数据参数
            path = req.path
            data = {
                "result": result,
                "path": path,
                "page_range": Paginator_all_object.page_range,
                "has_prev": Page_all_object.has_previous(),
                "has_next": Page_all_object.has_next(),
                "end_page": Paginator_all_object.num_pages,
                "Page": Page_all_object
            }
            # 渲染
            return render(req, "query.html", data)

    else:
        # 解析参数
        param = req.POST

        # 解析前端输入的房间号
        RoomId = param.get("roomid")
        # 判断前端是否输入房间号
        # 有输入房间号
        if RoomId:
            # 查询Room表中对应房间号的数据对象
            Room_object = Room.objects.filter(RoomID=RoomId)
            # 创建一个分页器对象
            Paginator_object = Paginator(Room_object, 10)
            # 创建一个Page对象
            Page_object = Paginator_object.page(1)
            # 找出Page对象中的数据
            result = Page_object.object_list
        # 没有输入房间号
        else:
            # 查询Room表中所有的数据对象
            result = False

        # 返回数据参数

        data = {
            "result": result,
            "paginate": True

        }
        # 渲染
        return render(req, "query.html", data)


# 客房预约
def reservation(req):
    # 判断请求方式为GET
    if req.method == "GET":
        param = req.GET
        page = param.get("page", 1)
        # 查询Reservation表中所有的数据对象
        Reservation_all_object = Reservation.objects.filter(Is_Check_in=0)
        # 创建一个分页器对象
        Paginator_all_object = Paginator(Reservation_all_object, 5)
        # 创建一个Page对象
        Page_all_object = Paginator_all_object.page(page)
        # 找出Page对象中的数据
        result = Page_all_object.object_list
        path = req.path
        # 返回数据参数
        data = {
            "result": result,
            "path": path,
            "page_range": Paginator_all_object.page_range,
            "has_prev": Page_all_object.has_previous(),
            "has_next": Page_all_object.has_next(),
            "end_page": Paginator_all_object.num_pages,
            "Page": Page_all_object
        }
        # 渲染
        return render(req, "reservation.html", data)
    else:
        # 解析参数
        param = req.POST
        # 解析前端输入的房间号
        roomid = param.get("roomid")
        # 解析前端输入的订单号
        reservationid = param.get("reservationid")
        # 解析前端输入的证件号
        crednum = param.get("crednum")
        # 解析前端输入的客户姓名
        username = param.get("username")
        # 解析前端输入的联系号码
        phone = param.get("phone")
        # 判断前端是否输入房间号
        if roomid:
            # 查询Room表中对应房间号的数据对象，然后得到对象的id
            Reservation_roomID = Room.objects.get(RoomID=roomid).id
            # 查询Reservation表中的房间号为上面的到的id的数据对象
            Reservation_object = Reservation.objects.filter(Reservation_roomID=Reservation_roomID)
        # 判断前端是否输入订单号
        elif reservationid:
            # 查询Reservation表中对应订单号的数据对象
            Reservation_object = Reservation.objects.filter(ReservationID=reservationid)
        # 判断前端是否输入证件号
        elif crednum:
            # 查询Reservation表中对应证件号的数据对象
            Reservation_object = Reservation.objects.filter(User_cred_num=crednum)
        # 判断前端是否输入客户姓名
        elif username:
            # 查询Reservation表中对应客户姓名的数据对象
            Reservation_object = Reservation.objects.filter(User_name=username)
        # 判断前端是否输入联系号码
        elif phone:
            # 查询Reservation表中对应联系号码的数据对象
            Reservation_object = Reservation.objects.filter(User_phone=phone)
        # 否则
        else:
            # 提示没输入，查询不到
            Reservation_object = False
        if Reservation_object:
            # 创建一个分页器对象
            Paginator_object = Paginator(Reservation_object, 5)
            # 创建一个Page对象
            Page_object = Paginator_object.page(1)
            # 找出Page对象中的数据
            result = Page_object.object_list
            # 返回数据参数
        else:
            result = False
        data = {
            "result": result,
            "paginate": True
        }
        # 渲染
        return render(req, "reservation.html", data)


# 客房预约中的重新预约
# #####这个逻辑有问题还要改 没有考虑如果某个房间是直接入住的没有通过预约的
def again_reservation(req):
    # 判断请求方式为GET
    if req.method == "GET":
        page = req.GET.get("page", 1)
        # 查询Room表中没有预约和没有入住和没有停用的数据对象
        Reservation_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))
        # 创建一个分页器对象
        Paginator_object = Paginator(Reservation_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result1 = Page_object.object_list
        path = req.path
        # 返回数据参数
        data = {
            "again_reservation": True,
            "result1": result1,
            "paginate": True,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,

        }
        # 渲染
        return render(req, "reservation.html", data)
    else:
        # 解析参数
        param = req.POST
        # 解析前端输入的客户姓名
        username = param.get("username")
        # 解析前端输入的联系电话
        phone = param.get("phone")
        # 解析前端输入的证件类型
        cred_type = param.get("cred_type")
        # 解析前端输入的入住时间
        check_time = param.get("check_time")
        # 解析前端输入的房间号
        roomid = param.get("roomid")
        # 解析前端输入的客户性别
        sex = param.get("sex")
        # 解析前端输入的押金
        deposit_money = param.get("deposit_money")
        # 解析前端输入的证件号
        cred_num = param.get("cred_num")
        # 解析前端输入的入住天数
        check_days = param.get("check_days")
        # 查询Room表中对应房间号的数据对象，然后得到对象的id
        Reservation_id = Room.objects.filter(RoomID=roomid).first().id
        # 查询Reservation表中对应客户姓名的数据对象
        Not_Reservation_name = Reservation.objects.filter(User_name=username)
        # 查询Reservation表中对应证件号的数据对象
        Not_Reservation_cred_num = Reservation.objects.filter(User_cred_num=cred_num)
        # 查询Reservation表中对应联系号码的数据对象
        Not_Reservation_phone = Reservation.objects.filter(User_phone=phone)
        # 查询Reservation表中的房间号为上面的到的id的数据对象
        Not_Reservation_roomID = Reservation.objects.filter(Reservation_roomID=Reservation_id)
        # 查询Room表中没有预约和没有入住和没有停用的数据对象
        Reservation_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))
        # 创建一个分页器对象
        Paginator_object = Paginator(Reservation_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(1)
        # 找出Page对象中的数据
        result1 = Page_object.object_list
        # 遍历Reservation_object中的对象
        for i in Reservation_object:
            # 判断想预约的房间号在可以预约的房间号中
            if roomid == i.RoomID:
                # 给not_reservation赋值
                not_reservation = False
                break
            # 判断想预约的房间号不在可以预约的房间号中
            else:
                # 给not_reservation赋值
                not_reservation = True
        # 判断如果解析到的前端参数不能预约
        if Not_Reservation_name or Not_Reservation_cred_num or Not_Reservation_phone or Not_Reservation_roomID:
            # 返回数据参数
            data = {
                "Not_Reservation_name": Not_Reservation_name,
                "Not_Reservation_cred_num": Not_Reservation_cred_num,
                "Not_Reservation_phone": Not_Reservation_phone,
                "Not_Reservation_roomID": Not_Reservation_roomID,
                "again_reservation": True,
                "result1": result1,
                "not_reservation": not_reservation,
                "roomid": roomid,
                "paginate": True

            }
            # 渲染
            return render(req, "reservation.html", data)
        # 判断如果解析到的前端参数能预约
        else:
            # 生成一个现在的日期，字符串格式
            today_date = datetime.date.today().strftime("%Y%m%d")
            # 拼接字符串
            ReservationID = today_date + "0" + roomid
            # 查询Room表中对应房间号的数据对象
            Room_object = Room.objects.get(RoomID=roomid)
            # 创建一个对应前端参数的预约数据
            Reservation_message = Reservation.objects.create(ReservationID=ReservationID, User_name=username,
                                                             User_sex=sex, User_cred_type=cred_type,
                                                             User_cred_num=cred_num, User_phone=phone,
                                                             Check_time=check_time, Check_days=check_days,
                                                             Deposit_money=deposit_money,
                                                             Reservation_roomID=Room_object, Is_Check_in=0)
            # 将上面的Room_object数据的Is_Reservation改为1
            Room_object.Is_Reservation = 1
            # 保存数据
            Room_object.save()
            # 查询Room表中没有预约和没有入住和没有停用的数据对象
            Reservation_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))
            # 创建一个分页器对象
            Paginator_object = Paginator(Reservation_object, 5)
            # 创建一个Page对象
            Page_object = Paginator_object.page(1)
            # 找出Page对象中的数据
            result1 = Page_object.object_list
            # 查询出Reservation表中刚创建的数据
            Reservation_success = Reservation.objects.filter(User_cred_num=cred_num)
            # 返回数据参数
            data = {
                "success_reservation": True,
                "again_reservation": True,
                "result1": result1,
                "roomid": roomid,
                "Reservation_success": Reservation_success,
                "paginate": True

            }
            # 渲染
            return render(req, "reservation.html", data)


# 客房预约中的取消预约
def cancel_reservation(req):
    # 判断请求方式为POST
    if req.method == "POST":
        # 解析参数
        param = req.POST
        # 解析前端输入的房间号
        roomid = param.get("room_id")
        # 查询Room表中对应房间号的数据对象，然后得到对象的id
        Room_object = Room.objects.filter(RoomID=roomid).first()
        # 将上面得到的Room_object的Is_Reservation改为0
        Room_object.Is_Reservation = 0
        # 得到上面Room_object的id
        id = Room_object.id
        # 保存数据
        Room_object.save()
        # 查询Reservation表中房间号为id的数据对象
        Reservation_object = Reservation.objects.filter(Reservation_roomID=id).first()
        # 删除上面的Reservation_object
        Reservation_object.delete()
        # 返回数据参数
        data = {

            "code": 1,

        }
        # 返回Json数据
        return JsonResponse(data)


# 客房入住
def check(req):
    # 判断请求方式为GET
    if req.method == "GET":
        page = req.POST.get("page", 1)
        Reservation_object = Reservation.objects.filter(Is_Check_in=0)
        # 创建一个分页器对象
        Paginator_object = Paginator(Reservation_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        # 赋值
        Booked = True
        # 返回数据参数
        path = req.path
        data = {
            "Booked": Booked,
            "result": result,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object
        }
        # 渲染
        return render(req, "checkin.html", data)
    else:
        # 解析参数
        param = req.POST
        # 解析前端输入的房间号
        roomid = param.get("roomid")
        # 解析前端输入的订单号
        checkid = param.get("checkid")
        # 解析前端输入的证件号
        crednum = param.get("crednum")
        # 解析前端输入的客户姓名
        username = param.get("username")
        # 解析前端输入的联系号码
        phone = param.get("phone")
        # 如果前端房间号不为空
        if roomid:
            # 查询Room表中对应房间号的数据对象，然后得到对象的id
            Reservation_roomID = Room.objects.get(RoomID=roomid).id
            # 查询Reservation表中对应的房间号和没有入住的数据对象
            Reservation_object = Reservation.objects.filter(Q(Reservation_roomID=Reservation_roomID) & Q(Is_Check_in=0))
        # 如果前端订单号不为空
        elif checkid:
            # 查询Reservation表中对应的订单号和没有入住的数据对象
            Reservation_object = Reservation.objects.filter(Q(ReservationID=checkid) & Q(Is_Check_in=0))
        # 如果前端证件号不为空
        elif crednum:
            # 查询Reservation表中对应的证件号和没有入住的数据对象
            Reservation_object = Reservation.objects.filter(Q(User_cred_num=crednum) & Q(Is_Check_in=0))
        # 如果前端客户姓名不为空
        elif username:
            # 查询Reservation表中对应的客户姓名和没有入住的数据对象
            Reservation_object = Reservation.objects.filter(Q(User_name=username) & Q(Is_Check_in=0))
        # 如果前端联系号码不为空
        elif phone:
            # 查询Reservation表中对应的联系号码和没有入住的数据对象
            Reservation_object = Reservation.objects.filter(Q(User_phone=phone) & Q(Is_Check_in=0))
        # 如果前端什么也没有输入
        else:
            # 查询Reservation表中没有入住的数据对象
            Reservation_object = []
        page = req.POST.get("page", 1)
        # 创建一个分页器对象
        Paginator_object = Paginator(Reservation_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        # 赋值
        Booked = True
        # 返回数据参数
        path = req.path
        data = {
            "Booked": Booked,
            "result": result,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,
            "paginate": True
        }
        # 渲染
        return render(req, "checkin.html", data)


# 客房入住中的办理入住
def reservation_to_check(req):
    # 判断请求方式为POST
    if req.method == "POST":
        # 解析参数
        param = req.POST
        # 解析ajax中的room_id参数
        roomid = param.get("room_id")
        # 查询Room表中对应房间号的数据对象
        Room_object = Room.objects.filter(RoomID=roomid).first()
        # 将上面的Room_object中Is_Reservation改为0
        Room_object.Is_Reservation = 0
        # 将上面的Room_object中Is_Check_in改为1
        Room_object.Is_Check_in = 1
        # 得到上面的Room_object中id
        id = Room_object.id
        # 保存数据
        Room_object.save()
        # 查询Reservation表中对应房间号的数据对象
        Reservation_object = Reservation.objects.filter(Reservation_roomID=id).first()
        # 得到上面的Reservation_object中的客户姓名
        check_name = Reservation_object.User_name
        # 得到上面的Reservation_object中的客户性别
        check_sex = Reservation_object.User_sex
        # 得到上面的Reservation_object中的证件类型
        check_cred_type = Reservation_object.User_cred_type
        # 得到上面的Reservation_object中的证件号
        check_cred_num = Reservation_object.User_cred_num
        # 得到上面的Reservation_object中的联系号码
        check_phone = Reservation_object.User_phone
        # 得到上面的Reservation_object中的入住时间
        check_check_time = Reservation_object.Check_time
        # 得到上面的Reservation_object中的入住天数
        check_check_days = Reservation_object.Check_days
        # 得到上面的Reservation_object中的押金
        check_deposit_money = Reservation_object.Deposit_money
        # 将上面的Reservation_object中Is_Check_in改为1
        Reservation_object.Is_Check_in = 1
        # 保存数据
        Reservation_object.save()
        # 生成现在的日期，返回字符串格式
        today_date = datetime.date.today().strftime("%Y%m%d")
        # 拼接字符串
        CheckID = "C" + today_date + "0" + roomid
        # 查询Room表中对应房间号的数据对象
        Room_object = Room.objects.get(RoomID=roomid)
        # 创建一条入住的数据
        CheckIn_message = CheckIn.objects.create(CheckID=CheckID, User_name=check_name, User_sex=check_sex,
                                                 User_cred_type=check_cred_type, User_cred_num=check_cred_num,
                                                 User_phone=check_phone, Check_time=check_check_time,
                                                 Check_days=check_check_days, Check_roomID=Room_object,
                                                 Deposit_money=check_deposit_money)
        if check_sex == 1:
            check_sex_str = "男"
        else:
            check_sex_str = "女"
        # 返回数据参数
        data = {

            "code": 1,
            "CheckID": CheckID,
            "User_name": check_name,
            "User_sex": check_sex_str,
            "User_cred_type": check_cred_type,
            "User_cred_num": check_cred_num,
            "User_phone": check_phone,
            "Check_roomID": roomid,
            "Check_time": check_check_time,
            "Check_days": check_check_days,
            "Deposit_money": check_deposit_money

        }
        # 返回Json数据
        return JsonResponse(data)


# 客房入住中没有预约直接办理入住
# ########还有点问题，没有没有考虑这个房间号根本就不存在的问题，可以把房间号的前端输入，改成select>option
def new_checkin(req):
    if req.method == "GET":
        page = req.GET.get("page", 1)
        path = req.path
        Cherk_all_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))
        # 创建一个分页器对象
        Paginator_object = Paginator(Cherk_all_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        data = {
            "Cherk_object": result,
            "new_checkin": True,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,
        }
        return render(req, "checkin.html", data)
    else:
        param = req.POST
        name = param.get("username")
        phone = param.get("phone")
        cred_type = param.get("cred_type")
        check_time = param.get("check_time")
        roomid = param.get("roomid")
        sex = param.get("sex")
        deposit_money = param.get("deposit_money")
        cred_num = param.get("cred_num")
        check_days = param.get("check_days")
        Name_in_reservation = Reservation.objects.filter(User_name=name)
        Name_in_cherk = CheckIn.objects.filter(User_name=name)
        Phone_in_reservation = Reservation.objects.filter(User_phone=phone)
        Phone_in_check = CheckIn.objects.filter(User_phone=phone)
        room_object = Room.objects.filter(RoomID=roomid).first()
        Roomid_in_reservation = Reservation.objects.filter(Reservation_roomID=room_object)
        Roomid_in_check = CheckIn.objects.filter(Check_roomID=room_object)
        Cred_num_in_reservation = Reservation.objects.filter(User_cred_num=cred_num)
        Cred_num_in_check = CheckIn.objects.filter(User_cred_num=cred_num)

        Cherk_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False) & Q(Is_Stop=False))

        if Name_in_reservation or Name_in_cherk or Phone_in_reservation or Phone_in_check or Roomid_in_reservation or Roomid_in_check or Cred_num_in_reservation or Cred_num_in_check:
            data = {
                "Name_in_reservation": Name_in_reservation,
                "Name_in_cherk": Name_in_cherk,
                "Phone_in_reservation": Phone_in_reservation,
                "Phone_in_check": Phone_in_check,
                "Roomid_in_reservation": Roomid_in_reservation,
                "Roomid_in_check": Roomid_in_check,
                "Cred_num_in_reservation": Cred_num_in_reservation,
                "Cred_num_in_check": Cred_num_in_check,
                "Cherk_object": Cherk_object,
                "new_checkin": True
            }
            return render(req, "checkin.html", data)
        else:
            room_object.Is_Check_in = 1
            room_object.save()
            # 生成现在的日期，返回字符串格式
            today_date = datetime.date.today().strftime("%Y%m%d")
            # 拼接字符串
            CheckID = "C" + today_date + "0" + roomid
            Check_object = CheckIn.objects.create(CheckID=CheckID, User_name=name, User_sex=sex,
                                                  User_cred_type=cred_type, User_cred_num=cred_num, User_phone=phone,
                                                  Check_time=check_time, Check_days=check_days,
                                                  Check_roomID=room_object, Deposit_money=deposit_money)
            Check_success = CheckIn.objects.filter(User_cred_num=cred_num)
            data = {
                "Check_success": Check_success,
                "Cherk_object": Cherk_object,
                "new_checkin": True
            }
            return render(req, "checkin.html", data)


# 客房更改
def room_change(req):
    if req.method == "GET":
        page = req.GET.get("page", 1)
        Check_query_object = CheckIn.objects.all()
        # 创建一个分页器对象
        Paginator_object = Paginator(Check_query_object, 4)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        replace_room_object = Room.objects.filter(Q(Is_Check_in=False) & Q(Is_Stop=False) & Q(Is_Reservation=False))
        path = req.path
        data = {
            "Check_object": result,
            "replace_room_object": replace_room_object,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,
        }
        return render(req, "room_change.html", data)
    else:
        param = req.POST
        roomid = param.get("roomid")
        checkid = param.get("checkid")
        crednum = param.get("crednum")
        username = param.get("username")
        phone = param.get("phone")
        try:
            Check_roomID = Room.objects.filter(RoomID=roomid).first().id
        except ValueError:
            Check_roomID = ""
        CheckID = CheckIn.objects.filter(CheckID=checkid)
        User_cred_num = CheckIn.objects.filter(User_cred_num=crednum)
        User_name = CheckIn.objects.filter(User_name=username)
        User_phone = CheckIn.objects.filter(User_phone=phone)
        if Check_roomID:
            Check_query_object = CheckIn.objects.filter(Check_roomID=Check_roomID)
        elif CheckID:
            Check_query_object = CheckID
        elif User_cred_num:
            Check_query_object = User_cred_num
        elif User_name:
            Check_query_object = User_name
        elif User_phone:
            Check_query_object = User_phone
        else:
            Check_query_object = []
        Paginator_object = Paginator(Check_query_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(1)
        # 找出Page对象中的数据
        result = Page_object.object_list
        replace_room_object = Room.objects.filter(Q(Is_Check_in=False) & Q(Is_Stop=False) & Q(Is_Reservation=False))
        # print(replace_room_object)
        data = {
            "Check_object": result,
            "replace_room_object": replace_room_object,
            "paginate": True

        }
        return render(req, "room_change.html", data)


# 客房更改中的续住和调房
def continue_check(req):
    if req.method == "GET":
        param = req.GET
        # 现有天数
        ava_days = param.get("ava_days")
        # 总押金
        ava_money = param.get("ava_money")
        # 原房间号
        ori_room = param.get("ori_room")
        Room_id = Room.objects.filter(RoomID=ori_room).first().id
        Check_object = CheckIn.objects.filter(Check_roomID=Room_id).first()
        Check_object.Check_days = ava_days
        Check_object.Deposit_money = ava_money
        Check_object.save()
        Check_object = CheckIn.objects.filter(Check_roomID=Room_id).first()

        CheckID = Check_object.CheckID
        User_name = Check_object.User_name
        if Check_object.User_sex == 1:
            User_sex = "男"
        else:
            User_sex = "女"
        User_cred_type = Check_object.User_cred_type
        User_cred_num = Check_object.User_cred_num
        User_phone = Check_object.User_phone
        Check_time_str = Check_object.Check_time.strftime("%Y%m%d")
        Check_time = Check_time_str[0:4] + "年" + (Check_time_str[4] if Check_time_str[4] != "0" else "") + \
                     Check_time_str[5] + "月" + (Check_time_str[6] if Check_time_str[6] != "0" else "") + Check_time_str[
                         7] + "日"
        print(Check_time)
        Check_days = Check_object.Check_days
        Check_roomID = Check_object.Check_roomID.RoomID
        Deposit_money = Check_object.Deposit_money
        data = {
            "code": 1,
            "CheckID": CheckID,
            "User_name": User_name,
            "User_sex": User_sex,
            "User_cred_type": User_cred_type,
            "User_cred_num": User_cred_num,
            "User_phone": User_phone,
            "Check_time": Check_time,
            "Check_days": Check_days,
            "Check_roomID": Check_roomID,
            "Deposit_money": Deposit_money,

        }
        return JsonResponse(data)
    else:
        param = req.POST
        # 现房间号
        now_room = param.get("now_room")
        # 总押金
        ava_money2 = param.get("ava_money2")
        # 原房间号
        ori_room = param.get("ori_room")
        room = Room.objects.filter(RoomID=ori_room).first()
        room.Is_Check_in = 0
        room_id = room.id
        room.save()
        Check_object = CheckIn.objects.filter(Check_roomID=room_id).first()
        room_object = Room.objects.filter(RoomID=now_room).first()
        room_object.Is_Check_in = 1
        room_object.save()
        Check_object.CheckID = Check_object.CheckID + "#" + now_room
        Check_object.Check_roomID = room_object
        Check_object.Deposit_money = ava_money2
        Check_object.save()
        room_id2 = Room.objects.filter(RoomID=now_room).first().id
        Check_object = CheckIn.objects.filter(Check_roomID=room_id2).first()

        CheckID = Check_object.CheckID
        User_name = Check_object.User_name
        if Check_object.User_sex == 1:
            User_sex = "男"
        else:
            User_sex = "女"
        User_cred_type = Check_object.User_cred_type
        User_cred_num = Check_object.User_cred_num
        User_phone = Check_object.User_phone
        Check_time_str = Check_object.Check_time.strftime("%Y%m%d")
        Check_time = Check_time_str[0:4] + "年" + (Check_time_str[4] if Check_time_str[4] != "0" else "") + \
                     Check_time_str[5] + "月" + (Check_time_str[6] if Check_time_str[6] != "0" else "") + Check_time_str[
                         7] + "日"
        print(Check_time)
        Check_days = Check_object.Check_days
        Check_roomID = Check_object.Check_roomID.RoomID
        Deposit_money = Check_object.Deposit_money
        data = {
            "code": 1,
            "CheckID": CheckID,
            "User_name": User_name,
            "User_sex": User_sex,
            "User_cred_type": User_cred_type,
            "User_cred_num": User_cred_num,
            "User_phone": User_phone,
            "Check_time": Check_time,
            "Check_days": Check_days,
            "Check_roomID": Check_roomID,
            "Deposit_money": Deposit_money,

        }
        return JsonResponse(data)


def room_settlement(req):
    if req.method == "GET":
        page = req.GET.get("page", 1)
        path = req.path
        Check_query_object = CheckIn.objects.all()
        # 创建一个分页器对象
        Paginator_object = Paginator(Check_query_object, 4)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        # replace_room_object = Room.objects.filter(Q(Is_Check_in=False) & Q(Is_Stop=False) & Q(Is_Reservation=False))
        data = {
            "Check_object": result,
            # "replace_room_object": replace_room_object,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,
        }
        return render(req, "room_settlement.html", data)
    else:
        param = req.POST
        roomid = param.get("roomid")
        checkid = param.get("checkid")
        crednum = param.get("crednum")
        username = param.get("username")
        phone = param.get("phone")
        try:
            Check_roomID = Room.objects.filter(RoomID=roomid).first().id
        except ValueError:
            Check_roomID = ""
        CheckID = CheckIn.objects.filter(CheckID=checkid)
        User_cred_num = CheckIn.objects.filter(User_cred_num=crednum)
        User_name = CheckIn.objects.filter(User_name=username)
        User_phone = CheckIn.objects.filter(User_phone=phone)
        if Check_roomID:
            Check_query_object = CheckIn.objects.filter(Check_roomID=Check_roomID)
        elif CheckID:
            Check_query_object = CheckID
        elif User_cred_num:
            Check_query_object = User_cred_num
        elif User_name:
            Check_query_object = User_name
        elif User_phone:
            Check_query_object = User_phone
        else:
            Check_query_object = CheckIn.objects.all()
        Paginator_object = Paginator(Check_query_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(1)
        # 找出Page对象中的数据
        result = Page_object.object_list
        replace_room_object = Room.objects.filter(Q(Is_Check_in=False) & Q(Is_Stop=False) & Q(Is_Reservation=False))
        # 单价
        room_price = Room.objects.filter(RoomID=roomid).first().RoomPrice
        data = {
            "Check_object": result,
            "replace_room_object": replace_room_object,
            "room_price": room_price,
            "paginate": True
        }
        return render(req, "room_settlement.html", data)


# 客房结算中的住宿费和其他费用
def stay_other(req):
    if req.method == "GET":
        param = req.GET
        discount = param.get("discount")
        paid = param.get("paid")
        unit_price = param.get("unit_price")
        stay_days = param.get("stay_days")
        discount_float = float(discount)
        paid_float = float(paid)
        unit_price_float = float(unit_price)
        stay_days_float = float(stay_days)
        stay_money = round(unit_price_float * stay_days_float * discount_float - paid_float, 2)
        data = {
            "code": 1,
            "stay_money": stay_money
        }
        return JsonResponse(data)
    else:
        param = req.POST
        other_price = param.get("other_price")
        deposit_money = param.get("deposit_money")
        other_price_float = float(other_price)
        deposit_money_float = float(deposit_money)
        other_money = round(other_price_float - deposit_money_float, 2)
        data = {
            "code": 1,
            "other_money": other_money,
        }
        return JsonResponse(data)


# 客房结算中的总合计和结算
def all_total_balance_accounts(req):
    if req.method == "GET":
        param = req.GET
        hotel_expense_total = param.get("hotel_expense_total")
        other_expense_total = param.get("other_expense_total")
        hotel_expense_total_float = float(hotel_expense_total)
        other_expense_total = float(other_expense_total)
        all_money = round(hotel_expense_total_float + other_expense_total, 2)
        data = {
            "code": 1,
            "all_money": all_money,

        }
        return JsonResponse(data)
    else:
        param = req.POST
        accounts_roomID = param.get("accounts_roomID")
        all_money = param.get("all_money")
        if all_money:
            Room_object = Room.objects.filter(RoomID=accounts_roomID).first()
            Room_object_id = Room_object.id
            Room_object.Is_Check_in = 0
            Room_object.save()
            Check_object = CheckIn.objects.filter(Check_roomID=Room_object_id).first()
            Check_object.delete()
            data = {
                "code": 1,
            }
        else:
            data = {
                "code": 2,
            }
        return JsonResponse(data)


# 客房类型 和客房类型中的新增
def room_type(req):
    if req.method == "GET":
        add = True
        data = {
            "add": add
        }
        return render(req, "room_type.html", data)
    else:
        param = req.POST
        RoomID = param.get("RoomID")
        RoomType = param.get("RoomType")
        RoomPrice = param.get("RoomPrice")
        RoomArea = param.get("RoomArea")
        RoomBed = param.get("RoomBed")
        RoomWifi = 1 if param.get("RoomWifi") == "有" else 0
        RoomRemarks = param.get("RoomRemarks")
        room_object = Room.objects.create(RoomID=RoomID, RoomType=RoomType, RoomPrice=RoomPrice, RoomArea=RoomArea,
                                          RoomBed=RoomBed, RoomWifi=RoomWifi, RoomRemarks=RoomRemarks)
        room_object = Room.objects.filter(RoomID=RoomID)
        add = True
        data = {
            "room_object": room_object,
            "add": add
        }
        return render(req, "room_type.html", data)


def room_modify(req):
    if req.method == "GET":
        room_all_object = Room.objects.all()
        modify = True
        data = {
            "room_all_object": room_all_object,
            "modify": modify
        }
        return render(req, "room_type.html", data)
    else:
        param = req.POST
        RoomID = param.get("RoomID2")
        RoomType = param.get("RoomType2")
        RoomPrice = param.get("RoomPrice2")
        RoomArea = param.get("RoomArea2")
        RoomBed = param.get("RoomBed2")
        RoomWifi = 1 if param.get("RoomWifi2") == "有" else 0
        RoomRemarks = param.get("RoomRemarks2")
        room_object = Room.objects.get(RoomID=RoomID)
        room_object.RoomType = RoomType
        room_object.RoomPrice = RoomPrice
        room_object.RoomArea = RoomArea
        room_object.RoomBed = RoomBed
        room_object.RoomWifi = RoomWifi
        room_object.RoomRemarks = RoomRemarks
        room_object.save()
        room_object = Room.objects.filter(RoomID=RoomID)
        modify = True
        data = {
            "room_object": room_object,
            "modify": modify
        }
        return render(req, "room_type.html", data)


def ajax(req):
    if req.method == "POST":
        param = req.POST
        RoomID = param.get("RoomID")
        room_object = Room.objects.filter(RoomID=RoomID).first()
        RoomType = room_object.RoomType
        RoomPrice = room_object.RoomPrice
        RoomArea = room_object.RoomArea
        RoomBed = room_object.RoomBed
        RoomWifi = "有" if room_object.RoomWifi == 1 else "无"
        RoomRemarks = room_object.RoomRemarks
        data = {
            "code": 1,
            "RoomType": RoomType,
            "RoomPrice": RoomPrice,
            "RoomArea": RoomArea,
            "RoomBed": RoomBed,
            "RoomWifi": RoomWifi,
            "RoomRemarks": RoomRemarks,
        }
        return JsonResponse(data)


def room_delete(req):
    if req.method == "GET":
        room_all_object = Room.objects.filter(Q(Is_Reservation=False) & Q(Is_Check_in=False))
        delete = True
        data = {
            "room_all_object": room_all_object,
            "delete": delete
        }
        return render(req, "room_type.html", data)
    else:
        param = req.POST
        RoomID = param.get("RoomID3")
        room_object = Room.objects.get(RoomID=RoomID)
        room_object.delete()
        delete_room = True
        delete = True
        data = {
            "delete_room": delete_room,
            "delete": delete,
            "RoomID": RoomID
        }
        return render(req, "room_type.html", data)


def room_status(req):
    if req.method == "GET":
        page = req.GET.get("page", 1)
        path = req.path
        room_object = Room.objects.all()
        Paginator_object = Paginator(room_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(page)
        # 找出Page对象中的数据
        result = Page_object.object_list
        data = {
            "result": result,
            "path": path,
            "page_range": Paginator_object.page_range,
            "has_prev": Page_object.has_previous(),
            "has_next": Page_object.has_next(),
            "end_page": Paginator_object.num_pages,
            "Page": Page_object,
        }
        return render(req, "room_status.html", data)
    else:
        param = req.POST
        room_id = param.get("roomid")
        room_object = Room.objects.filter(RoomID=room_id)
        Paginator_object = Paginator(room_object, 5)
        # 创建一个Page对象
        Page_object = Paginator_object.page(1)
        # 找出Page对象中的数据
        result = Page_object.object_list
        data = {
            "result": result
        }
        return render(req, "room_status.html", data)


def status_ajax(req):
    if req.method == "POST":
        param = req.POST
        room_id = param.get("room_id")
        now_status = param.get("now_status")
        room_object = Room.objects.filter(RoomID=room_id).first()
        if now_status == "已预约":
            room_object.Is_Reservation = 1
            room_object.Is_Check_in = 0
            room_object.Is_Stop = 0
        elif now_status == "已入住":
            room_object.Is_Reservation = 0
            room_object.Is_Check_in = 1
            room_object.Is_Stop = 0
        elif now_status == "已停用":
            room_object.Is_Reservation = 0
            room_object.Is_Check_in = 0
            room_object.Is_Stop = 1
        else:
            room_object.Is_Reservation = 0
            room_object.Is_Check_in = 0
            room_object.Is_Stop = 0
        room_object.save()
        data = {
            "code": 1
        }
        return JsonResponse(data)
