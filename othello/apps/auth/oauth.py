from social_core.backends.oauth import BaseOAuth2
from social_core.pipeline.user import get_username as social_get_username

def get_username(strategy, details, user=None, *args, **kwargs):
    result = social_get_username(strategy, details, user=user, *args, **kwargs)
    return result

# Instead of using an Ion user id, just take the username as a base36 number
def username_to_id(username):
    if not username.isalnum():
        return -1
    id = int(username, 36)
    return id


class IonOauth2(BaseOAuth2):
    name = 'ion'
    AUTHORIZATION_URL = 'https://ion.tjhsst.edu/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://ion.tjhsst.edu/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires')
    ]

    def get_scope(self):
        # The permissions we require when accessing an account
        return ["read"]

    def get_user_details(self, response):
        profile = self.get_json('https://ion.tjhsst.edu/api/profile',
                                params={'access_token': response['access_token']})

        # fields used to populate/update User model
        return {
            'username': profile['ion_username'],
            'full_name': profile['full_name'],
            'id': username_to_id(profile['ion_username']),
            'email': profile['tj_email'],
            'service': False,
            'is_superuser': False,
            'staff': profile['is_teacher'] and not profile['is_student']
        }

    def get_user_id(self, details, response):
        return details['id']
