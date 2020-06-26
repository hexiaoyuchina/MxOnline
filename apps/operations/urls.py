from django.urls import  path


from apps.operations.views import AddFavView

app_name='op'
urlpatterns=[
    path('fav/',AddFavView.as_view(),name='fav'),

]