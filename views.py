from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import *
from .models import *
from .my_utils import *
from .tasks import send_verify_mail

# Create your views here.
cache = caches['confirm']


def home(req):
    wheels = Wheel.objects.all()
    menus = Nav.objects.all()
    mustbuy = MustBuy.objects.all()
    shops = Shop.objects.all()
    mainshows = MainShow.objects.all()
    result = {
        "title": "首页",
        "wheels": wheels,
        "menus": menus,
        "mustbuy": mustbuy,
        "shop0": shops[0],
        "shop1_3": shops[1:3],
        "shop3_7": shops[3:7],
        "shop_last": shops[7:],
        "mainshows": mainshows
    }

    return render(req, 'home/home.html', result)


def market(req):
    return redirect(reverse("axf:market_params", args=("104749", "0", 0)))


def market_with_params(req, type_id, sub_type_id, order_type):
    # 获取所有的一级分类
    types = FoodTypes.objects.all()

    current_cate = types.filter(typeid=type_id)[0]
    childtypenames = current_cate.childtypenames.split("#")
    # sub_types=[]
    # for i in childtypenames:
    #     tmp=i.split(":")
    #     sub_types.append(tmp)
    sub_types = [i.split(":") for i in childtypenames]
    # print(sub_types)

    # 根据typeid 搜索商品信息
    goods = Goods.objects.filter(
        categoryid=int(type_id)
    )
    if sub_type_id == "0":
        pass
    else:
        goods = goods.filter(childcid=int(sub_type_id))

    NO_SORT = 0
    PRICE_SORT = 1
    SALES_SORT = 2
    if int(order_type) == 0:
        pass
    elif int(order_type) == 1:
        goods = goods.order_by("price")
    else:
        goods = goods.order_by("productnum")

    user = req.user
    if isinstance(user, MyUser):
        tmp_dict = {}
        cart_nums = Cart.objects.filter(user=user)
        print(cart_nums)

        for i in cart_nums:
            # print(i.goods)
            tmp_dict[i.goods_id] = i.num
            print(tmp_dict)
        for i in goods:
            i.num = tmp_dict.get(i.id) if tmp_dict.get(i.id) else 0

    result = {
        "title": "闪购",
        "types": types,
        "goods": goods,
        "current_type_id": type_id,
        "sub_types": sub_types,
        "current_sub_type_id": sub_type_id,
        "order_type": int(order_type)
    }
    return render(req, "market/market.html", result)


@login_required(login_url="/axf/login")
def cart(req):
    user = req.user
    data = Cart.objects.filter(user_id=user.id)
    sum_money = get_cart_money(data)

    if data.exists() and not data.filter(is_selected=False).exists():
        is_all_select = True
    else:
        is_all_select = False
    result = {
        "title": "购物车",
        "uname": user.username,
        "phone": user.phone if user.phone else "暂无",
        "address": user.address if user.address else "暂无",
        "cart_items": data,
        "sum_money": sum_money,
        "is_all_select": is_all_select,
    }
    return render(req, "cart/cart.html", result)


# @login_required(login_url="/axf/login")
def mine(req):
    btns = MineBtns.objects.filter(is_used=True)
    user = req.user
    is_login = True
    if isinstance(user, AnonymousUser):
        # print("zhixing")
        is_login = False
    u_name = user.username if is_login else ""
    icon = "http://" + req.get_host() + "/static/uploads/" + user.icon.url if is_login else ""
    # print(icon)
    # print(user)
    result = {
        "title": "我的",
        "btns": btns,
        "is_login": is_login,
        "u_name": u_name,
        "icon": icon

    }
    return render(req, "mine/mine.html", result)


class RegisterAPI(View):

    def get(self, req):
        return render(req, "user/register.html")

    def post(self, req):
        params = req.POST

        icon = req.FILES.get("u_icon")

        name = params.get("u_name")

        pwd = params.get("u_pwd")

        confirm_pwd = params.get("u_confirm_pwd")

        email = params.get("email")

        if pwd and confirm_pwd and pwd == confirm_pwd:
            # 判断用户名是否可以
            if MyUser.objects.filter(username=name).exists():
                return render(req, "user/register.html", {"help_msg": "该用户已存在"})
            else:
                user = MyUser.objects.create_user(
                    username=name,
                    is_active=False,
                    email=email,
                    password=pwd,
                    icon=icon
                )
                # 生成验证连接
                # 发送邮件
                # 设置缓存
                # 返回登录页面
                url = "http://" + req.get_host() + "/axf/confirm/" + get_uuique_str()
                send_verify_mail.delay(url, user.id, email)
                return render(req, "user/login.html")


class LoginAPI(View):
    def get(self, req):
        return render(req, "user/login.html")

    def post(self, req):
        # 解析参数

        # 校验数据
        # 使用用户名、密码校验用户
        # 如果可以就登陆
        # 不可以就返回提示
        params = req.POST
        name = params.get("name")
        pwd = params.get("pwd")

        if not name or not pwd:
            data = {
                "code": 2,
                "msg": "账号或密码不能为空",
                "data": ""
            }
            return JsonResponse(data)

        user = authenticate(username=name, password=pwd)

        if user:
            login(req, user)
            data = {
                "code": 1,
                "msg": "ok",
                "data": "/axf/mine"
            }
            return JsonResponse(data)
        else:
            data = {
                "code": 3,
                "msg": "密码错误",
                "data": ""
            }
            return JsonResponse(data)


class LogoutAPI(View):
    def get(self, req):
        logout(req)
        return redirect(reverse("axf:mine"))


