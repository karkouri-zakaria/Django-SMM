from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Popular/', views.Popular, name='popular'),
    path('searching/', views.searching, name='searching'),
    path('Top_rated/', views.Top_rated, name='top_rated'),
    path('Contact/', views.Contact, name='contact'),
    path('Search_page/', views.Search_page, name='s_p'),
    path('Movie/', views.Movie, name='movie'),
    path('Login/', views.addUser, name='addUser'),
    path('Login/Connect/', views.Connect, name='connect'),
    path('Logout/', views.Logout, name='logout'),
    path('Reset_password/', views.Reset, name='reset'),
    path('Return_password/', views.Return, name='back'),
    path('MyList/', views.MyList, name='mylist'),
    path('Suggestions/', views.Suggestions, name='suggestions'),
    path('Contacting/', views.Contacting, name='contacting'),
]

