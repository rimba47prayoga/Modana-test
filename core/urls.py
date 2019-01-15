from rest_framework import routers
from .views import PaymentViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register('payment', PaymentViewSet, 'payment-path')

urlpatterns = router.urls
