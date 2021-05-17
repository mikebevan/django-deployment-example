from django.shortcuts import render

# Create your views here.
from basic_app.forms import UserForm, UserProfileInfoForm

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered= False

    if request.method=='POST':
        print("Inside POST")
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileInfoForm(data=request.POST)
        print("User valid: "+ str(user_form.is_valid()))
        print("Profile valid: "+ str(profile_form.is_valid()))

        if user_form.is_valid() and profile_form.is_valid():
            print(" Inside valid")
            user= user_form.save()
            user.set_password(user.password)  # to set hashing password
            user.save()
            print("User saved")

            profile = profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            else:
                print(user_form.errors, profile_form.errors)
            profile.save()
            registered = True
            print(" registered:"+ str(registered))
    else:
        user_form = UserForm()
        profile_form=UserProfileInfoForm()

    context_dict={'registered': registered, 'profileform':profile_form,'userform':user_form}
    return render(request,'basic_app/registeration.html',context_dict)


def user_login(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse(" Account not found, please register")
        else:

            print(" SOMEONE TRIED TO LOG IN WITH INVALID CREDENTIALS ")
            print("USERNAME {} and password {}".format(username,password))
            return HttpResponse(" INVALID USER CREDENTIALS")
    else:
        return render(request, 'basic_app/login.html')
