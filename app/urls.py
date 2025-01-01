from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    LoginPageView,
    RegisterView,
    LogoutPageView,
    HomePageView,
    PlantListView,
    PlantDetailView,
    PlantCreateView,
    PlantUpdateView,
    PlantDeleteView
)

urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('home/', HomePageView.as_view(), name='home'),

    path('plants/', PlantListView.as_view(), name='plant_list'),
    path('plants/add/', PlantCreateView.as_view(), name='create_plant'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant_detail'),
    path('plants/<int:pk>/update/', PlantUpdateView.as_view(), name='update_plant'),
    path('plants/<int:pk>/delete/', PlantDeleteView.as_view(), name='delete_plant'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)