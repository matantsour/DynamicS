
from django.urls import path
from . import views


urlpatterns = [
    path("",views.indexView.as_view()),

    #Admin
    path("admin/",views.admin_page),
    path("admin/add-client",views.admin_new_client),
    path("admin/update-details",views.admin_update_detail),
    path("admin/first-meeting",views.admin_first_meeting),
    path("admin/manage-creations",views.admin_manage_creations),
    path("admin/personnel-lists",views.admin_manage_personnel),
    path("admin/meetings",views.admin_meetings_calendar),
    path("admin/finance",views.admin_finance),
    path("admin/last-files",views.admin_last_files),

    #Worker
    path("worker/",views.worker_page),
    path("worker/tasks",views.worker_tasks),
    path("worker/upload",views.worker_upload),
    path("worker/mettings",views.worker_mettings),

    #Client
    path("client/",views.client_page),
    path("client/creations",views.client_creations),
    path("client/meetings",views.client_meetings),
    path("client/details",views.client_details)

]