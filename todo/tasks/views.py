from django import contrib
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
@login_required
def tasksList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = Task.objects.filter(done='done', update_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    taskDone = Task.objects.filter(done='done', user=request.user).count()
    taskDoing = Task.objects.filter(done='doing', user=request.user).count()

    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
   
    elif filter:

        tasks = Task.objects.filter(done=filter, user=request.user)

    else:
        task_list = Task.objects.all().order_by ('-created_at').filter(user=request.user)
        paginator = Paginator(task_list,3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request, 'tasks/list.html', {'tasks': tasks,'tasksrecently': tasksDoneRecently,  'taskDone': taskDone,'taskDoing': taskDoing} ) #Criando template django
@login_required
def taskView (request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})
@login_required
def newTask (request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.done = 'doing'
            task.save()
            messages.info(request, "Tafera criada com sucesso!")
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html',{'form':form} )
@login_required
def editTask (request, id):
    task = get_object_or_404(Task, pk=id) 
    form = TaskForm(instance=task)

    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            messages.info(request, "Tafera alterada com sucesso!")
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.tml', {'form' :form , 'task': task } )    

    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task })

@login_required
def deleteTask (request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()

    messages.info(request, "Tafera deletada com sucesso!")
    return redirect('/')

def helloworld(request):
    return HttpResponse('Hello World')


def yourName(request, name):
    return render(request,'tasks/yourname.html',{'name':name})


@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done ='doing'
    task.save()
    return redirect('/')        