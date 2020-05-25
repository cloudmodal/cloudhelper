"""iam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from . import api
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

from .swagger import get_swagger_view
from . import views


api_v1 = [
    path('authentication/', include('authentication.urls.api_urls', namespace='api-auth')),
    path('common/', include('common.urls.api_urls', namespace='api-common')),
    path('account/', include('account.urls.api_urls', namespace='api-account')),
    path('access/', include('access.urls.api_urls', namespace='api-access')),
    path('orgs/', include('organization.urls.api_urls', namespace='api-orgs')),
    path('audits/', include('audits.urls.api_urls', namespace='api-audits')),
    path('assets/', include('assets.urls.api_urls', namespace='api-assets')),
]


app_view_patterns = [
    path('auth/', include('authentication.urls.views_urls', namespace='auth')),
    path('audits/', include('audits.urls.views_urls', namespace='audits')),
    path('assets/', include('assets.urls.views_urls', namespace='assets')),
    path('account/', include('account.urls.views_urls', namespace='account')),
    path('credentials/', include('access.urls.views_urls', namespace='credentials')),
]


js_i18n_patterns = i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)


urlpatterns = [
    # path('', api.IndexAPI.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('v1/', include(api_v1)),
    path('i18n/<str:lang>/', views.I18NView.as_view(), name='i18n-switch'),
    # External apps url
    path('captcha/', include('captcha.urls')),
]

urlpatterns += app_view_patterns
urlpatterns += js_i18n_patterns

if settings.DEBUG:
    urlpatterns += [
        re_path('swagger(?P<format>.json|.yaml)',
                get_swagger_view().without_ui(cache_timeout=1), name='schema-json'),
        path('docs/', get_swagger_view().with_ui('swagger', cache_timeout=1), name="docs"),
        # path('redoc/', get_swagger_view().with_ui('redoc', cache_timeout=1), name='redoc'),
    ]
