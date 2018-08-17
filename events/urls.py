from django.urls import path
from events.views import EventListView, EventView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list_view'),
    path('<int:pk>/', EventView.as_view(), name='event_view')
]