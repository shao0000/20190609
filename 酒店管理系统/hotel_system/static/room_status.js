$(".room_status_select").change(function () {
    $this_select=$(this);
    $(this).attr("id","this_select");
    var room_id=$(this).attr("room_id");
    var now_status=$("#this_select option:selected").text();
    console.log(now_status);
    $(this).removeAttr("id");
    $.ajax({
        url:"/hotel/status_ajax",
        data:{
            "now_status":now_status,
            "room_id":room_id,
        },
        method:"post",
        success:function (res) {
            if (res.code==1){
                $this_select.closest("td").next().text(now_status);
                $this_select.closest("td").next().css("color","red");
            }
        },
    });
});