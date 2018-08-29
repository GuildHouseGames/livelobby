from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse

from events.models import Event, Participant
from events.forms import JoinForm, CreateEventForm
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render

class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        # Sort the events by date ascending
        events_by_date = Event.objects.order_by('time')
        return events_by_date

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

class CreateEventView(CreateView):
    template_name = 'events/create_event.html'
    model = Event
    form_class = CreateEventForm
    success_url = '/events'

    def get_context_data(self, **kwargs):
        context = super(CreateEventView, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        form = CreateEventForm(request.POST)
        if (form.is_valid()):
            new_event = form.save(commit=True)

            # Create a new participant, who will be hosting this event
            host = Participant()
            host.name = request.POST['host']
            host.event = new_event
            host.type = "HOST"
            host.save()
            return HttpResponseRedirect('/events')
        else:
            return render(request, 'events/create_event.html', {'form': form})
