from events.models import Event
from django.views.generic import DetailView, ListView

class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventView(DetailView):
    template_name = 'events/event.html'
    model = Event
