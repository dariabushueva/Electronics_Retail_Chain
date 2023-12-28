from rest_framework import serializers

from chain.models import Supplier, Product


class SupplierSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Поставщика """

    class Meta:
        fields = '__all__'
        model = Supplier
        read_only_fields = ('created',)

    def validate(self, data):
        parent = data.get('parent')
        supplier_type = data.get('supplier_type')
        instance = self.instance

        # Проверка, что завод не имеет поставщика
        if parent and supplier_type == Supplier.FACTORY:
            raise serializers.ValidationError('Завод не может иметь поставщика')

        # Проверка обновления поля "Задолженность перед поставщиком"
        if instance and 'debt' in data and instance.debt != data['debt']:
            raise serializers.ValidationError('Обновление поля "Задолженность перед поставщиком" запрещено.')

        return data


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Продукта """

    class Meta:
        fields = '__all__'
        model = Product
