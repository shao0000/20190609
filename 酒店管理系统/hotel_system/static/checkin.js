$(function () {
    $(".reservation_to_check").click(function () {
        $check_button = $(this)
        var room_id = $(this).attr("room_id")
        // console.log(room_id)
        $.ajax({
            url: "/hotel/reservation_to_check",
            data: {
                room_id: room_id
            },
            method: "post",
            success: function (res) {
                // console.log("okkk")
                if (res.code == 1) {
                    $check_button.html("已入住")
                    $check_button.css("color", "red")
                    $("#CheckContent_table").append("<tr>\n" +
                        "<td class=\"active\">"+res.CheckID+"</td>\n" +
                        "<td class=\"active\">"+res.User_name+"</td>\n" +
                        "<td class=\"active\">"+res.User_sex+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_type+"</td>\n" +
                        "<td class=\"active\">"+res.User_cred_num+"</td>\n" +
                        "<td class=\"active\">"+res.User_phone+"</td>\n" +
                        "<td class=\"active\">"+res.Check_roomID+"</td>\n" +
                        "<td class=\"active\">"+res.Check_time+"</td>\n" +
                        "<td class=\"active\">"+res.Check_days+"</td>\n" +
                        "<td class=\"active\">"+res.Deposit_money+"</td>\n" +
                        "<td class=\"active\">已入住</td>\n" +
                        "</tr>")
                }
            }

        })
    })
})