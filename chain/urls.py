from chain.apps import ChainConfig

from rest_framework.routers import DefaultRouter

from chain.views import SupplierViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'products', ProductViewSet, basename='products')

app_name = ChainConfig.name

urlpatterns = [] + router.urls

