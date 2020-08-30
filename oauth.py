import json

from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class VkSignIn(OAuthSignIn):
    def __init__(self):
        super(VkSignIn, self).__init__('vk')
        self.service = OAuth2Service(
            name='vk',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url = None
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='friends, email, offline',
            response_type='code',
            redirect_uri = self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None
        oauth_session = self.service.get_raw_access_token(
            data = {'code': request.args['code'],
                  'client_id': self.consumer_id, 
                  'client_secret' :self.consumer_secret,
                  'redirect_uri': self.get_callback_url()},
        )
        
        user_id = oauth_session.json().get('user_id')
        token = oauth_session.json().get('access_token')
        
        return user_id, token
