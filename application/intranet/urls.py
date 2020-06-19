"""intranet URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from projectsApp import views as projectsViews
from mainApp import views as mainViews
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static  #used to upload images

# Edit Admin Page
admin.site.site_header = 'Sistema de Gerenciamento de Projetos do DCC'
admin.site.site_title = 'Intranet DCC'
admin.site.index_title = 'Intranet DCC'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', mainViews.HomepageManage.as_view(), name='home'),

    # Projects stuff
    path('projectsApp/projects/', projectsViews.projectsListView.as_view(), name='projects'),
    path('projectsApp/projects/<int:pk>/delete', projectsViews.projectDeleteView.as_view(),name='delete_project'),
    path('projectsApp/projects/<int:pk>/edit', projectsViews.projectEditView.as_view(),
         name='edit_project'),
    path('projectsApp/projects/create', projectsViews.createProjectView.as_view(),
         name='create_project'),
    path('projectsApp/projects/delete_project_member/<int:pk>', projectsViews.delete_project_memberView.as_view(), name='delete_project_member'),
    path('projectsApp/projects/<int:project_pk>/add_project_member/<int:member_pk>', projectsViews.add_project_member, name='add_project_member'),
    path('projectsApp/projects/<int:project_pk>/add_selected_member', projectsViews.add_selected_member, name='add_selected_member'),

    # Profile stuff
    path('projectsApp/profile/', mainViews.profile, name='profile'),
    path('projectsApp/profilev/<int:pk>/edit', mainViews.pessoaEditView.as_view(),
         name='edit_profile'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
