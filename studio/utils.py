from .models import *

SESSIONS_DEFALUTS = {"is_logged_in":False,
                     "user_logged_in":False,
                     "user_type":"guest",
                     }

#Views Utils
def reset_sessions_to_default(request):
    for key,default_val in SESSIONS_DEFALUTS.items():
        request.session[key]=default_val

def getUser(email, passcode):
    query_results = Login_Details.objects.filter(
        email=email, password=passcode)
    if not query_results:
        return None
    else:
        fetched_user = query_results[0].u_id
        return fetched_user



#Models Utils