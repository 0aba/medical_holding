from main.views import http404_page
from django.urls import path
from . import views


urlpatterns=[
    path('', views.Home.as_view(), name='home'),
    path('login/', views.MyLoginView.as_view(), name='log_in'),
    path('signup/', views.SignupView.as_view(), name='sign_up'),
    path('logout/', views.logout_page, name='log_out'),

    path('profile/user/<slug:username>/', views.ProfileUserView.as_view(), name='profile_user'),
    path('profile/user/<slug:username>/change/', views.ChangeProfileUserView.as_view(), name='change_profile_user'),
    path('ban/user/<slug:username>/', views.ban_user, name='ban_user'),
    path('unban/user/<slug:username>/', views.unban_user, name='unban_user'),

    path('organization/', views.OrganizationRouter.as_view(), name='router_organization'),
    path('organization/new/', views.RegisterOrganizationView.as_view(), name='new_organization'),
    path('profile/organization/<int:pk>/', views.OrganizationProfileView.as_view(), name='profile_organization'),
    path('profile/organization/<int:pk>/change/',
       views.ChangeProfileOrganizationView.as_view(), name='profile_organization_change'),

    path('profile/organization/<int:pk>/branch/',
         views.OrganizationBranchListView.as_view(), name='organization_branch_list'),
    path('profile/organization/<int:pk>/branch/new/',
         views.CreateBranchOrganizationView.as_view(), name='organization_branch_new'),
    path('profile/organization/<int:pk>/branch/<int:pk_branch>/change/',
         views.UpdateBranchOrganizationView.as_view(), name='organization_branch_change'),
    path('profile/organization/<int:pk>/branch/<int:pk_branch>/delete/',
         views.delete_organization_branch, name='organization_branch_delete'),

    path('profile/organization/<int:pk>/employee/',
         views.OrganizationEmployeeListView.as_view(), name='organization_employee_list'),
    path('profile/organization/<int:pk>/employee/new/',
         views.CreateEmployeeOrganizationView.as_view(), name='organization_employee_new'),
    path('profile/organization/<int:pk>/employee/<int:pk_employee>/change/',
         views.UpdateEmployeeOrganizationView.as_view(), name='organization_employee_change'),
    path('profile/organization/<int:pk>/employee/<int:pk_employee>/delete/',
         views.delete_organization_employee, name='organization_employee_delete'),

    path('services/', views.ServicesListView.as_view(), name='services_list'),
    path('services/new/', views.CreateServicesView.as_view(), name='services_new'),
    path('services/<int:pk>/', views.ServicesView.as_view(), name='services_view'),
    path('services/<int:pk>/change/',
         views.UpdateServicesView.as_view(), name='services_change'),
    path('services/<int:pk>/delete/',
         views.delete_organization_service, name='service_delete'),
    path('services/<int:pk>/grage/<int:pk_grade>/delete/', views.delete_grade_service , name='delete_rating'),
    path('services/organization/',
       views.OrganizationAppointmentListView.as_view(), name='appointment_organization'),

    path('services/comment/<int:pk>/delete/', views.delete_comment_service, name='delete_comment'),
    path('services/comment/<int:pk>/change/', views.ChangeCommentServicesView.as_view(), name='change_comment'),
]

handler404 = http404_page
