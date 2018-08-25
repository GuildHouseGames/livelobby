from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from events.models import Event, Participant
from events.forms import JoinForm
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
    success_url = '/events'

    def get_context_data(self, **kwargs):
        context = super(JoinView, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_initial(self):
        # Get initial gets run before get_context_data()
        # Raise a 404 if it does not exist
        try:
            self.event = Event.objects.get(pk=self.kwargs['event_id'])
        except Event.DoesNotExist:
            raise Http404("The event does not exist")
        return {'event': self.event}