# defines view fns

# The django.shortcuts and django.http modules are part of the Django package 
# and are installed with Django when set up project's virtual env
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# class-based views are classes that create view fn objs containing pre-defined controller logic commonly used for basic CRUD ops
# main benefit is to provide convenience to developers
from .models import Cat, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import boto3  # for aws
import uuid 

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'catcollector-k'
0
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

@login_required # needs to log in to access below, similar to is_authenticated fn from before
# does NOT work on class-based view, use mixin, # line 139
def cats_index(request):
    # Cat is a model
    # user: a field on the Cat model that refers to the user who owns the cat
    # request.user is a built-in attr of Django's auth system, represents the currently logged-in user
    cats = Cat.objects.filter(user=request.user) # only show the logged in user's cats
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
# NOTE: url params are explicitly passed to view fns seperate from the req obj
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()

    # step 1) create a ls of toys the cat has
    cat_toys_ids = cat.toys.all().values_list('id') # gives a ls of toy ids belonging to a cat, e.g, [1, 5]
    # step 2) create a ls of toys the cat DOESN'T have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat_toys_ids) # field lookup, id in=>cat_toys_idss

    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,
    })

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
    # find the cat
    cat = Cat.objects.get(id=cat_id)
    # associate the toy
    cat.toys.add(toy_id) # accepts an obj. or pk(id) of obj.
    # redirect back to the detail pg
    return redirect('cats_detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
    # find the cat
    cat = Cat.objects.get(id=cat_id)
    # unassociate the toy
    cat.toys.remove(toy_id) # accepts an obj. or pk(id) of obj.
    # redirect back to the detail pg
    return redirect('cats_detail', cat_id=cat_id)

@login_required
def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys})

@login_required
def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', {'toy': toy})

def signup(request):
    # POST request
    error_message = '' # putting it here so that it can be overwritten if invalid in line 116
    if request.method == 'POST':
        # create a user in memory using the UserCreationForm(so that we can validate the form)
        form = UserCreationForm(request.POST)
        # check if the form inputs are valid
        if form.is_valid():
        # if valid: save new user to db as 'user'
            user = form.save()
            # login the new user    
            login(request, user)
            # redirect to the cats index pg
            return redirect('cats_index')
        # else: generate an error msg 'invalid input' 
        else: 
            error_message = 'Invalid sign up - try again' # line 116

    # GET request
        # send an empty form to the client
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form, 
        'error': error_message
    })

def add_photo(request, cat_id):
    # attempt to collect photo submission from request
    photo_file = request.FILES.get('photo-file', None) # FILES: dictionary
    # if photo file present
    if photo_file: 
        # setup a s3 client obj - obj w/methods for working with s3
        s3 = boto3.client('s3')
        # create a UNIQUE name for the photo file, uuid can help with this
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try to upload file to aws s3
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # generate a unique url for the img
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # save the url as a new instance of the photo model
            # NOTE: make sure to associate the cat with the photo model instance
            Photo.objects.create(url=url, cat_id=cat_id)
        # if exception(error)
        except Exception as error:
            # print erro msg for debugging
            print('photo upload failed')
            print(error)
    # redirect to the detail pg regardless if successful
    return redirect('cats_detail', cat_id=cat_id)

class CatCreate(LoginRequiredMixin, CreateView): # line 139
    model = Cat 
    # fields = ('name', 'breed', 'description')
    fields = ('name', 'breed', 'description', 'age') # '__all__'magic string: adds all the fields to the corresponding ModelForm
    template_name = 'cats/cat_form.html' # changing the path to the field
    # success_url = '/cats/' # redirect to /cats/ OPTION 2 in models.py

    def form_valid(self, form):# self: the instance of the view that is handling the form submission. form parameter contains the validated form data.
        
        # instance: instance that is created by this form
        # form.instance attr: the instance of the model that is being created or updated by the form
        form.instance.user = self.request.user # self.request.user: user that made the request to the view
        
        return super().form_valid(form)


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('description', 'age') 
    # tuples are preferred over list for the field attr
    # tuples are lightweight
    template_name = 'cats/cat_form.html'

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'
    template_name ='cats/cat_confirm_delete.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ('name', 'color')
    template_name = 'toys/toy_form.html'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'
    