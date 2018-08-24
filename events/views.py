from events.models import Event, Participant
from events.forms import JoinForm
from  django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event

class EventView(DetailView):
    template_name = 'events/event.html'
    model = Event

class JoinView(CreateView):
    template_name = 'events/join_event.html'
    model = Participant
    form_class = JoinForm

    def get_success_url(self):
        return reverse('event_view', kwargs={'pk':self.kwargs['event_id']})

    def get_initial(self):
        return {'event': Event.objects.get(pk=self.kwargs['event_id'])}