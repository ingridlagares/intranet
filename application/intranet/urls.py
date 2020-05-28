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
from projectsApp import views

# Edit Admin Page
admin.site.site_header = 'Sistema de Gerenciamento de Projetos do DCC'
admin.site.site_title = 'Intranet DCC'
admin.site.index_title = 'Intranet DCC'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),

    # Projects stuff
    path('projectsApp/projects/', views.projects, name='projects'),
    path('projectsApp/projects/<int:pk>/delete', views.delete_project,
         name='delete_project'),
    path('projectsApp/projects/<int:pk>/edit', views.edit_project,
         name='edit_project'),
    path('projectsApp/projects/create', views.create_project,
         name='create_project'),
    path('projectsApp/projects/<int:project_pk>/delete_project_member/<int:member_pk>', views.delete_project_member, name='delete_project_member'),
    path('projectsApp/projects/<int:project_pk>/add_project_member/<int:member_pk>', views.add_project_member, name='add_project_member'),
    path('projectsApp/projects/<int:project_pk>/add_selected_member', views.add_selected_member, name='add_selected_member'),
    # Profile stuff
    path('projectsApp/profile/', views.profile, name='profile'),
    path('projectsApp/profile/edit', views.edit_profile,
         name='edit_profile'),
]
