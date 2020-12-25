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
from django.contrib import messages
from django.db.models import Q

#Machine Learning imports
import csv
from django.http import HttpResponse,HttpResponseRedirect
import joblib
import pandas as pd
import numpy as np
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
plt.style.use('bmh')
from array import *
import matplotlib
matplotlib.use('Agg')



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
                messages.success(request, 'User Registered Successfully.')
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
            messages.success(request, 'User Login Successfully.')
            return redirect('AllAdds')

#Home Function
def home(request):
    return render(request,'home.html')

#logout Function
@login_required
def logoutuser(request):
        logout(request)
        messages.success(request, 'User Logout Successfully.')
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
            messages.success(request, 'Profile Updated Successfully.')
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

#LocationBased function
@login_required
def search(request):

    if request.method == 'POST':

        if request.POST['search']:
            search_term = request.POST['search']
            search_item = Adds.objects.filter(Q(title__icontains=search_term)| Q(description__icontains=search_term))
           
    return render(request,'search.html', {'search_item':search_item})  

#Myadds function
@login_required
def MyAdds(request):
    myadd = Adds.objects.filter(user=request.user)
    return render(request,'MyAdds.html',{'myadd':myadd})  

#PostAuction Function
@login_required
def PostAdd(request):
    if request.method == 'POST':

        if request.POST['title'] and request.POST['Description'] and request.POST['Deu_Date'] and request.FILES['image'] and request.POST['Minimum_Bid']:

            add = Adds()
            add.title = request.POST['title']
            add.description = request.POST['Description']
            add.Due_date = request.POST['Deu_Date']
            add.image = request.FILES['image']
            add.bid_total = request.POST['Minimum_Bid']
            add.user = request.user
            add.save() 
           
            messages.success(request, 'Auction posted Successfully.')
            return redirect('/detail/' + str(add.id))
        else:
            return render(request, 'PostAdd.html',{'error':'All fields shuld be filled before the post Auction.'})
    else:
         return render(request,'PostAdd.html')  


#Detail Function
@login_required
def detail(request, Add_id):
    add = get_object_or_404(Adds, pk=Add_id) 
    pre_adds = Bids.objects.filter(Add_ID=Add_id).count()
    print(pre_adds)

    return render(request,'detail.html',{'Adds':add, 'pre_adds':pre_adds}) 

#Auction winner Function
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
                messages.success(request, 'Bid is updated Successfully.')
            else:
                messages.error(request, 'You Shuld Add Higher Bid.')
                return redirect('/detail/' + str(add.id))
                
            return redirect('/detail/' + str(add.id))
        else:
            return redirect('AllAdds')

#delete Function
@login_required
def delete_add(request, Add_id):
    if request.method == 'POST':
        add = get_object_or_404(Adds, pk=Add_id)
        add.delete()
        messages.success(request, 'Auction is deleted Successfully.')
        return redirect('MyAdds')

@login_required(login_url="loginuser")
def bids(request):
    bid = Bids.objects 
    return render(request,'AllAdds.html',{'bid':bid})  


#comment
def contact(request):
    return render(request,'contact.html')
    


#prediction Forecast
@login_required
def prediction(request , Add_id):
    pre_adds = Bids.objects.filter(Add_ID=Add_id)
    add = get_object_or_404(Adds, pk=Add_id) 

    
    test_list = []

    for test in pre_adds:
        test_list.append(test.Bid)
    

    df = pd.DataFrame({'Bid':test_list})

   # print(df)


    df = df[['Bid']]

    future_Bids = 10

    
    df['prediction'] = df[['Bid']].shift(-future_Bids)
    

    x = np.array(df.drop(['prediction'], 1))[:-future_Bids]

    y = np.array(df['prediction'])[:-future_Bids]

    x_train,x_test,y_train,y_test = train_test_split(x,y, test_size= 0.10)

    tree = DecisionTreeRegressor().fit(x_train,y_train)

    lr = LinearRegression().fit(x_train, y_train)

    x_future = df.drop(['prediction'], 1)
    x_future = x_future.tail(future_Bids)
   # print(x_future)
    x_future = np.array(x_future)
   # x_future
    

    lr_prediction = lr.predict(x_future)
    predict = pd.DataFrame({'Bid':lr_prediction})
    print(lr_prediction)

    predictions = lr_prediction

    plt.figure(figsize=(16,8))
    plt.title('Auction')
    plt.xlabel('Bid')
    plt.ylabel('Price US($)')
    plt.plot(predict['Bid'], 'y')
    plt.legend('prediction','y = yellow')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    return render(request,'prediction.html',{'data':uri, 'Adds':add}) 


#prediction Accuracy    
@login_required  
def Acuprediction(request , Add_id):
      
      acu_adds = Bids.objects.filter(Add_ID=Add_id)

      acu_adds = Bids.objects.filter(Add_ID=Add_id)

      test_list = []

      for test in acu_adds:
        test_list.append(test.Bid)

      df = pd.DataFrame({'Bid':test_list})

      df = df[['Bid']]

      future_Bids = 12

      df['prediction'] = df[['Bid']].shift(-future_Bids)

      x = np.array(df.drop(['prediction'], 1))[:-future_Bids]
      y = np.array(df['prediction'])[:-future_Bids]

      x_train,x_test,y_train,y_test = train_test_split(x,y, test_size= 0.10)

      

      lr = LinearRegression().fit(x_train, y_train)

      x_future = df.drop(['prediction'], 1)[:-future_Bids]
      x_future = x_future.tail(future_Bids)
      x_future = np.array(x_future)

      

      lr_prediction = lr.predict(x_future)

      predictions = lr_prediction

      valid = df[x.shape[0]:]
      valid['predictions'] = predictions
      plt.figure(figsize=(16,9))
      plt.title('Auction Accuracy')
      plt.xlabel('Date')
      plt.ylabel('Bid US($)')
      plt.plot(df['Bid'])
      plt.plot(valid[['Bid','predictions']])
      plt.legend(['original','valid','prediction'])
      fig = plt.gcf()
      buf = io.BytesIO()
      fig.savefig(buf,format='png')
      buf.seek(0)
      string = base64.b64encode(buf.read())
      uri1 =  urllib.parse.quote(string)
      


      return render(request,'Acuprediction.html',{'data1':uri1})  
     

    

    
    




