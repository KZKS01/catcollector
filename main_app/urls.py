from django.urls import path # define URL patterns for Django app
from . import views # from the current folder, import views
# contains the view fns that will be associated with each URL pattern

# NOTE: django ONLY uses GET & POST; no REST in django, never do DELETE, PUT
# NOTE: updating & deleting will be conducted using POST request

urlpatterns = [
    path('', views.home, name='home'),
    # add another path to about/ here and connect it to views.about view fn
    path('about/', views.about, name='about'),
    # NOTE: djangho paths NEVER begin with "/"; django prepends this automatically
    path('cats/', views.cats_index, name='cats_index'),
    path('cats/<int:cat_id>/', views.cats_detail, name='cats_detail'), 
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'), # ToyCreate is a class-based view,convert the view class into an actual view fn that can be used in a URL pattern, so as_view()
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
    path('toys/', views.toys_index, name='toys_index'),
    path('toys/<int:toy_id>/', views.toys_detail, name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy_delete'),
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('cats/<int:cat_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('accounts/signup/', views.signup, name='signup'),
]