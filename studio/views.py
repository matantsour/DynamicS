from hashlib import new
import re
from unicodedata import name
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from importlib import import_module
from django.conf import settings
from .models import *
from django.db.models import Q
from .forms import *
from .utils import *
from django.urls import reverse
from django.utils import timezone
import ast
from django.views.generic.edit import CreateView


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
                user.update_login_time(timezone.now())
            else:
                request.session["is_logged_in"] = False

        return render(request, "studio/index.html", {"login_form": login_form})


class creationsView(View):
    def get(self, request):
        if request.session["user_type"] != "guest":
            # get creations based on which user is logged in
            user_ob = User.objects.filter(
                id=request.session["user_logged_in_id"])[0]
            if request.session["user_type"] == 'customer':
                extract_creations = user_ob.creations.all()
            else:
                extract_creations = Employee.objects.filter(u_id=user_ob)[
                    0].creations.all()
            list_of_creations = sorted(
                extract_creations, key=lambda c: c.completion_percent(), reverse=True)
            # sort creations
            creations_phases_not_done = {
                c: c.phases.all() for c in list_of_creations if c.completion_percent() != 1}
            creations_phases_done = {
                c: c.phases.all() for c in list_of_creations if c.completion_percent() == 1}
            exists_completed_creations = True if creations_phases_done else False
            # creation_phases_update_form
            update_phases_form = phaseStatusForm()
            return render(request, "studio/pages/creations_page/creations_main.html",
                          {"user_name": user_ob.lname,
                           "list_of_creations": list_of_creations,
                           "creations_phases_not_done": creations_phases_not_done,
                           "creations_phases_done": creations_phases_done,
                           "exists_completed_creations": exists_completed_creations,
                           "update_phases_form": update_phases_form})
        else:
            return HttpResponseRedirect(reverse("index-page"))

    def post(self, request):
        form = phaseStatusForm(request.POST)
        if form.is_valid():
            # transform changes to dict {phase_id:new_status}
            changes = ast.literal_eval(
                "{"+form.cleaned_data["changes"][:-1]+"}")
            for p_id, new_status_desc in changes.items():
                extract_phase = Phase.objects.filter(phase_id=p_id)[0]
                extract_phase.update_phase_status(new_status_desc)
        return HttpResponseRedirect(reverse("artwork"))


class CreateFileView(View):
    def get(self, request, creation_id):
        u_id = request.session["user_logged_in_id"]
        ok_list = permitted_creations_list(u_id)
        if creation_id not in ok_list:
            return HttpResponseRedirect(reverse("index-page"))
        form = CreationFileForm()
        all_files = CreationFile.objects.all()
        print(all_files)
        return render(request, "studio/pages/upload_files_page/upload_files_main.html", {
            "form": form,
            "files": all_files,
            "creation_id": creation_id
        })

    def post(self, request, creation_id):
        submitted_form = CreationFileForm(request.POST, request.FILES)
        u_id = request.session["user_logged_in_id"]
        ok_list = permitted_creations_list(u_id)
        if creation_id not in ok_list:
            return HttpResponseRedirect(reverse("index-page"))
        creation = Creation.objects.filter(id=creation_id)[0]
        nowdate = str(timezone.localdate()).replace("-", "_")
        fname = creation.name[:3]+"_"+nowdate+"." + \
            str(request.FILES["audioFile"]).split(".")[-1]
        print(fname)
        if submitted_form.is_valid():
            newfile = CreationFile(audioFile=request.FILES["audioFile"],
                                   creation=creation, fname=fname)
            newfile.save()
            return render(request, "studio/includes/welcome_user.html")

        return render(request, "studio/pages/upload_files_page/upload_files_main.html", {
            "form": form,
            "creation": find_creation
        })


class last_version(View):
    def get(self, request, creation_id):
        creationfile = CreationFile.objects.all()[0]
        return render(request, "studio/pages/last_version_page/last_version_main.html", {"creationfile": creationfile})


def client_approved_click(request, creation_id):
    creation = Creation.objects.get(id=creation_id).client_approved()
    return redirect('artwork')


