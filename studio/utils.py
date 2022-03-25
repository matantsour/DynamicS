from .models import *

SESSIONS_DEFALUTS = {"is_logged_in":False,
                    "user_type":"guest",
                     "user_logged_in_fname":False,
                     "user_logged_in_id":False
                     }

#Views Utils

def permitted_creations_list(user_id):
    fetched_user=User.objects.filter(id=user_id)[0]
    if fetched_user==None:
        return []
    else:
        user_type=fetched_user.user_type.type
        if user_type=='customer':
            creations=fetched_user.creations.all()
        else: #it's a manager or worker
            creations=Employee.objects.filter(u_id=fetched_user)[0].creations.all()
    return [c.id for c in creations]

def reset_sessions_to_default(request):
    for key,default_val in SESSIONS_DEFALUTS.items():
        request.session[key]=default_val



def getUser(email, passcode):
    passcode=rotationalCipher(passcode)
    query_results = Login_Details.objects.filter(
        email=email, password=passcode)
    if not query_results:
        return None
    else:
        fetched_user = query_results[0].u_id
        return fetched_user


def get_password_update_details_form(user,dets):
    ##password validation:
    #old password validation - password should match what is in the DB already
    #new password validation - both new passcode boxes should be itentical and != current password
    is_password_okay=True
    current_pass=dets['current_password'] # we got this from the form
    new_pass=dets['new_password']
    repeat_new_pass=dets['repeat_new_password']
    cond1=user.is_password_okay(rotationalCipher(current_pass))
    cond2=current_pass!=new_pass
    cond3=new_pass==repeat_new_pass
    is_password_okay=(cond1 and cond2 and cond3)
    if is_password_okay:
        return rotationalCipher(new_pass)
    return rotationalCipher(current_pass)



#Models Utils
DIGITS=['0','1','2','3','4','5','6','7','8','9']
ALPHAS=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
SPECIAL_SIGNS=list(" '"'!#$%&()*+,-./:;<=>?@[\]^_`{|}~"'"")
def circular_k(arr,starting_idx,steps):
    max_index=len(arr)-1
    new_idx=starting_idx+steps
    while new_idx>max_index:
        new_idx-=max_index+1
    return arr[new_idx]


def rotationalCipher(input, rotation_factor=3):
    output=""
    for c in list(input):
        if c.isdigit():
            output=output+circular_k(DIGITS, DIGITS.index(c), rotation_factor)
        elif c.isalpha():
            k=circular_k(ALPHAS, ALPHAS.index(c), rotation_factor)
            k=k.upper() if c.isupper() else k.lower()
            output = output + k
        elif c in SPECIAL_SIGNS:
            output=output+circular_k(SPECIAL_SIGNS, SPECIAL_SIGNS.index(c), rotation_factor)
        else:
            output = output + c
    return output