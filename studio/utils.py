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
    passcode=rotationalCipher(passcode)
    query_results = Login_Details.objects.filter(
        email=email, password=passcode)
    if not query_results:
        return None
    else:
        fetched_user = query_results[0].u_id
        return fetched_user



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