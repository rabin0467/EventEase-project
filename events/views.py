from django.shortcuts import render, redirect, HttpResponse
from datetime import date, timedelta
from django.db.models import Q, Count
from events.models import Event, Category
from events.forms import EventModelForm, CategoryModelForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
# from django.contrib.auth.models import User
from users.views import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

def is_adminOrManager(user):
    return (user.groups.filter(name='Admin').exists() or 
            user.groups.filter(name='Organizer').exists()
    )

def organizer_view(request):
    is_organizer = request.user.groups.filter(name='Organizer').exists()
    return render(request,'loged_nav.html', {'is_organizer': is_organizer})


@method_decorator(login_required, name='dispatch')
class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'event/event_list.html'

    def get_queryset(self):
        type = self.request.GET.get('type', 'ongoing')

        base_query = Event.objects.select_related("category").prefetch_related("rsvp_participants")
        if type=="upcoming":
            events = base_query.filter(date__gt=date.today())
        elif type == "completed":
            events= base_query.filter(date__lt=date.today())
        elif type == "ongoing":
            events = base_query.filter(date = date.today())
        elif type == "all":
            events = base_query.all()
        
        query = self.request.GET.get('query')
        if query:
            events = base_query.filter(Q(name__icontains=query) | Q(location__icontains=query))

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            events = base_query.filter(date__gt=start_date,date__lt=end_date)

        return events

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        counts = Event.objects.aggregate(
            total_participants = Count("rsvp_participants", distinct=True),
            total_event = Count('id', distinct=True),
            upcoming_event = Count('id', distinct=True, filter=Q(date__gt=date.today())),
            completed_event = Count('id', distinct=True, filter=Q(date__lt=date.today())),
            on_going_event = Count('id', distinct=True ,filter=Q(date=date.today()))
        )

        context['counts']= counts
        context['type']= self.request.GET.get('type', 'ongoing')
        context['categories']= Category.objects.all()
        context['query']= self.request.GET.get('query')
        context['start_date']= self.request.GET.get('start_date')
        context['end_date']= self.request.GET.get('end_date')

        return context

        


@user_passes_test(is_adminOrManager, login_url='no-permission')
def participants_list(request):
    rsvp_users = User.objects.filter(rsvp_events__isnull=False).distinct()

    return render(request, 'events/participants.html', {'users': rsvp_users})


@login_required
def event_details(request, event_id):
    event = Event.objects.prefetch_related('rsvp_participants').get(id=event_id)


    return render(request, 'events/event_details.html', {'event': event})

@login_required
def events_by_category(request):
    categories = Category.objects.prefetch_related('events')
    return render(request, 'events/events_by_category.html', { 'categories': categories})




@method_decorator(user_passes_test(is_adminOrManager, login_url='no-permission'), name='dispatch')
class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'events/create_category.html'
    success_url = reverse_lazy('events-by-category')

    def form_valid(self, form):
        messages.success(self.request, 'Category created succesfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong')
        return super().form_invalid(form)
        



@method_decorator(user_passes_test(is_adminOrManager, login_url='no-permission'), name='dispatch')
class UpdateCategoryView(UpdateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'events/create_category.html'
    success_url = reverse_lazy('events-by-category')
    pk_url_kwarg = 'category_id'

    def form_valid(self, form):
        response =  super().form_valid(form)
        messages.success(self.request, 'Category updated succesfully')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong')
        return super().form_invalid(form)

@login_required
@user_passes_test(is_adminOrManager, login_url='no-permission')
def category_details(request, cat_id):
    category = Category.objects.prefetch_related('events').get(id=cat_id)

    return render(request, 'events/category_details.html', {'category': category})



@user_passes_test(is_adminOrManager, login_url='no-permission')
def delete_category(request,cat_id):
    category = Category.objects.get(id=cat_id)

    if request.method == 'POST':
        cat_name = category.name
        category.delete()
        messages.success(request, f'{cat_name} deleted succesfully')
        return redirect('events-by-category')
    
    return render(request, 'events/delete_category.html', {'category':category})


@method_decorator(user_passes_test(is_adminOrManager, login_url='no-permission'), name='dispatch')
class CreateEventView(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong')
        return super().form_invalid(form)



@method_decorator(user_passes_test(is_adminOrManager, login_url='no-permission'), name='dispatch')
class UpdateEventView(UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'events/update_event.html'
    success_url = reverse_lazy('event-list')
    pk_url_kwarg = 'event_id'

    def form_valid(self, form):
        response =  super().form_valid(form)
        messages.success(self.request, 'Event updated successfully')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong')
        return super().form_invalid(form)

@user_passes_test(is_adminOrManager, login_url='no-permission')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'{event_name} deleted succesfully')
        return redirect('event-list')
    
    return render(request, 'events/delete_event.html', {'event':event})

def rsvp_event(request, event_id):
    event = Event.objects.get(id = event_id)
    user = request.user

    if user in event.rsvp_participants.all():
        messages.info(request, 'You have already joined to this event')
        return redirect("rsvp-dashboard")
    else:
        event.rsvp_participants.add(user)
        messages.success(request, 'RSVP successful ! A confirmation email sent')
    return redirect("rsvp-dashboard")

def rsvp_activation_mail(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')

@user_passes_test(is_adminOrManager, login_url='no-permission')
def organizer_dashboard(request):
    categories = Category.objects.prefetch_related('events__rsvp_participants')
    events = Event.objects.select_related('category').prefetch_related('rsvp_participants')

    context={
        'categories': categories,
        'events': events
    }
    return render(request, 'organizer/organizer_dashboard.html', context)
    


def navbar(request):
    return render(request, "navbar.html")
