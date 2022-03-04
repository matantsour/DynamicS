import re
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from importlib import import_module
from django.conf import settings
from .models import *
from django.db.models import Q
from .forms import LoginForm, UpdateUserDetailsForm
from .utils import *
from django.urls import reverse


##
# Create your util functions here, then move them to utils.


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
            user = getUser(email, passcode)
            if user != None:
                request.session["is_logged_in"] = True
                request.session["user_type"] = user.user_type.type
                request.session["user_logged_in_fname"] = user.fname
                request.session["user_logged_in_id"] = user.id
            else:
                request.session["is_logged_in"] = False
        return render(request, "studio/index.html", {"login_form": login_form})


class creationsView(View):
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        list_of_creations = user_ob.creations.all()
        creations_phases = {c: c.phases.all() for c in list_of_creations}
        return render(request, "studio/pages/creations_page/creations_main.html",
                      {"user_name": user_ob.lname,
                       "list_of_creations": list_of_creations,
                       "creations_phases": creations_phases})

    def post(self, request):
        pass


class userMeetingView(View):
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        user_list_of_meetings = user_ob.meetings.all()
        return render(request, "studio/pages/meetings_page/meetings_main.html", {"user_name": user_ob.lname, "list_of_meetings": user_list_of_meetings})

    def post(self, request):
        pass

    def post(self, request):
        pass


class Update_user_details(View):
    def get(self, request):
        user = User.objects.filter(id=request.session["user_logged_in_id"])[0]
        initial_dict = {
            'fname': user.fname,
            'lname': user.lname,
            'city': user.city,
            'phone': user.phone,
            'dob': user.dob,
            'organization': user.organization,
            'current_password': user.login_details.password,
            'new_password': user.login_details.password,
            'repeat_new_password': user.login_details.password}
        update_form = UpdateUserDetailsForm(initial=initial_dict)
        return render(request, "studio/pages/user_details_page/user_details_main.html",
                      {"update_form": update_form})

    def post(self, request):
        user = User.objects.filter(id=request.session["user_logged_in_id"])[0]
        update_form = UpdateUserDetailsForm(request.POST)
        params = dict()
        form_fields = ['fname', 'lname', 'city',
                       'phone', 'dob', 'organization']
        print(update_form.is_valid())
        print(update_form.errors)
        if update_form.is_valid():
            for c in form_fields:
                params[c] = update_form.cleaned_data[c]
            params['password'] = get_password_update_details_form(
                user, update_form.cleaned_data)
        flag = user.update_user_details(params)
        if flag:
            message = 'עדכון הפרטים הצליח'
            request.session["user_logged_in_fname"] = user.fname
        else:
            message = 'עלייך להשתמש בסיסמה אחרת'

        return render(request, "studio/pages/user_details_page/user_details_main.html",
                      {"update_form": update_form,
                       "message": message})


# functional views

def logoutFunc(request):
    reset_sessions_to_default(request)
    return HttpResponseRedirect(reverse("index-page"))


# old views functions

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
