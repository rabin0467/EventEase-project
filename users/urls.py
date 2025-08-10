from django.urls import path
from users.views import sign_up,  sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list,delete_group, delete_participants, rsvp_dashboard
from users.views import CustomLoginView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView, ProfileView, EditProfileView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    # path('sign-in/',sign_in, name="sign-in"),
    path('sign-in/',CustomLoginView.as_view(), name="sign-in"),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/assign-role/<int:user_id>', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/delete-group/<int:group_id>/',delete_group, name='delete-group'),
    path('admin/delete-participant/<int:user_id>/', delete_participants, name='delete-participant'),
    path('user/rsvp-dashboard/', rsvp_dashboard, name='rsvp-dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePassword.as_view(template_name = 'accounts/password_change.html'), name='password-change'),
    path('password-changed/done/', PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')

]
