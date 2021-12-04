from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"studio/index.html")

def admin_page(request):
    pass

def admin_new_client (request):
    pass

def admin_update_detail (request):
    pass

def admin_first_meeting(request):
    pass

def admin_manage_creations(request):
    pass

def admin_manage_personnel(request):
    pass

def admin_meetings_calendar (request):
    pass

def admin_finance(request):
    pass

def admin_last_files(request):
    pass

def worker_page(request):
    pass

def worker_tasks(request):
    pass

def worker_upload(request):
    pass

def worker_mettings(request):
    pass

def client_page(request):
    pass

def client_creations(request):
    pass

def client_meetings(request):
    pass

def client_details(request):
    pass
