from django.urls import  path


from apps.operations.views import AddFavView,CommentView

app_name='op'
urlpatterns=[
    path('fav/',AddFavView.as_view(),name='fav'),
    path('comment/',CommentView.as_view(),name='comment'),

]