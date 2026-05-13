from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('members/',views.MemberListView.as_view(), name='member-list'),
    path('members/create/',views.MemberCreateView.as_view(), name='member-create'),
    path('members/update/<int:pk>/',views.MemberUpdateView.as_view(), name='member-update'),
]
