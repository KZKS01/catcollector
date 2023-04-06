# The django.shortcuts and django.http modules are part of the Django package 
# and are installed with Django when set up project's virtual env
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# class-based views are classes that create view fn objs containing pre-defined controller logic commonly used for basic CRUD ops
# main benefit is to provide convenience to developers
from .models import Cat, Toy
from .forms import FeedingForm


# dummy cat data for prototyping
# class Cat: 
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Mr. Worms', 'Russian Blue', 'A very shy cat', 12),
#     Cat('Mr. Kitty', 'Russian Blue', 'A very outgoing cat', 12),
#     Cat('Iris', 'Russian Blue', 'Can be mean sometimes', 8),
# ]

# use this file to define controller logic
# NOTE: each controller is defined using either a fn or a class
# NOTE: all views fn take at least 1 required positional arg: request

def home(request):
    # NOTE: responses are returned from view function
    # return HttpResponse('Hello World')
    return render(request, 'home.html') #passing the path that happens to be a folder 'home.html'

def about(request):
    # return HttpResponse('<h1>About the CatCollector</h1>')
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all() # Cat is a model
    return render(request, 'cats/index.html', {'cats': cats})

# NOTE: url params are explicitly passed to view fns seperate from the req obj
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form
    })

def add_feeding(request, cat_id):
    # create a new model instance of feeding
    form = FeedingForm(request.POST) # FeedingForm()creates a model form obj; request.POST is kindof like req.body in express
    # {'meal': 'B', date: X, cat_id: None}

    # validate user input provided from form submission
    if form.is_valid(): 
        new_feeding = form.save(commit=False) # create an in-memory instance w/o saving to the db
        new_feeding.cat_id = cat_id # attach the associated cat's id to the cat_id attr
        new_feeding.save()
    # as long as form is valid, we can associate the related cat to the new feeding
    # return a redirect response to the client
    return redirect('cats_detail', cat_id=cat_id)

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys})

def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', {'toy': toy})

class CatCreate(CreateView):
    model = Cat 
    # fields = ('name', 'breed', 'description')
    fields = '__all__' # magic string: adds all the fields to the corresponding ModelForm
    template_name = 'cats/cat_form.html' # changing the path to the field
    # success_url = '/cats/' # redirect to /cats/ OPTION 2 in models.py

class CatUpdate(UpdateView):
    model = Cat
    fields = ('description', 'age') 
    # tuples are preferred over list for the field attr
    # tuples are lightweight
    template_name = 'cats/cat_form.html'

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
    template_name ='cats/cat_confirm_delete.html'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ('name', 'color')
    template_name = 'toys/toy_form.html'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'
    