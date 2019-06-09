$("#hotel_expense_btn").click(function () {
    var discount = $("#discount").val();
    var paid = $("#paid").val();
    var unit_price = $("#unit_price").text();
    var stay_days = $("#stay_days").text();
    $.ajax({
        url: "/hotel/stay_other",
        data: {
            "discount": discount,
            "paid": paid,
            "unit_price": unit_price,
            "stay_days": stay_days
        },
        method: "get",
        success: function (res) {
            if (res.code == 1) {
                $("#hotel_expense_total").text(res.stay_money);
                $("#hotel_expense_btn").text("已合计");

            }
            ;
        }

    });
});

$("#other_expense_btn").click(function () {
    var other_price = $("#other_price").val();
    var deposit_money = $("#deposit_money").text();
    $.ajax({
        url: "/hotel/stay_other",
        data: {
            "other_price": other_price,
            "deposit_money": deposit_money,
        },
        method: "post",
        success: function (res) {
            if (res.code == 1) {
                $("#other_expense_total").text(res.other_money);
                $("#other_expense_btn").text("已合计");
            }
            ;
        },
    });

});

$("#all_total").click(function () {
    var hotel_expense_total = $("#hotel_expense_total").text();
    var other_expense_total = $("#other_expense_total").text();
    $.ajax({
        url: "/hotel/all_total_balance_accounts",
        data: {
            "hotel_expense_total": hotel_expense_total,
            "other_expense_total": other_expense_total,
        },
        method: "get",
        success: function (res) {
            if (res.code == 1) {
                $("#all_money").val(res.all_money);
                $("#all_total").text("已合计");
            }
            ;


        },
    });

});

$("#balance_accounts").click(function () {
    var accounts_roomID = $("#balance_accounts").attr("accounts_roomID");
    var all_money=$("#all_money").val();
    $.ajax({
        url: "/hotel/all_total_balance_accounts",
        data: {
            "accounts_roomID": accounts_roomID,
            "all_money":all_money
        },
        method: "post",
        success: function (res) {
            if (res.code == 1) {
                $("#balance_accounts").text("已退房");
            }else {
                alert("对不起，没有结算！！！");
            }
        },
    });
});