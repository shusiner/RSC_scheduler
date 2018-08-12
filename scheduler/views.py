from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Guard, Manager, Site, User, Schedule
from django.contrib.auth.models import User
from .forms import NewGuardForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from .forms import GuardCreateForm, SiteCreateForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic

from django.urls import reverse_lazy
import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


@login_required
def home(request):
    """View function for home page of site."""

    

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html')

@login_required
def guard_profile(request, user):
    """ try:
        guard = Guard.objects.get(id=id)
    except Guard.DoesNotExist:
        raise Http404 """
    guard = get_object_or_404(Guard, user)
    
    return render(request, 'profile.html', {'guard': guard})

@login_required
def new_guard(request):

    if request.method == 'POST':
        form = NewGuardForm(request.POST)
        if form.is_valid():
            guard = form.save(commit=False)
            guard.save()
            guard = Guard.objects.create(
                name=form.cleaned_data.get('name'),
                age=form.cleaned_data.get('age'),
                position=form.cleaned_data.get('position'),
            )
            return redirect('home')  # TODO: redirect to the created topic page
    else:
            form = NewGuardForm()
    return render(request, 'new_guard.html', {'form': form})

"""         if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']

        user = User.objects.first()  # TODO: get the currently logged in user

        guard = Guard.objects.create(
            name=name,
            age=age,
        )

        return redirect('home')  # TODO: redirect to the home page

    return render(request, 'new_guard.html') """




class GuardView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'scheduler.manager_view'

    model = Guard
    
    context_object_name = 'guard_list'
    paginate_by = 4

class GuardDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'scheduler.manager_view'

    model = Guard

class GuardCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.manager_view'

    model = User
    form_class = GuardCreateForm
    template_name = 'scheduler\guard_create.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'guard'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('guard_create_done')

class GuardCreateDone(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.manager_view'

    model = User
    fields = []
    template_name = 'scheduler\guard_create_done.html'

class GuardUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'scheduler.manager_view'

    model = Guard
    fields = ['name', 'position', 'date_of_birth', 'site']

class GuardDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'scheduler.manager_view'

    model = Guard
    success_url = reverse_lazy('guard')

        


class SiteView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'scheduler.manager_view'

    model = Site    
    context_object_name = 'site_list'

class SiteDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'scheduler.manager_view'

    model = Site

        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['date_list'] = Schedule.objects.filter(guard=Guard.objects.first(), date__gte=datetime.date.today()).order_by('date')
        context['today'] = datetime.date.today()

        schedule_list = Schedule.objects.filter(guard=Guard.objects.first(), date__gte=datetime.date.today()).order_by('date')
        paginator = Paginator(schedule_list, 10)
        page = self.request.GET.get('page')
        contacts = paginator.get_page(page)
        context['contacts'] = contacts
        return context

class SiteCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.manager_view'

    model = Site
    fields = ['name', 'location']
    template_name = 'scheduler\site_create.html'

    def form_valid(self, form):
        form.save()
        return redirect('site_create_done')

class SiteCreateDone(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.manager_view'

    model = Site
    fields = []
    template_name = 'scheduler\site_create_done.html'
    
class SiteUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'scheduler.manager_view'

    model = Site
    fields = ['name', 'location']

class SiteDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'scheduler.manager_view'

    model = Site
    success_url = reverse_lazy('site')



class ScheduleView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'scheduler.guard_view'

    model = Schedule  
    paginate_by = 10  

    def get_queryset(self):
        return Schedule.objects.filter(guard=self.request.user.guard, date__gte=datetime.date.today()).order_by('date')

class ScheduleDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'scheduler.guard_view'

    model = Schedule

class ScheduleCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.guard_view'

    model = Schedule
    fields = ['date', 'is_day', 'is_night']
    template_name = 'scheduler\schedule_create.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.guard = user.guard
        form.save()
        return redirect('schedule_create_done')

class ScheduleCreateDone(PermissionRequiredMixin,CreateView):
    permission_required = 'scheduler.guard_view'

    model = Schedule
    fields = []
    template_name = 'scheduler\schedule_create_done.html'
    
class ScheduleUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'scheduler.guard_view'

    model = Schedule
    fields = ['date', 'is_day', 'is_night']
    success_url = reverse_lazy('schedule')

class ScheduleDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'scheduler.guard_view'

    model = Schedule
    success_url = reverse_lazy('schedule')