def confirm(req, uuid_str):
    # 去缓存
    # 修改is_active
    user_id = cache.get(uuid_str)

    if user_id:
        user = MyUser.objects.get(pk=int(user_id))
        user.is_active = True
        user.save()
        return redirect(reverse("axf:login"))
    else:
        return HttpResponse("<h2>失效</h2>")


def check_uname(req):
    uname = req.GET.get("uname")
    data = {
        "code": 1,
        "data": ""

    }
    if uname and len(uname) >= 3:
        if MyUser.objects.filter(username=uname).exists():
            data["msg"] = "账号已存在"
        else:
            data["msg"] = "账号可用"

    else:
        data["msg"] = "用户名过短"

    return JsonResponse(data)


class CartAPI(View):
    def post(self, req):
        user = req.user
        if not isinstance(user, MyUser):
            data = {
                "code": 2,
                "msg": "not login",
                "data": "/axf/login"
            }

            return JsonResponse(data)

        op_type = req.POST.get("type")
        g_id = int(req.POST.get("g_id"))

        goods = Goods.objects.get(pk=g_id)

        if op_type == "add":

            goods_num = 1

            if goods.storenums > 1:
                cart_goods = Cart.objects.filter(
                    user=user,
                    goods=goods
                )
                print(cart_goods)
                if cart_goods.exists():
                    cart_item = cart_goods.first()
                    # print(cart_item)
                    # print(cart_item.num)
                    cart_item.num = cart_item.num + 1
                    cart_item.save()
                    goods_num = cart_item.num
                else:
                    Cart.objects.create(user=user, goods=goods)
                data = {

                    "code": 1,
                    "msg": "ok",
                    "data": goods_num

                }
                return JsonResponse(data)
            else:
                data = {
                    "code": 3,
                    "msg": "库存不足",
                    "data": ""
                }
            return JsonResponse(data)

        elif op_type == "sub":
            goods_num = 0
            cart_item = Cart.objects.get(
                user=user,
                goods=goods
            )
            print(cart_item)
            cart_item.num = cart_item.num - 1
            cart_item.save()

            if cart_item.num == 0:
                cart_item.delete()

            else:
                goods_num = cart_item.num

            data = {
                "code": 1,
                "msg": "ok",
                "data": goods_num
            }
            return JsonResponse(data)


class CartStatusAPI(View):
    def patch(self, req):
        params = QueryDict(req.body)
        # print(params)
        c_id = int(params.get("c_id"))
        user = req.user

        cart_items = Cart.objects.filter(user_id=user.id)
        # print(cart_items)
        cart_data = cart_items.get(id=c_id)
        # print(cart_items.filter(is_selected=True))

        cart_data.is_selected = not cart_data.is_selected
        cart_data.save()

        sum_money = get_cart_money(cart_items)

        if cart_items.filter(is_selected=False).exists():
            is_all_select = False
        else:
            is_all_select = True

        result = {
            "code": 1,
            "msg": "ok",
            "data": {
                "is_select_all": is_all_select,
                "sum_money": sum_money,
                "status": cart_data.is_selected
            }
        }
        return JsonResponse(result)


class CartAllAtatusAPI(View):
    def put(self, req):
        user = req.user

        cart_items = Cart.objects.filter(user_id=user.id)
        is_select_all = False
        if cart_items.exists() and cart_items.filter(is_selected=False).exists():
            is_select_all = True
            # for i in cart_items.filter(is_selected=False):
            #     i.is_selected = True
            #     i.save()
            cart_items.filter(is_selected=False).update(is_selected=True)
            sum_money = get_cart_money(cart_items)
        else:
            cart_items.update(is_selected=False)
            sum_money = 0
        result = {
            "code": 1,
            "msg": "ok",
            "data": {
                "sum_money": sum_money,
                "all_select": is_select_all
            }
        }
        return JsonResponse(result)


class CartItemAPI(View):
    def post(self, req):
        user = req.user
        c_id = req.POST.get("c_id")
        print(c_id)

        cart_item = Cart.objects.get(id=int(c_id))

        if cart_item.goods.storenums < 1:
            data = {
                "code": 2,
                "msg": "库存不足",
                "data": "",

            }
            return JsonResponse(data)

        cart_item.num += 1
        cart_item.save()
        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )
        sum_money = get_cart_money(cart_items)

        data = {
            "code": 1,
            "msg": "ok",
            "data": {
                "num": cart_item.num,
                "sum_money": sum_money
            }
        }
        return JsonResponse(data)

    def delete(self, req):
        user = req.user

        c_id = QueryDict(req.body).get("c_id")

        cart_item = Cart.objects.get(pk=int(c_id))

        cart_item.num -= 1
        cart_item.save()

        if cart_item.num == 0:
            goods_num = 0
            cart_item.delete()
        else:
            goods_num = cart_item.num

        cart_items = Cart.objects.filter(
            user=user,
            is_selected=True
        )
        sum_money = get_cart_money(cart_items)

        data = {
            "code": 1,
            "msg": "ok",
            "data": {
                "num": goods_num,
                "sum_money": sum_money
            }

        }
        return JsonResponse(data)


class OrderAPI(View):
    def get(self, req):
        user = req.user
        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )
        if not cart_items.exists():
            return render(req, "order/order_detail.html")

        order = Order.objects.create(
            user=user
        )
        for i in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=i.goods,
                num=i.num,
                buy_money=i.goods.price,
            )
        sum_money = get_cart_money(cart_items)
        cart_items.delete()
        data = {
            'sum_money': sum_money,
            "order": order
        }

        return render(req, "order/order_detail.html", data)
