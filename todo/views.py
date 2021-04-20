from django.shortcuts import render, redirect
from django.views import generic
from .models import Todo
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class customerLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegistrationForm(generic.FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegistrationForm, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegistrationForm, self).get(*args, **kwargs)


class TodoView(LoginRequiredMixin, generic.ListView):
    model = Todo
    context_object_name = 'Tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tasks'] = context['Tasks'].filter(user=self.request.user)
        context['count'] = context['Tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['Tasks'] = context['Tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context


class TodoDetail(LoginRequiredMixin, generic.DetailView):
    model = Todo
    context_object_name = 'Detail'
    # template_name = 'todo/todo_detail.html'


class TodoCreate(LoginRequiredMixin, generic.CreateView):
    model = Todo
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)


class TodoUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Todo
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Todo
    context_object_name = "Detail"
    success_url = reverse_lazy('tasks')
