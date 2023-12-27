from rest_framework import viewsets, filters

from chain.models import Supplier, Product
from chain.permissions import IsActiveOrStaff
from chain.serializers import SupplierSerializer, ProductSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsActiveOrStaff]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['country']
    ordering_fields = ['country']

    def get_queryset(self):
        queryset = Supplier.objects.all()

        # Фильтрация по стране, если она указана в параметрах запроса
        country = self.request.query_params.get('country', None)
        if country is not None:
            queryset = queryset.filter(country=country)

        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveOrStaff]