class notesView(View):
    def get(self, request, creation_id):
        u_id = request.session["user_logged_in_id"]
        ok_list = permitted_creations_list(u_id)
        if creation_id not in ok_list:
            return HttpResponseRedirect(reverse("index-page"))
        find_creation = Creation.objects.filter(id=creation_id)
        if find_creation:
            creation_name = find_creation[0].name
            notes = find_creation[0].notes.all()
            customer_notes = []
            other_notes = []
            all_notes = []
            new_note = AddNote()
            for i in notes:
                if str(i.user.user_type) == 'customer':
                    customer_notes.append((i, 'customer'))
            for i in notes:
                if str(i.user.user_type) != 'customer':
                    other_notes.append((i, 'nocustomer'))
            all_notes = customer_notes+other_notes
            all_notes.sort(key=lambda y: y[1])

        return render(request, "studio/pages/notes_page/notes_main.html",
                      {'creation_name': creation_name,
                       'creation_id': creation_id,
                       "notes": notes,
                       "other_notes": other_notes,
                       "customer_notes": customer_notes,
                       "all_notes": all_notes,
                       'new_note': new_note})

    def post(self, request, creation_id):
        find_creation = Creation.objects.filter(id=creation_id)
        if find_creation:
            note_form = AddNote(request.POST)
            if note_form.is_valid():
                new_note = Note(creation=find_creation[0], user=User.objects.filter(
                    id=request.session["user_logged_in_id"])[0], text=note_form.cleaned_data['text'])
                new_note.save()
            creation_name = find_creation[0].name
            notes = find_creation[0].notes.all()
            customer_notes = []
            other_notes = []
            all_notes = []
            new_note = AddNote()
            for i in notes:
                if str(i.user.user_type) == 'customer':
                    customer_notes.append((i, 'customer'))
            for i in notes:
                if str(i.user.user_type) != 'customer':
                    other_notes.append((i, 'nocustomer'))
            all_notes = customer_notes+other_notes
            all_notes.sort(key=lambda y: y[1])

        return render(request, "studio/pages/notes_page/notes_main.html",
                      {'creation_name': creation_name,
                       'creation_id': creation_id,
                       "notes": notes,
                       "other_notes": other_notes,
                       "customer_notes": customer_notes,
                       "all_notes": all_notes,
                       'new_note': new_note})


class userMeetingView(View):
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        user_list_of_meetings = user_ob.meetings.all()
        return render(request, "studio/pages/meetings_page/meetings_main.html", {"user_name": user_ob.lname, "list_of_meetings": user_list_of_meetings})

    def post(self, request):
        pass


class newProgram(View):
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        customer_user_type = User_Type.objects.filter(type="customer")
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        return render(request, "studio/pages/new_program_page/new_program_main.html", {"user_name": user_ob.lname, 'all_customers': all_customers})

    def post(self, request):
        pass


class newProgramSingle(View):
    
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        customer_user_type = User_Type.objects.filter(type="customer") #need to check if user is allowed
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        all_customers_names=[cus.fname+" "+cus.lname+"|"+str(cus.id) for cus in all_customers]
        form = newProgramSingleForm()
        dict_of_defaults = {"song":["פגישה ראשונה","קביעת מילים ולחן","סקיצה ראשונה","עריכה מוזיקלית","עריכה סופית","אישור לקוח"],
                            "podcast":["פגישה ראשונה","הקלטה","עריכה","אישור לקוח"]}
        dict_of_lenghts = {"song":len(dict_of_defaults["song"]),
                            "podcast":len(dict_of_defaults["podcast"])}
        return render(request, "studio/pages/new_program_page/pages/new_program_single.html",
                      {'all_customers': all_customers,
                      "all_customers_names":all_customers_names,
                      "form":form,
                      "dict_of_defaults":dict_of_defaults,
                      "dict_of_lenghts":dict_of_lenghts,
                      
                       })

    def post(self, request):
        customer_user_type = User_Type.objects.filter(type="customer")
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        form = newProgramSingleForm(request.POST)
        dict_of_defaults = {"song":["פגישה ראשונה","קביעת מילים ולחן","סקיצה ראשונה","עריכה מוזיקלית","עריכה סופית","אישור לקוח"],
                            "podcast":["פגישה ראשונה","הקלטה","עריכה","אישור לקוח"]}
        dict_of_lenghts = {"song":len(dict_of_defaults["song"]),
                            "podcast":len(dict_of_defaults["podcast"])}
        if form.is_valid():
            print(form.cleaned_data)
        new_form=newProgramSingleForm()
        return render(request, "studio/pages/new_program_page/pages/new_program_single.html",
                      {'all_customers': all_customers,
                      "form":new_form,
                      "dict_of_defaults":dict_of_defaults,
                      "dict_of_lenghts":dict_of_lenghts
                       })

class newProgramMultiple(View):
    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        customer_user_type = User_Type.objects.filter(type="customer")
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        return render(request, "studio/pages/new_program_page/pages/new_program_multiple.html", {"user_name": user_ob.lname, 'all_customers': all_customers})

    def post(self, request):
        pass


class Update_user_details(View):
    def get(self, request, user_id):
        if request.session["user_type"] == 'manager':
            search_id = user_id
        else:
            search_id = request.session["user_logged_in_id"]
        user = User.objects.filter(id=search_id)[0]
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
                      {"update_form": update_form,
                       "u": user})

    def post(self, request, user_id):
        if request.session["user_type"] == 'manager':
            search_id = user_id
        else:
            search_id = request.session["user_logged_in_id"]
        user = User.objects.filter(id=search_id)[0]
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
                       "message": message,
                       "u": user})


class admin_update_details(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "studio/pages/admin_update_details_page/admin_update_details.html",
                      {"users": users})

    def post(self, request):
        pass


class delete_user(View):
    def get(self, request):
        pass

    def post(self, request, user_id):
        pass

# functional views


def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return HttpResponseRedirect(reverse("admin_update_details"))


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
