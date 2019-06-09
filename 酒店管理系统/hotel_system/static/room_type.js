$("#RoomID2").change(function () {
    var RoomID = $("#RoomID2 option:selected").text();
    console.log(RoomID);
    $.ajax({
        url: "/hotel/ajax",
        data: {
            "RoomID": RoomID
        },
        method: "post",
        success: function (res) {
            if (res.code == 1) {
                $("input[name='RoomType2']").val(res.RoomType);
                $("input[name='RoomPrice2']").val(res.RoomPrice);
                $("input[name='RoomArea2']").val(res.RoomArea);
                $("input[name='RoomBed2']").val(res.RoomBed);
                $("input[name='RoomWifi2']").val(res.RoomWifi);
                $("input[name='RoomRemarks2']").val(res.RoomRemarks);

            };

        },

    });
});

$("#RoomID3").change(function () {
    var RoomID = $("#RoomID3 option:selected").text();
    console.log(RoomID);
    $.ajax({
        url: "/hotel/ajax",
        data: {
            "RoomID": RoomID
        },
        method: "post",
        success: function (res) {
            if (res.code == 1) {
                $("input[name='RoomType3']").val(res.RoomType);
                $("input[name='RoomPrice3']").val(res.RoomPrice);
                $("input[name='RoomArea3']").val(res.RoomArea);
                $("input[name='RoomBed3']").val(res.RoomBed);
                $("input[name='RoomWifi3']").val(res.RoomWifi);
                $("input[name='RoomRemarks3']").val(res.RoomRemarks);

            };

        },

    });
});