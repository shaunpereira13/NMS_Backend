from django.urls import path
from .views import video_feed,video_feed1,run_subprocess1,run_subprocess2

urlpatterns = [
    # path('capture/', capture_and_send_size, name='capture_and_send_size'),
    path('video_feed/', video_feed, name='VideoCapture'),
    path('video_feed1/', video_feed1, name='VideoCapture'),
    path('aruco_model/', run_subprocess1, name='aruco_model'),
    path('refrence_model/', run_subprocess2, name='refrence _model'),
]
