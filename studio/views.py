from hashlib import new
import re
from unicodedata import name
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect,HttpResponseNotFound
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
from .calendarAPI import *
import datetime


##
# Create your util function00s here, then move them to utils.


def deleteCreation(request, creation_id):
    creation = Creation.objects.get(id=creation_id)
    creation.delete()
    return HttpResponseRedirect(reverse(viewname="artwork", args=[request.session["supervisor_id"],request.session["client_overview_id"], request.session["album_id"]]))


def createMeetinginProgram(meeting):  # details="2022-05-20-20-00-topic-users"
    startDateTime = datetime.datetime(year=meeting.start_date.year,
                                      month=meeting.start_date.month,
                                      day=meeting.start_date.day,
                                      hour=meeting.start_time.hour,
                                      minute=meeting.start_time.minute,
                                      second=0,
                                      microsecond=0).isoformat()

    endDateTime = datetime.datetime(year=meeting.end_date.year,
                                    month=meeting.end_date.month,
                                    day=meeting.end_date.day,
                                    hour=meeting.end_time.hour,
                                    minute=meeting.end_time.minute,
                                    second=0,
                                    microsecond=0).isoformat()

    service = get_calendar_service()

    event = {
        'summary': meeting.phase_id.creation_id.name + ": " + meeting.topic,
        'location': meeting.location,
        'description': 'Meeting about the client songs',
        'start': {
            'dateTime': startDateTime,
            'timeZone': 'Israel',
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': 'Israel',
        },
        'attendees': [
            {"email":u.login_details.email}
            for u in meeting.attendees.all()
        ]
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return HttpResponseRedirect(reverse("index-page"))


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
    def get(self, request, supervisor_id=0,client_id=0, album_id=0):
        album_id = int(album_id)
        request.session["album_id"] = album_id
        client_id = int(client_id)
        request.session["client_overview_id"] = client_id
        supervisor_id = int(supervisor_id)
        request.session["supervisor_id"] = supervisor_id
        # see creations the current user is working on (either client or worker).
        if client_id == 0 and supervisor_id==0:
            if request.session["user_type"] != "guest":
                # get creations based on which user is logged in
                user_ob = User.objects.filter(
                    id=request.session["user_logged_in_id"])[0]
                if request.session["user_type"] == 'customer':
                    extract_creations = user_ob.creations.all()
                else:
                    extract_creations = Employee.objects.filter(u_id=user_ob)[
                        0].creations.all()
                # filter creations based on album
                if album_id == 0:
                    pass  # do nothing, the user wants to see all the creations
                elif album_id == -1:  # creations with no album.
                    extract_creations = [
                        c for c in extract_creations if c.album_id == None]
                elif album_id == -2:  # creations with any album.
                    extract_creations = [
                        c for c in extract_creations if c.album_id != None]
                else:  # specific album
                    extract_creations_fixed = []
                    for c in extract_creations:
                        if c.album_id != None:
                            if c.album_id.id == album_id:
                                extract_creations_fixed.append(c)
                    extract_creations = extract_creations_fixed
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
        elif client_id != 0 and supervisor_id==0:  # see creations of a specific client as a manger view
            user_ob = User.objects.filter(
                id=client_id)[0]
            extract_creations = user_ob.creations.all()
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
        elif supervisor_id!=0 and client_id == 0:  # see creations of a specific worker as a manger view
            user_ob = User.objects.filter(
                id=supervisor_id)[0]
            employee_ob=Employee.objects.get(u_id=user_ob)
            extract_creations = employee_ob.creations.all()
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
    def post(self, request, supervisor_id=0, client_id=0, album_id=0):
        form = phaseStatusForm(request.POST)
        if form.is_valid():
            # transform changes to dict {phase_id:new_status}
            changes = ast.literal_eval(
                "{"+form.cleaned_data["changes"][:-1]+"}")
            for p_id, new_status_desc in changes.items():
                extract_phase = Phase.objects.filter(phase_id=p_id)[0]
                extract_phase.update_phase_status(new_status_desc)
        return HttpResponseRedirect(reverse(viewname="artwork", args=[request.session["supervisor_id"],request.session["client_overview_id"], request.session["album_id"]]))

class albumsView(View):
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
            # extract albums
            albums = {0: "כל היצירות"}
            albums.update({str(-1): "יצירות ללא אלבום"})
            albums.update({str(-2): "יצירות עם אלבום"})
            albums.update(
                {str(c.album_id.id): c.album_id.name for c in extract_creations if c.album_id != None})
            print(albums)
        return render(request, "studio/pages/albums_page/albums_main.html", {"albums": albums})

    def post(self, request):
        return HttpResponseRedirect(reverse(viewname="index-page"))

class creations_by_creator(View):
    def get(self, request):
        if request.session["user_type"] == "manager":
            creators_data = { creation.creator.id : creation.creator.fname+" "+ creation.creator.lname for creation in Creation.objects.all()}
            return render(request, "studio/pages/creations_page/mods/creations_by_creator.html", {"creators_data": creators_data})
        else:
            return HttpResponseRedirect(reverse(viewname="index-page"))

    def post(self, request):
        return HttpResponseRedirect(reverse(viewname="creations_per_client"))

class creations_by_supervisor(View):
    def get(self, request):
        if request.session["user_type"] == "manager":
            supervisors_data={creations_supers_ob.supervisor.u_id.id:creations_supers_ob.supervisor.u_id.fname+" "+creations_supers_ob.supervisor.u_id.lname for creations_supers_ob  in Creations_Supervisors.objects.all()}
            return render(request, "studio/pages/creations_page/mods/creations_by_supervisor.html", {"supervisors_data": supervisors_data})
        else:
            return HttpResponseRedirect(reverse(viewname="index-page"))

    def post(self, request):
        return HttpResponseRedirect(reverse(viewname="creations_per_client"))


class CreateFileView(View):
    def get(self, request, creation_id):
        u_id = request.session["user_logged_in_id"]
        if request.session["user_type"] in ['guest','customer']:
            return HttpResponseRedirect(reverse("index-page"))
        elif request.session["user_type"]=='worker':
            ok_list = permitted_creations_list(u_id)
            if creation_id not in ok_list:
                return HttpResponseRedirect(reverse("index-page"))
        #if we've gotten this far, it means that either the logged in user is manager or worker with permitted access
        form = CreationFileForm()
        try:
            creation_ob = Creation.objects.filter(id=creation_id)[0]
        except Creation.DoesNotExist:
            return HttpResponseNotFound("<h1>משהו השתבש, נסה שוב</h1>")
        all_files = CreationFile.objects.filter(creation=creation_ob)
        return render(request, "studio/pages/upload_files_page/upload_files_main.html", {
            "form": form,
            "files": all_files,
            "creation_id": creation_id
        })

    def post(self, request, creation_id):
        submitted_form = CreationFileForm(request.POST, request.FILES)
        u_id = request.session["user_logged_in_id"]
        if request.session["user_type"] in ['guest','customer']:
            return HttpResponseRedirect(reverse("index-page"))
        elif request.session["user_type"]=='worker':
            ok_list = permitted_creations_list(u_id)
            if creation_id not in ok_list:
                return HttpResponseRedirect(reverse("index-page"))
        creation_ob = Creation.objects.filter(id=creation_id)[0]
        nowdate = str(timezone.localdate()).replace("-", "_")
        fname = creation_ob.name[:3]+"_"+nowdate+"." + \
            str(request.FILES["audioFile"]).split(".")[-1]
        print(fname)
        if submitted_form.is_valid():
            #delete old file
            for f in CreationFile.objects.filter(creation=creation_ob):
                f.delete()
            newfile = CreationFile(audioFile=request.FILES["audioFile"],
                                   creation=creation_ob, fname=fname)
            newfile.save()
            return HttpResponseRedirect(reverse(viewname="files_upload", args=[int(creation_id)]))

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
    return HttpResponseRedirect(reverse(viewname="artwork", args=[request.session["supervisor_id"],request.session["client_overview_id"], request.session["album_id"]]))


class notesView(View):
    def get(self, request, creation_id):
        u_id = request.session["user_logged_in_id"]
        ok_list = permitted_creations_list(u_id)
        # managers can look + add any notes anywhere
        if creation_id not in ok_list and request.session["user_type"] != 'manager':
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
        customer_user_type = User_Type.objects.filter(
            type="customer")  # need to grab all customers
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        all_customers_names = [cus.fname+" "+cus.lname +
                               "|"+str(cus.id) for cus in all_customers]
        form = newProgramSingleForm(initial={'creation_type': 'musical'})
        dict_of_defaults = {"song": ["פגישה ראשונה", "קביעת מילים ולחן", "סקיצה ראשונה", "עריכה מוזיקלית", "עריכה סופית", "אישור לקוח"],
                            "podcast": ["פגישה ראשונה", "הקלטה", "עריכה", "אישור לקוח"]}
        dict_of_lenghts = {"song": len(dict_of_defaults["song"]),
                           "podcast": len(dict_of_defaults["podcast"])}
        return render(request, "studio/pages/new_program_page/pages/new_program_single.html",
                      {'all_customers': all_customers,
                       "all_customers_names": all_customers_names,
                       "form": form,
                       "dict_of_defaults": dict_of_defaults,
                       "dict_of_lenghts": dict_of_lenghts,

                       })

    def post(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        form = newProgramSingleForm(request.POST)
        success = False
        if form.is_valid():
            print(form.cleaned_data)
            creator_id = int(form.cleaned_data["creator_choice"].split('|')[1])
            creation_name = form.cleaned_data["creation_name"]
            phases_list = form.cleaned_data["phases_names"]
            phases_list = '{'+phases_list[:len(phases_list)-1]+'}'  # dict rep
            phases_list = ast.literal_eval(
                phases_list)  # now it's a dictionary
            # but might have duplicates becuase of unknown error
            phases_list = list(phases_list.values())
            phases_list = list(dict.fromkeys(phases_list))
            # get creator, supervisor
            creator = User.objects.filter(id=creator_id)[0]
            supervisor = Employee.objects.filter(u_id=user_ob)[0]
            # creating objects
            newcreation = Creation.objects.create(
                name=creation_name,
                creator=creator,
            )
            newcreation.supervisors.add(supervisor)
            print(phases_list)
            # create first phase
            first_phase_object = Phase.objects.create(
                creation_id=newcreation,
                status=Status.objects.filter(desc="not_done")[0],
                name=phases_list[0]
            )
            for phase in phases_list[1:]:
                new_phase_ob = Phase.objects.create(
                    creation_id=newcreation,
                    status=Status.objects.filter(desc="not_done")[0],
                    name=phase
                )
            # create meeting:
            m_phase = first_phase_object
            m_start_date = form.cleaned_data["start_date"]
            m_end_date = form.cleaned_data["start_date"]
            m_start_time = form.cleaned_data["start_time"]
            m_end_time = datetime.datetime(year=m_start_date.year,
                                           month=m_start_date.month,
                                           day=m_start_date.day,
                                           hour=m_start_time.hour+1,
                                           minute=m_start_time.minute,
                                           second=0,
                                           microsecond=0)
            m_topic = first_phase_object.name
            m_location = 'Dynamic Studio Kfar Saba'
            meeting_ob = Meeting(phase_id=m_phase,
                                 start_date=m_start_date,
                                 end_date=m_end_date,
                                 start_time=m_start_time,
                                 end_time=m_end_time,
                                 topic=m_topic,
                                 location=m_location)
            meeting_ob.save()
            meeting_ob.attendees.add(user_ob, creator)
            createMeetinginProgram(meeting_ob)
            # set success as True
            success = True
        return render(request, "studio/pages/new_program_page/pages/new_program_created.html",
                      {"success": success,
                       })


class createMeeting(View):
    def get(self, request):

        form = CreateMeetingForm()

        list_of_options = []
        for u in User.objects.all():
            for c in u.creations.all():
                for p in c.phases.all():
                    list_of_options.append(
                        "|".join([c.name, p.name, u.fname+" "+u.lname, str(u.id), p.phase_id]))
        return render(request, "studio/pages/new_meeting_page/pages/new_meeting_main.html",
                      {"form": form,
                       "list_of_options": list_of_options
                       })

    def post(self, request):
        success = False
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        form = CreateMeetingForm(request.POST)
        if form.is_valid():
            p_id = form.cleaned_data['creator_creation_phase'].split("|")[-1]
            u_id = form.cleaned_data['creator_creation_phase'].split("|")[-2]
            phase = Phase.objects.get(phase_id=p_id)
            creator = User.objects.get(id=u_id)
            m_start_date = form.cleaned_data["start_date"]
            m_end_date = form.cleaned_data["start_date"]
            m_start_time = form.cleaned_data["start_time"]
            m_end_time = datetime.datetime(year=m_start_date.year,
                                           month=m_start_date.month,
                                           day=m_start_date.day,
                                           hour=m_start_time.hour+1,
                                           minute=m_start_time.minute,
                                           second=0,
                                           microsecond=0)
            m_topic = phase.name
            m_location = 'Dynamic Studio Kfar Saba'
            meeting_ob = Meeting(phase_id=phase,
                                 start_date=m_start_date,
                                 end_date=m_end_date,
                                 start_time=m_start_time,
                                 end_time=m_end_time,
                                 topic=m_topic,
                                 location=m_location)
            meeting_ob.save()
            meeting_ob.attendees.add(user_ob, creator)
            createMeetinginProgram(meeting_ob)
            success = True
        return render(request, "studio/pages/new_meeting_page/pages/new_meeting_created.html",
                      {"success": success,
                       })
        return HttpResponseRedirect(reverse("index-page"))


class newProgramMultiple(View):

    def get(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        customer_user_type = User_Type.objects.filter(
            type="customer")  # need to grab all customers
        all_customers = User.objects.filter(user_type__in=customer_user_type)
        all_customers_names = [cus.fname+" "+cus.lname +
                               "|"+str(cus.id) for cus in all_customers]
        form = newProgramMultipleForm(initial={'creation_type': 'musical'})
        dict_of_defaults = {"song": ["פגישה ראשונה", "קביעת מילים ולחן", "סקיצה ראשונה", "עריכה מוזיקלית", "עריכה סופית", "אישור לקוח"],
                            "podcast": ["פגישה ראשונה", "הקלטה", "עריכה", "אישור לקוח"]}
        dict_of_lenghts = {"song": len(dict_of_defaults["song"]),
                           "podcast": len(dict_of_defaults["podcast"])}
        return render(request, "studio/pages/new_program_page/pages/new_program_multiple.html",
                      {'all_customers': all_customers,
                       "all_customers_names": all_customers_names,
                       "form": form,
                       "dict_of_defaults": dict_of_defaults,
                       "dict_of_lenghts": dict_of_lenghts,

                       })

    def post(self, request):
        user_ob = User.objects.filter(
            id=request.session["user_logged_in_id"])[0]
        form = newProgramMultipleForm(request.POST)
        success = False

        if form.is_valid():
            ALBUM_DONE = form.cleaned_data["albumDone"]
            # create album if not exist
            newAlbumOb, created = Album.objects.get_or_create(
                name=form.cleaned_data["albumName"])
            # create the creation, its phases and connect to album
            creator_id = int(form.cleaned_data["creator_choice"].split('|')[1])
            creation_name = form.cleaned_data["creation_name"]
            phases_list = form.cleaned_data["phases_names"]
            phases_list = '{'+phases_list[:len(phases_list)-1]+'}'  # dict rep
            phases_list = ast.literal_eval(
                phases_list)  # now it's a dictionary
            # but might have duplicates becuase of unknown error
            phases_list = list(phases_list.values())
            phases_list = list(dict.fromkeys(phases_list))
            # get creator, supervisor
            creator = User.objects.filter(id=creator_id)[0]
            supervisor = Employee.objects.filter(u_id=user_ob)[0]
            # creating objects
            newcreation = Creation.objects.create(
                name=creation_name,
                creator=creator,
                album_id=newAlbumOb
            )
            newcreation.supervisors.add(supervisor)
            print(phases_list)
            # create first phase
            first_phase_object = Phase.objects.create(
                creation_id=newcreation,
                status=Status.objects.filter(desc="not_done")[0],
                name=phases_list[0]
            )
            for phase in phases_list[1:]:
                new_phase_ob = Phase.objects.create(
                    creation_id=newcreation,
                    status=Status.objects.filter(desc="not_done")[0],
                    name=phase
                )
            # create meeting:
            m_phase = first_phase_object
            m_start_date = form.cleaned_data["start_date"]
            m_end_date = form.cleaned_data["start_date"]
            m_start_time = form.cleaned_data["start_time"]
            m_end_time = datetime.datetime(year=m_start_date.year,
                                           month=m_start_date.month,
                                           day=m_start_date.day,
                                           hour=m_start_time.hour+1,
                                           minute=m_start_time.minute,
                                           second=0,
                                           microsecond=0)
            m_topic = first_phase_object.name
            m_location = 'Dynamic Studio Kfar Saba'
            meeting_ob = Meeting(phase_id=m_phase,
                                 start_date=m_start_date,
                                 end_date=m_end_date,
                                 start_time=m_start_time,
                                 end_time=m_end_time,
                                 topic=m_topic,
                                 location=m_location)
            meeting_ob.save()
            meeting_ob.attendees.add(user_ob, creator)
            createMeetinginProgram(meeting_ob)
            # set success as True
            success = True

        # REDIRECTION BASED ON SITUATION: "ALBUM_DONE==TRUE"
        if ALBUM_DONE != "1":
            # loading neccecery data
            customer_user_type = User_Type.objects.filter(
                type="customer")  # need to grab all customers
            all_customers = User.objects.filter(
                user_type__in=customer_user_type)
            all_customers_names = [cus.fname+" "+cus.lname +
                                   "|"+str(cus.id) for cus in all_customers]
            dict_of_defaults = {"song": ["פגישה ראשונה", "קביעת מילים ולחן", "סקיצה ראשונה", "עריכה מוזיקלית", "עריכה סופית", "אישור לקוח"],
                                "podcast": ["פגישה ראשונה", "הקלטה", "עריכה", "אישור לקוח"]}
            dict_of_lenghts = {"song": len(dict_of_defaults["song"]),
                               "podcast": len(dict_of_defaults["podcast"])}
            return render(request, "studio/pages/new_program_page/pages/new_program_multiple.html",
                          {'all_customers': all_customers,
                           "all_customers_names": all_customers_names,
                           "form": form,
                           "dict_of_defaults": dict_of_defaults,
                           "dict_of_lenghts": dict_of_lenghts,
                           "existing_creator": form.cleaned_data["creator_choice"]
                           })
        else:
            return render(request, "studio/pages/new_program_page/pages/new_album_created.html",
                          {"success": success,
                           })


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


class ReportHours(View):
    def get(self, request):
        report_form = ReportHoursForm()
        return render(request, "studio/pages/report_hours/report_hours.html", {'report_form': report_form})

    def post(self, request, user_id):
        pass


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
