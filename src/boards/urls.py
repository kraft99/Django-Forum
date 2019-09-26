from django.urls import path
from . import views



app_name = 'boards'

urlpatterns = [
    # path('',
    # 	views.board_index,
    # 	name='board_index'),

    path('',
        views.BoardListView.as_view(),
        name='board_index'),
    
    # path('boards/<str:pk>/',
    # 	views.board_topics,
    # 	name='board_topics'),

    path('boards/<str:pk>/',
        views.BoardTopicsListView.as_view(),
        name='board_topics'),

    path('boards/<str:pk>/new/topic',
    	views.new_topic,
    	name='new_topic'),

    # path('boards/<str:board_pk>/topics/<str:topic_pk>/',
    # 	views.topic_posts_view,
    # 	name='topic_posts'),

    path('boards/<str:board_pk>/topics/<str:topic_pk>/',
        views.TopicPostListView.as_view(),
        name='topic_posts'),


    path('boards/<str:board_pk>/topics/<str:topic_pk>/reply/',
    	views.reply_topic,
    	name='reply_topic'),

    path('boards/<str:board_pk>/topics/<str:topic_pk>/posts/<str:post_pk>/edit/',
    	views.PostUpdateView.as_view(),
    	name='update_post'),

]
