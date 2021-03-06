from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests,json
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, login, logout
from .models import Movies_List

page=1

def index(request):
    return HttpResponse(loader.get_template('Main.html').render({}, request))

def page_management(request):
    global page; page=int(request.POST.get('number', page)); action = request.POST.get("Page_num")
    if action =="Next" :
        page+=1
    elif action == "Previous" and page>1:
        page-=1
    return(page)

def Popular(request):
    page=page_management(request)
    param={'page':str(page)}
    Movies = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=6fe2c9251ad61629064389bb48013886",params=param).json()['results']
    template = loader.get_template('Grid.html')
    context = { 
        'Movies': Movies,
        'page' : page,
        'active1':'active',
    }
    return HttpResponse(template.render(context, request))


def searching(request):
    data = request.GET; action = data.get("search")
    if action != '': 
        page=page_management(request)
        param={'page':str(page),'query':action}
        Movies = requests.get("https://api.themoviedb.org/3/search/multi?api_key=6fe2c9251ad61629064389bb48013886",params=param).json()['results']
        template = loader.get_template('Grid.html')
        context = { 
            'Movies': Movies,
            'page' : page,
        }
        return HttpResponse(template.render(context, request))
    else :
        return HttpResponseRedirect(reverse('s_p'))

def Top_rated(request):
    page=page_management(request)
    param={'page':str(page)}
    Movies = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=6fe2c9251ad61629064389bb48013886",params=param).json()['results']
    template = loader.get_template('Grid.html')
    context = { 
        'Movies': Movies,
        'page' : page,
        'active2': 'active',
    }
    return HttpResponse(template.render(context, request))


def Contact(request):
    return HttpResponse(loader.get_template('contact.html').render({'active5':'active',}, request))

def Search_page(request):
    return HttpResponse(loader.get_template('Search_page.html').render({}, request))

def Movie(request):
    from random import shuffle
    data = request.GET
    print(request.POST)
    if bool(request.POST.get('Fav_button', False)):
        if not any([True for dic in Movies_List.objects.all().values()  if dic['movie']==int(data['id']) and dic['username_id'] == request.user.id]):
            Movies_List(movie=data['id'],username_id=request.user.id).save()
        else:
            Movies_List.objects.get(movie=int(data['id']),username_id=request.user.id).delete()

    id=data.get("id")
    page=page_management(request)
    param={'page':str(page)}
    template = loader.get_template('Movie.html')

    Fav ="favorited" if any([True for dic in Movies_List.objects.all().values()  if dic['movie']==int(id) and dic['username_id'] == request.user.id]) else ""

    Main_Movie = requests.get("https://api.themoviedb.org/3/movie/"+str(id)+"?api_key=6fe2c9251ad61629064389bb48013886").json()
    Trailers = requests.get("https://api.themoviedb.org/3/movie/"+str(id)+"/videos?api_key=6fe2c9251ad61629064389bb48013886").json()['results']
    video=Trailers[0]
    for Trailer in Trailers:
        if 'Main' in Trailer['name'] and 'Reaction' not in Trailer['name'] :
            video = Trailer
            break
        elif 'Trailer' in Trailer['name'] and 'HD' in Trailer['name'] and 'Reaction' not in Trailer['name'] :
            video = Trailer
            break
        elif 'Trailer' in Trailer['name'] and 'Reaction' not in Trailer['name'] :
            video = Trailer
            break

    List = requests.get("https://api.themoviedb.org/3/movie/"+str(id)+"/similar?api_key=6fe2c9251ad61629064389bb48013886",params=param).json()['results'];shuffle(List)
    context = { 
        'MM': Main_Movie,
        'Trailer': video,
        'List': List,
        'page' : page,
        'Fav':Fav,
    }
    return HttpResponse(template.render(context, request))

def Connect(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username'); password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                template = loader.get_template('redirecting.html')
                return HttpResponse(template.render({'back':-2, 'data':request.POST}, request))
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    template = loader.get_template('redirecting.html')
    return HttpResponse(template.render({"login_form":form, 'back':-1}, request))

def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return HttpResponseRedirect(reverse('index'))

def addUser(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            template = loader.get_template('Login.html')
            return HttpResponse(template.render({"register_form":form}, request))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    template = loader.get_template('Login.html')
    return HttpResponse(template.render({"register_form":form}, request))


def Reset(request):
    return HttpResponse(loader.get_template('Lost_pass.html').render({}, request))

def Return(request):
    from pathlib import Path
    file=open(str(Path(__file__).resolve().parent.parent)+'\\static\\txt\\password_reset_email.txt',"a")
    file.write(request.POST.get('email')); file.write("\n")
    file.close()
    return HttpResponseRedirect(reverse('index'))

def MyList(request,Movies=[]):
    page=page_management(request)
    List=Movies_List.objects.all().values()
    for dic in List[10*(page-1):10*page]:
        if dic["username_id"]==request.user.id:
            Movies.append(requests.get("https://api.themoviedb.org/3/movie/"+str(dic['movie'])+"?api_key=6fe2c9251ad61629064389bb48013886").json())
    template = loader.get_template('Grid.html')
    context = { 
        'Movies': Movies,
        'page' : page,
        'active3':'active',
    }
    return HttpResponse(template.render(context, request))

def Suggestions(request,Movies=[]):
    from random import shuffle,randint
    List=Movies_List.objects.all().values()
    for dic in List:
        if dic["username_id"]==request.user.id:
            param={'page':randint(1,30)}
            Similars_List=requests.get("https://api.themoviedb.org/3/movie/"+str(dic['movie'])+"/similar?api_key=6fe2c9251ad61629064389bb48013886",params=param).json()['results']
            for movie in Similars_List:
                if float(movie["vote_average"])>=7:
                    Movies.append(movie)
    shuffle(Movies)
    template = loader.get_template('Grid.html')
    context = { 
        'Movies': Movies[:20],
        'page' : page,
        'active4':'active', 
    }
    return HttpResponse(template.render(context, request))

def Contacting(request):
    from pathlib import Path
    file=open(str(Path(__file__).resolve().parent.parent)+'\\static\\txt\\Contact_msgs.txt',"a")
    for k,v in request.POST.items():
        file.write(f"{k} : {v} \n")
    file.write("---------------------------------------------------\n")
    file.close()
    messages.info(request,f"{request.POST['name']} we have received your message successfully, Thank you for contacting us. With love SMM's team")
    return HttpResponseRedirect(reverse('contact'))
