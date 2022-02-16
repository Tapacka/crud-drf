from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = ['title', 'description', 'id']

    


class ProductPositionSerializer(serializers.ModelSerializer):   
    class Meta:
        model = StockProduct
        fields = ['stock', 'product', 'quantity','price']
    


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address','positions']

    def create(self, validated_data):
        pos = validated_data.pop('positions')    
        stock = super().create(validated_data)
        for p in pos:
            StockProduct.objects.create(stock=stock, **p)
        return stock
    

        

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        StockProduct.objects.update_or_create(stock=stock, **positions)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
