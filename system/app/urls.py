from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path('index/',views.index,name='index'),
    path('details/<int:event_id>',views.details,name='details'),
    path('create/',views.create,name='create'),
    path('my-event/',views.my_event,name='my-event'),
    path('edit-event/<int:event_id>',views.edit_event,name='edit-event'),
    path('del-event/<int:event_id>',views.del_event,name='del-event'),
    path('my_profile/',views.my_profile,name='my_profile'),
    path('setting/',views.setting,name='setting'),
]
