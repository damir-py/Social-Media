from django.urls import path

from .views import (home_view, setting_view,
                    profile_view, login_view,
                    logout_view, register_view,
                    upload_view, like_view, follow_view, search_view, upload_author_view)

urlpatterns = [
    path('', home_view),
    path('setting/', setting_view),
    path('profile/<int:pk>/', profile_view),

    path('login/', login_view),
    path('logout/', logout_view),

    path('register/', register_view),
    path('upload/', upload_view),

    path('pic_upload/', upload_author_view),

    path('like/', like_view),

    path('follow/', follow_view),
    path('search/', search_view),

]

