"""AnyBid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AuctionApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),


    #Auth
    path('signup/',views.signupuser, name = 'signupuser'),
    path('login/',views.loginuser, name = 'loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    #App
    path('home/',views.home, name = 'home'),

    #AllAdds
     path('AllAdds/',views.AllAdds, name = 'AllAdds'),

     #MyAdds
     path('MyAdds/',views.MyAdds, name = 'MyAdds'),

     #PostAdds
     path('PostAdd/',views.PostAdd, name = 'PostAdd'),

     #Detail
     path('detail/<int:Add_id>', views.detail, name = 'detail'),
     path('detail/<int:Add_id>/Place_bid', views.Place_bid, name = 'Place_bid'),
     path('detail/<int:Add_id>/Delete_add', views.delete_add, name = 'delete_add'),
     ##
     path('detail/<int:Add_id>/prediction', views.prediction, name = 'prediction'),
     path('detail/<int:Add_id>/Acuprediction',views.Acuprediction, name = 'Acuprediction'),
     
     #profile
     path('MyProfile/', views.MyProfile, name = 'MyProfile'),
     path('UpdateProfile/',views.UpdateProfile, name = 'UpdateProfile'),
     path('bids/', views.bids, name = 'bids'),

     #bid winner
     path('winner/<int:Bid_id>', views.winner, name = 'winner'),
    
    #location based Adds

    path('LocationBased/',views.LocationBased, name = 'LocationBased'),

    #contact

    path('contact/',views.contact, name = 'contact'),

    #search
    path('search/',views.search, name = 'search'),

    

  


   


] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
