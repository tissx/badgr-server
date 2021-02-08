import requests
from django.conf import settings
# from issuer.models import BadgeInstance
def get_lms_api_token():
    acess_token_credentials=getattr(settings, 'LMS_TOKEN_CREDENTIALS',{})
    lms_url= getattr(settings, 'LMS_ROOT_URL','http://192.168.0.169:8000')
    access_token_url='{}/oauth2/access_token/'.format(lms_url)
    try:
        response = requests.post(access_token_url,data=acess_token_credentials)
        if response.ok:
            acess_token=response.json()['access_token']
        else:
            acess_token=None
    except requests.exceptions.RequestException as e:
        err_msg = "Failed to get user acess token with exception "
        # log.error(err_msg.format(e))
        acess_token=None
    return acess_token

def getUserGrade(badgeinstance,recipient_email):
    acess_token=get_lms_api_token()
    if acess_token:
        lms_url= getattr(settings, 'LMS_ROOT_URL','http://192.168.0.169:8000')
        api_url='{}/mx_utility/api/get_user_grade/'.format(lms_url)
        try:
            headers = {"Authorization": "Bearer {}".format(acess_token)}
            param={'recipient_email':recipient_email,'badge_class_slug':badgeinstance.badgeclass.slug}
            response = requests.get(api_url,headers=headers,params=param)
            if response.ok:
                data=response.json()['data']
                return data
        except requests.exceptions.RequestException as e:
            print(e)
    return dict()

def get_user_grade(badgeinstance):
    from issuer.models import BadgeInstance, BadgeClass
    if not isinstance(badgeinstance, BadgeInstance):
        return None
    else :
        badge_class_slug=badgeinstance.badgeclass.slug
        recipient_email=badgeinstance.user.email
        acess_token=get_lms_api_token()
        grade_detail=getUserGrade(badgeinstance,recipient_email)
        return grade_detail

    


   