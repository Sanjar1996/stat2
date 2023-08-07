from django.conf import settings
from django import http
from django.http import HttpResponse


class BlockedIpMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = ['89.249.63.50', '89.249.63.51', '89.249.63.52', '89.249.63.53',
                       '89.249.63.54']  # Authorized ip's

        user_ip = self.get_client_ip(request)
        path_info = request.META.get('PATH_INFO')  # Get requested path

        # if user_ip not in allowed_ips and '/admin/' in path_info:  # ip not in allowed_ips and
        #     return http.HttpResponseForbidden('<h1>Forbidden</h1> ' + str(user_ip)+ '<br>' + str(request.__dict__))

        # If IP is allowed we don't do anything
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('x-forwarded-for')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
