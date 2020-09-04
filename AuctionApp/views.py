from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Adds,Bids
from .models import UserProfile
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from datetime import timedelta, date

#Signup function
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('AllAdds')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

#Login function
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('AllAdds')

#Home Function
def home(request):
    return render(request,'home.html')

#logout Function
@login_required
def logoutuser(request):
        logout(request)
        return redirect('loginuser')

#AllAdds Function

@login_required(login_url="loginuser")
def AllAdds(request):
    add = Adds.objects
    return render(request,'AllAdds.html',{'add':add})  

#profile Function
@login_required
def MyProfile(request):
    pro = UserProfile.objects  
    return render(request,'MyProfile.html',{'pro':pro})
    


#UpdateProfile Function
@login_required
def UpdateProfile(request):
    if request.method == 'POST':

        if request.POST['Self_description'] and request.POST['Contact'] and request.POST['Address'] and request.POST['latitude'] and request.POST['logitude'] and request.POST['Zipcode']:

            pro = UserProfile()
            pro.Self_description = request.POST['Self_description']
            pro.Contact = request.POST['Contact']
            pro.Zipcode = request.POST['Zipcode']
            pro.Address = request.POST['Address']
            pro.latitiude = request.POST['latitude']
            pro.logitude = request.POST['logitude']
            pro.user = request.user
            pro.save()
            return redirect('MyProfile')
        else:
            return render(request, 'UpdateProfile.html',{'error':'All fields shuld be filled before the Update the profile add.'})
    else:
         return render(request,'UpdateProfile.html')  

#LocationBased function
@login_required
def LocationBased(request):
    lmyadd = Adds.objects
    return render(request,'LocationBased.html',{'lmyadd':lmyadd})  


#Myadds function
@login_required
def MyAdds(request):
    myadd = Adds.objects.filter(user=request.user)
    return render(request,'MyAdds.html',{'myadd':myadd})  

#Postadd Function
@login_required
def PostAdd(request):
    if request.method == 'POST':

        if request.POST['title'] and request.POST['Description'] and request.POST['Deu_Date'] and request.FILES['image'] and request.POST['Minimum_Bid']:

            add = Adds()
            bid = Bids()
            add.title = request.POST['title']
            add.description = request.POST['Description']
            add.Due_date = request.POST['Deu_Date']
            add.image = request.FILES['image']
            add.bid_total = request.POST['Minimum_Bid']
            bid.Add_ID = str(add.id)
            bid.Title = request.POST['title']
            bid.Bid = request.POST['Minimum_Bid']
            bid.user = request.user
            add.user = request.user
            add.save()
            bid.save()
            return redirect('/detail/' + str(add.id))
        else:
            return render(request, 'PostAdd.html',{'error':'All fields shuld be filled before the post add.'})
    else:
         return render(request,'PostAdd.html')  


#Detail Function
@login_required
def detail(request, Add_id):
    add = get_object_or_404(Adds, pk=Add_id)  
    return render(request,'detail.html',{'Adds':add}) 

#Detail Function
@login_required
def winner(request, Bid_id):
    highest_bid = Bids.objects.filter(Add_ID=Bid_id).order_by('-Bid').first()
    winner = highest_bid.user.userprofile
    
    return render(request,'winner.html',{'winner':winner}) 





#Bid Function
@login_required
def Place_bid(request, Add_id):
    if request.method == 'POST':
        if request.POST['bid_total']:
            bid = Bids()
            add = get_object_or_404(Adds, pk=Add_id)

            new =int(request.POST['bid_total'])
            old =int(add.bid_total)
             
            if (new > old):
                add.bid_total= request.POST['bid_total']
                bid.Add_ID = str(add.id)
                bid.Bid = request.POST['bid_total']
                bid.Title = add.title
                bid.user = request.user
                add.save()
                bid.save()
            else:
                return redirect('/detail/' + str(add.id),{'error':'All fields shuld be filled before the post add.'})
                
            return redirect('/detail/' + str(add.id))
        else:
            return redirect('AllAdds')

#delete Function
@login_required
def delete_add(request, Add_id):
    if request.method == 'POST':
        add = get_object_or_404(Adds, pk=Add_id)
        add.delete()
        return redirect('MyAdds')

@login_required(login_url="loginuser")
def bids(request):
    bid = Bids.objects 
    return render(request,'AllAdds.html',{'bid':bid})  

#Contact

def contact(request):
    return render(request,'contact.html')
    
@login_required
def prediction(request):
    return render(request,'prediction.html')
