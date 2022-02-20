from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from importlib import import_module
from django.conf import settings
from .models import *
from django.db.models import Q
from .forms import LoginForm


info = dict()

# Create your util functions here.


def getUser(email, passcode):
    query_results=Login_Details.objects.filter(email=email,password=passcode)
    if not query_results:
        return None
    else:
        fetched_user=query_results[100].u_id
        print(fetched_user)
        return fetched_user


# create your class views here
class indexView(View):
    def get(self, request):
        print("you are in get request")
        login_form = LoginForm()
        print(request.session["user_type"])
        if request.session.get('is_logged_in', False) == False:
            request.session["user_type"] = "guest"
        else:
            request.session["is_logged_in"] = True
        return render(request, "studio/index.html", {"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): #form is valid
            email=login_form.cleaned_data['user_name']
            passcode=login_form.cleaned_data['passcode']
            fetched_user=user=getUser(email,passcode) #getting the user object or None
            if fetched_user!=None:
                request.session["is_logged_in"] = True
                request.session["user_type"] = user.user_type.type
            else:
                request.session["is_logged_in"] = False
        return render(request, "studio/index.html",{"login_form": login_form})


# previous views functions
def index(request):
    return render(request, "studio/index.html")


def admin_page(request):
    pass


def admin_new_client(request):
    pass


def admin_update_detail(request):
    pass


def admin_first_meeting(request):
    pass


def admin_manage_creations(request):
    pass


def admin_manage_personnel(request):
    pass


def admin_meetings_calendar(request):
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
