from django.urls import path

from .views import HomepageView, change_name_view

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    # path('change/', change_name_view)
]