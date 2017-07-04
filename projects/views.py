from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import WorkDiaryForm
from projects.models import (
                            Project,
                            ProjectAssignment,
                            WorkDiary,
                            WorkDiaryLog,
                        )
from accounts.models import Account
from management.models import Misc


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/projects.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.filter(projectassignment=request.user.id)
        assignment = ProjectAssignment.objects.filter(employee_id=request.user.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(assignment, 5)
        try:
            assignment = paginator.page(page)
        except PageNotAnInteger:
            assignment = paginator.page(1)
        except EmptyPage:
            assignment = paginator.page(paginator.num_pages)
        ctx_data = {
            'assignments': assignment,
            'projects': project,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/work_diary.html'

    def get(self, request, *args, **kwargs):
        form = WorkDiaryForm(initial={'project_assignment': kwargs['id']})
        project_assignment = ProjectAssignment.objects.get(id=kwargs['id'])
        works = WorkDiary.objects.filter(project_assignment=project_assignment).order_by('-date')
        query = request.GET.get('q')
        page = request.GET.get('page', 1)
        if query:
            works = works.filter(
                Q(finished_task__icontains=query)|
                Q(todo_task__icontains=query)|
                Q(issues__icontains=query)|
                Q(date__icontains=query)|
                Q(hours__icontains=query)
                ).distinct()
        paginator = Paginator(works, 5)
        try:
            works = paginator.page(page)
        except PageNotAnInteger:
            works = paginator.page(1)
        except EmptyPage:
            works = paginator.page(paginator.num_pages)
        ctx_data = {
            'form': form,
            'works': works,
            'project_assignment': project_assignment,
        }
        return render(self.request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = WorkDiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project:work-diary', id=kwargs['id'])
        ctx_data = {
            'form': form,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryEditView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/edit_work_diary.html'

    def get(self, request, *args, **kwargs):
        work_diary_id = kwargs['work_diary_id']
        project_assignment = ProjectAssignment.objects.get(id=kwargs['id'])
        works = WorkDiary.objects.get(id=work_diary_id, project_assignment=project_assignment)
        form = WorkDiaryForm(instance=works)
        ctx_data = {'form': form, 'works': works}
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        work_diary_id = kwargs['work_diary_id']
        project_assignment = ProjectAssignment.objects.get(id=kwargs['id'])
        works = WorkDiary.objects.get(id=work_diary_id, project_assignment=project_assignment)
        wd_history = WorkDiaryLog(work_diary=works, finished_task=works.finished_task, todo_task=works.todo_task, issues=works.issues, hours=works.hours)
        wd_history.save()
        form = WorkDiaryForm(request.POST, instance=works)
        if form.is_valid():
            form.save()
        return redirect('project:work-diary', id=kwargs['id'])


class WorkDiaryLogView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/work_diary_log.html'

    def get_context_data(self, *args, **kwargs):
        work_diary_id = kwargs['work_diary_id']
        work = WorkDiary.objects.get(id=work_diary_id)
        logs = WorkDiaryLog.objects.filter(work_diary__id=work_diary_id, work_diary__project_assignment__employee=self.request.user).order_by('-date_created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(logs, 10)
        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)
        kwargs['logs'] = logs
        kwargs['work'] = work
        return kwargs


class EmployeesMiscView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/employees_misc.html'

    def get(self, request, *args, **kwargs):
        employees = Account.objects.all().exclude(is_staff=True)
        miscs = Misc.objects.filter(employees=request.user, status=True)
        ctx_data = {'miscs': miscs}
        return render(request, self.template_name, ctx_data)
