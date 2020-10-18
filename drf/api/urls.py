from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
gv_router = DefaultRouter()
mv_router = DefaultRouter()

router.register(r'post', views.PostAPIViewsets, basename='post')
gv_router.register(r'gv-post', views.PostAPIGenericViewsets, basename='gv_post')
mv_router.register(r'mv-post', views.PostAPIGenericViewsets, basename='mv_post')

urlpatterns = [

    # model viewsets and routers
    path('mv/', include(mv_router.urls)),

    # generic viewsets and routers
    path('gv/', include(gv_router.urls)),

    # viewsets and routers
    path('viewsets/', include(router.urls)),
    path('viewsets/<int:id>', include(router.urls)),

    # class-based view
    path('cbv/post/', views.PostAPI.as_view()),
    path('cbv/detail/<int:id>/', views.PostDetailAPI.as_view()),

    # generic API view
    path('gv/post/<int:id>/', views.PostGenericAPIView.as_view()),

    path('list/', views.postList, name="post_list"),
    path('add/', views.addPost, name="add_post"),
    path('detail/<int:id>/', views.detail, name="detail"),
]