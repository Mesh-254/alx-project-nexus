from rest_framework.routers import DefaultRouter  # type: ignore
from django.urls import path, include  # type: ignore
from realtimejobs import views



router = DefaultRouter()


router.register(r'signup', views.RegisterViewSet, basename='signup')
router.register(r'profile', views.UserViewSet, basename='profile')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'jobtypes', views.JobTypeViewSet, basename='jobtype')
router.register(r'tags', views.TagsViewSet, basename='tag')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'jobposts', views.JobpostViewSet, basename='jobpost')
router.register(r'jobinteractions', views.JobInteractionViewSet, basename='jobinteraction')
router.register(r'jobalerts', views.JobAlertViewSet, basename='jobalert')
router.register(r'joblists', views.JobPostListViewSet, basename='joblist')
router.register(r'payments', views.PaymentViewSet, basename='payment')




urlpatterns = [
    path('', include(router.urls)),
    path('auth/user/', views.get_current_user, name='auth-user'),
    path('profile/change-password/', views.UserViewSet.as_view({'patch': 'change_password'}), name='change-password'),
    path('verify_payment/', views.PaymentVerificationView.as_view(), name='verify_payment'),
    path('unsubscribe/<uuid:alert_id>/', views.unsubscribe, name='unsubscribe'),
]
