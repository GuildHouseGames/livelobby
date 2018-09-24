from django.urls import path
from events.views import EventListView, EventView, JoinView, JoinConfirmationView, CreateEventView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list_view'),
    path('<int:pk>/', EventView.as_view(), name='event_view'),
    path('<int:event_id>/join/', JoinView.as_view(), name='join_view'),
    path('<int:pk>/confirm/', JoinConfirmationView.as_view(), name='join_confirmation_view'),
    path('create/', CreateEventView.as_view(), name='create_event_view'),
]
