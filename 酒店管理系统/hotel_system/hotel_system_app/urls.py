from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^home$', home),
    url(r"^query_(?P<param>\d+)$", query, name="query"),
    url(r"^reservation$", reservation, name="reservation"),
    url(r"^again_reservation$", again_reservation, name="again_reservation"),
    url(r"^cancel_reservation$", cancel_reservation),
    url(r"^check$", check, name="check"),
    url(r"^reservation_to_check$", reservation_to_check),
    url(r"^new_checkin$", new_checkin, name="new_checkin"),
    url(r"^room_change$", room_change, name="room_change"),
    url(r"^continue_check$", continue_check),
    url(r"^room_settlement$", room_settlement, name="room_settlement"),
    url(r"^stay_other$", stay_other),
    url(r"^all_total_balance_accounts$", all_total_balance_accounts),
    url(r"^room_type$", room_type, name="room_type"),
    url(r"^room_modify$", room_modify, name="room_modify"),
    url(r"^ajax$", ajax),
    url(r"^room_delete$", room_delete, name="room_delete"),
    url(r"^room_status$", room_status, name="room_status"),
    url(r"^status_ajax$", status_ajax),
]
