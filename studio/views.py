from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from importlib import import_module
from django.conf import settings
from .models import *
from django.db.models import Q
from .forms import LoginForm

SESSIONS_DEFALUTS = {"is_logged_in":False,
                     "user_logged_in":False,
                     "user_type":"guest",
                     }

# Create your util functions here.

def reset_sessions_to_default(request):
    for key,default_val in SESSIONS_DEFALUTS.items():
        request.session[key]=default_val

def logoutFunc(request):
    reset_sessions_to_default(request)
    login_form = LoginForm()
    return render(request, "studio/index.html", {"login_form": login_form})


def all_unexpired_sessions_for_user(user):
    user_sessions = []
    all_sessions = Session.objects.filter(
        expire_date__gte=datetime.datetime.now())
    for session in all_sessions:
        session_data = session.get_decoded()
        if user.pk == session_data.get('_auth_user_id'):
            user_sessions.append(session.pk)
    return Session.objects.filter(pk__in=user_sessions)


def delete_all_unexpired_sessions_for_user(user, session_to_omit=None):
    session_list = all_unexpired_sessions_for_user(user)
    if session_to_omit is not None:
        session_list.exclude(session_key=session_to_omit.session_key)
    session_list.delete()


def getUser(email, passcode):
    query_results = Login_Details.objects.filter(
        email=email, password=passcode)
    if not query_results:
        return None
    else:
        fetched_user = query_results[0].u_id
        return fetched_user


# create your class views here
class indexView(View):
    def get(self, request):

        login_form = LoginForm()
        request.session["is_logged_in"] = False
        request.session["user_type"] = "guest"
        return render(request, "studio/index.html", {"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # form is valid
            email = login_form.cleaned_data['user_name']
            passcode = login_form.cleaned_data['passcode']
            # getting the user object or None
            fetched_user = user = getUser(email, passcode)
            if fetched_user != None:
                request.session["is_logged_in"] = True
                request.session["user_type"] = user.user_type.type
            else:
                request.session["is_logged_in"] = False
        return render(request, "studio/index.html", {"login_form": login_form})


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
