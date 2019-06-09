$(function () {
    $(".cancel_reservation").click(function () {
    $reservation_button=$(this)
    var room_id=$(this).attr("room_id")
    // console.log(room_id)
    $.ajax({
        url:"/hotel/cancel_reservation",
        data:{
            room_id:room_id
        },
        method:"post" ,
        success:function (res) {
            console.log("okkk")
            if (res.code==1){
                $reservation_button.html("已取消")
                $reservation_button.css("color","red")
            }
        }

        })
    })
})