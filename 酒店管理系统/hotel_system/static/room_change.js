$("#add_days").change(function () {
    var ori_days = $("#ori_days").attr("value");
    // console.log(ori_days);
    var add_days = $("#add_days").val();
    // console.log(add_days)
    if (add_days != "") {
        var ava_days = parseInt(ori_days) + parseInt(add_days);
        $("#ava_days").val(ava_days);
    }

});
$("#add_money").change(function () {
    var ori_money = $("#ori_money").attr("value");
    // console.log(ori_money);
    var add_money = $("#add_money").val();
    // console.log(add_money)
    if (add_money != "") {
        var ava_money = parseFloat(ori_money) + parseFloat(add_money);
        $("#ava_money").val(ava_money);
    }

});

$("#cha_room").change(function () {
    var cha_room = $("#cha_room").val();
    // console.log(add_money2)
    if (cha_room != "") {
        $("#now_room").val(cha_room);
    }

});

$("#add_money2").change(function () {
    var ori_money2 = $("#ori_money2").attr("value");
    // console.log(ori_money2);
    var add_money2 = $("#add_money2").val();
    // console.log(add_money2)
    if (add_money2 != "") {
        var ava_money2 = parseFloat(ori_money2) + parseFloat(add_money2);
        $("#ava_money2").val(ava_money2);
    }

});

$("#continue_room").click(function () {
    var ava_days = $("#ava_days").val();
    var ava_money = $("#ava_money").val();
    var ori_room = $("#ori_room").val();
    $.ajax({
        url: "/hotel/continue_check",
        data: {
            "ava_days": ava_days,
            "ava_money": ava_money,
            "ori_room": ori_room
        },
        method: "get",
        success: function (res) {
            if (res.code == 1) {
                // console.log("ada");
                $("tr").eq(1).after("<tr>\n" +
                        "<td class=\"active\">"+res.CheckID+"</td>\n" +
                        "<td class=\"active\">"+res.User_name+"</td>\n" +
                        "<td class=\"active\">"+res.User_sex+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_type+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_num+"</td>\n" +
                        "<td class=\"active\">"+res.User_phone+"</td>\n" +
                        "<td class=\"active\">"+res.Check_roomID+"</td>\n" +
                        "<td class=\"active\">"+res.Check_time+"</td>\n" +
                        "<td class=\"active\" style='color: red'>"+res.Check_days+"</td>\n" +
                        "<td class=\"active\" style='color: red'>"+res.Deposit_money+"</td>\n" +
                        "<td class=\"active\" style='color: red'>已续住</td>\n" +
                        "</tr>");
            }
        }

    })
});

$("#change_room").click(function () {
    var now_room = $("#now_room").val();
    var ava_money2 = $("#ava_money2").val();
    var ori_room = $("#ori_room").val();
    console.log(ori_room);
    $.ajax({
        url: "/hotel/continue_check",
        data: {
            "now_room": now_room,
            "ava_money2": ava_money2,
            "ori_room": ori_room
        },
        method: "post",
        success: function (res) {
            if (res.code == 1) {
                // console.log("ada");
                $("tr").eq(1).after("<tr>\n" +
                        "<td class=\"active\">"+res.CheckID+"</td>\n" +
                        "<td class=\"active\">"+res.User_name+"</td>\n" +
                        "<td class=\"active\">"+res.User_sex+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_type+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_num+"</td>\n" +
                        "<td class=\"active\">"+res.User_phone+"</td>\n" +
                        "<td class=\"active\" style='color: red'>"+res.Check_roomID+"</td>\n" +
                        "<td class=\"active\">"+res.Check_time+"</td>\n" +
                        "<td class=\"active\">"+res.Check_days+"</td>\n" +
                        "<td class=\"active\" style='color: red'>"+res.Deposit_money+"</td>\n" +
                        "<td class=\"active\" style='color: red'>已调房</td>\n" +
                        "</tr>");
            }
        }

    })
});