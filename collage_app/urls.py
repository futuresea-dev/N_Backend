from django.urls import path, include
from collage_app import views
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'serie', views.SeriedToken)
router.register(r'serie/add', views.TokenAddSet)
router.register(r'serie/random', views.TokenRandomGet, basename="random")
router.register(r'serie/update', views.TokenUpdateSet, basename="update")
router.register(r'serie/get_collections', views.CollectionsGet)
router.register(r'serie/get_tokens', views.TokensGet)
router.register(r'check', views.UserCheckGet)
urlpatterns = router.urls

urlpatterns += [
    path('main-page/', views.TokenList.as_view(), name='home')
]