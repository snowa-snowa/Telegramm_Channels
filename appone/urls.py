from django.urls import path
from . import views
from .views import SignupView, LoginView, LogoutConfirmationView

app_name = 'chat'

urlpatterns = [
    path('', views.conversations_list, name='conversations_list'),
    path('user/<str:username>/', views.open_conversation, name='open_conversation'),
    path('conversation/<int:convo_id>/', views.conversation_detail, name='conversation_detail'),

    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('message/edit/<int:message_id>/', views.edit_message, name='edit_message'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutConfirmationView.as_view(), name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('users/', views.users_list, name='users_list'),
    path('users/<str:username>/', views.user_detail, name='user_detail'),

    path('settings/', views.settings_view, name='settings'),
]
