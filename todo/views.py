# general app imports
from telnetlib import STATUS
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy

# todo app imports
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

# todo classes imports
from .models import Task
from .forms import TaskFormFast

# folders imports
from folders.models import Folder


#region main


# Renders the index
class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return get_context(self.request, context)


# Returns Index / TaskList context: the tasks, folders, current folder, search input, task create form
def get_context(req, context):

    try:
        user = req.user

        # if context already contains 'tasks', update the list
        # otherwise, create the list
        if 'tasks' in context:
            context['tasks'] = context['tasks'].filter(user=user)
        else:
            context.update({'tasks': Task.objects.filter(user=user)})

        user_folders = Folder.objects.filter(user=user)
    except:
        context['tasks'] = list()
        user_folders = list()

    # get the user's folders
    context.update({'folders': user_folders})

    allow_move_btn = True if len(user_folders) > 0 else False

    print(allow_move_btn)

    # set the bool 'allow_move_btn' to true if Users has more than one folder 
    context.update({'allow_move_btn': allow_move_btn})

    # initialize folder variable
    folder = None

    # if session contains a folder pk, get the folder object as 'folder'
    # otherwise, there is no current folder, just leave 'folder' as None
    if 'current_folder' in req.session:
        session_folder = req.session['current_folder']
        try:
            folder = Folder.objects.all().get(pk=session_folder)
        except Folder.DoesNotExist:
            folder = None
            req.session['current_folder'] = -1

    # if there's a current folder parameter in context, set its value
    # otherwise, add the parameter to context and set its value
    if 'current_folder' in context:
        context['current_folder'] = folder
    else:
        context.update({'current_folder': folder})

    # finally, if the folder is not None, set 'tasks' in the context as the folder's tasks only
    if folder is not None:
        context['tasks'] = context['tasks'].filter(folder=folder)

    # get the search input if any
    search_input = req.GET.get('search-area') or ''
    # if search input is present, filter the tasks by its text
    if search_input:
        context['tasks'] = context['tasks'].filter(title__icontains=search_input)

    # update the search input context
    context['search_input'] = search_input

    # pass the TaskForm as context
    context['fast_form'] = TaskFormFast()

    context.update({'theme': req.session['theme'] if 'theme' in req.session else 'light'})

    return context


# Returns a render of the Task List with updated context
def tasks(req):
    print(f'tasks() -- {req.session["sel_tasks"]}')
    return render(req, 'todo/task_list.html', get_context(req, {}))


#endregion


#region old CBV


# old: CBV to see Task's details
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


# old: CBV to update tasks
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('index')


#endregion


#region main Task actions


# Create a new Task
def t_new(req):

    task_title = req.POST.get('title')

    if len(task_title) < 1: return render(req, 'todo/task_list.html', get_context(req, {'tasks': Task.objects.filter(user=req.user)}))

    # Initialize a folder reference
    folder = None

    # Checks if there's a current folder in the user's session
    if 'current_folder' in req.session and req.session['current_folder'] >= 0:

        # Try to assign the current folder to the local reference
        try:
            folder = Folder.objects.get(pk=req.session['current_folder'])

        # Ignore if None found and continue with the call
        except Folder.DoesNotExist:
            pass

        # Log with target folder name
        print("new task in folder: " + folder.folder_name)

    # No folder in session
    else:
        print("new uncategorized task")

    # Create the Task with the folder 'folder'
    Task.objects.create(user=req.user, title=task_title, folder=folder)

    # Return the updated Task List to be swapped in by HTMX
    return render(req, 'todo/task_list.html', get_context(req, {'tasks': Task.objects.filter(user=req.user)}))


