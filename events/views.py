from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse

from events.models import Event, Participant
from events.forms import JoinForm, CreateEventForm
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render
from django.template.defaulttags import register
import calendar
from django.utils import timezone

class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event

    # Used to get from the 'groups' dictionary
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    # Converts a given month number to an abbreviation (eg. 8 = Aug)
    @register.filter
    def month_abbr(month_num):
        return calendar.month_abbr[int(month_num)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_participants = {}
        # Count how many users are in each event
        for e in Event.objects.all():
            grouped_participants[e] = (e.initial_size +
            len(Participant.objects.filter(event=e))-1)
        context.update({
            'events': Event.objects.filter(date__gte=timezone.now()).order_by('date', 'time'),
            'participants': Participant.objects.all(),
            'groups': grouped_participants
        })
        return context

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
            form.save(commit=True)
            return HttpResponseRedirect('/events')
        else:
            return render(request, 'events/create_event.html', {'form': form})