# Checks / Unchecks the Task as complete
def t_complete(req, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    task.completed = not task.completed
    task.save()
    return HttpResponse(status=200)
    # return render(req, 'todo/task_list_item.html', {'task':task})


# Moves the Task to a Folder
def t_move (req, pk, pk2=-1):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    if pk2 < 0:
        folder = None
    else:
        try:
            folder = Folder.objects.get(pk=pk2)
        except Folder.DoesNotExist:
            return HttpResponse(status=404)
    task.folder = folder
    task.save()
    # req.session['sel_tasks'].remove(pk)
    req.session['sel_tasks'] = []       # TODO !!!! bandaid fix
    return render(req, 'todo/task_list.html', get_context(req, {}))


# Deletes a Task
def t_del(req, pk):
    Task.objects.get(pk=pk).delete()
    if 'sel_tasks' in req.session and pk in req.session['sel_tasks']: 
        print(f'req.session["sel_tasks"]: {req.session["sel_tasks"]} contains {pk}')
        # req.session['sel_tasks'].remove(pk)
        req.session['sel_tasks'] = []       # TODO !!!! bandaid fix
        print(f'req.session["sel_tasks"]: {req.session["sel_tasks"]} removed {pk}')
    else: print(f'req.session["sel_tasks"] does NOT contain {pk}')
    return tasks(req)



#endregion


#region Select


# Selects / Unselects a Task, overwriting any selected tasks with the newly selected task
def t_sel(req, pk):

    # try to get task from pk
    try:
        Task.objects.get(pk=pk)

    # no task found
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    # initialize session 'sel_tasks' with sel_task if list is not in session yet
    if 'sel_tasks' not in req.session or pk not in list(req.session['sel_tasks']):
        req.session['sel_tasks'] = list({pk})
        print(f"task {pk} selected")
        return HttpResponse(status=201)

    print(f"task {pk} deselected")
    req.session['sel_tasks'] = list({})

    return HttpResponse(status=201)


# Selects / Unselects a Task incrementally with previously selected Tasks
def t_sel_multi(req, pk):

    # try to get task from pk
    try:
        Task.objects.get(pk=pk)

    # no task found
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    # initialize session 'sel_tasks' with sel_task if list is not in session yet
    if 'sel_tasks' not in req.session:
        req.session['sel_tasks'] = list({pk})
        return HttpResponse(status=201)

    # reference the list locally
    session_tasks = req.session['sel_tasks']

    # select sel_task if not selected yet
    if pk not in session_tasks:
        session_tasks.append(pk)

    # otherwise, deselect it
    else:
        session_tasks.remove(pk)

    # replace the list
    req.session['sel_tasks'] = list(session_tasks)

    for task in session_tasks:
        print(task)

    return HttpResponse(status=201)


#endregion


#region selected Task actions

def t_sel_actions (req):
    if 'sel_tasks' in req.session and len(req.session['sel_tasks']) > 0: 
        return render(req, 'todo/sel_actions.html', {})
    return render(req, 'todo/sel_actions_none.html', {})

def t_sel_all(req):
    
    if 'sel_tasks' not in req.session:
        req.session.update({'sel_tasks': []})
        return HttpResponse(status=201)
        # return f_reload(req)

    if len(req.session['sel_tasks']) > 0:
        req.session['sel_tasks'] = []
        return HttpResponse(status=201)
        # return f_reload(req)

    try:
        tasks = Task.objects.filter(folder=Folder.objects.get(pk=req.session['current_folder']))
    except:
        tasks = Task.objects.filter(user=req.user)

    # print(f'tasks: {list(tasks)}')
    lst = [t.pk for t in list(tasks)]

    req.session['sel_tasks'] = lst

    return HttpResponse(status=200)
    # return f_reload(req)

# Checks / Unchecks the selected Tasks' "complete"
def t_sel_complete (req):
    if 'sel_tasks' in req.session:
        tasks = [Task.objects.get(pk=pk) for pk in req.session['sel_tasks']]
        complete = False
        for task in tasks:
            if not task.completed: complete = True
        print(f'should complete? {complete}')
        for task in tasks:
            task.completed = complete
            task.save()
    return render(req, 'todo/task_list.html', get_context(req, {}))


# Deletes the selected Tasks
def t_sel_del (req):
    if 'sel_tasks' in req.session:
        for pk in req.session['sel_tasks']:
            Task.objects.get(pk=pk).delete()
        req.session['sel_del'] = []
    return render(req, 'todo/task_list.html', get_context(req, {}))


def t_sel_move (req, pk=-1):
    if pk < 0:
        folder = None
    else:
        try:
            folder = Folder.objects.get(pk=pk)
        except Folder.DoesNotExist:
            return HttpResponse(status=404)
    if 'sel_tasks' not in req.session or len(list(req.session['sel_tasks'])) < 1:
        return HttpResponse(status=201)
    task_pks = list(req.session['sel_tasks'])
    print(task_pks)
    for task_pk in task_pks:
        print(task_pk)
        task = Task.objects.get(pk=task_pk)
        task.folder = folder
        task.save()
    req.session['sel_tasks'] = []
    return render(req, 'todo/task_list.html', get_context(req, {}))


#endregion


#region modals


# Opens the modal to move a Task to a Folder
def move_modal(req, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    return render(req, 'todo/modals/move_modal.html', {'folders':Folder.objects.filter(user=req.user), 'target_task':task})


def sel_move_modal(req):
    return render(req, 'todo/modals/sel_move_modal.html', {'folders':Folder.objects.filter(user=req.user)})

def t_sel_super_update(req):
    return render(req, 'todo/sel_tasks_super_updater.html', {})

#endregion
