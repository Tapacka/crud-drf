from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = ['title', 'description', 'id']

    


class ProductPositionSerializer(serializers.ModelSerializer):   
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity','price']
    


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address','positions', 'id']

    def create(self, validated_data):
        pos = validated_data.pop('positions')    
        stock = super().create(validated_data)
        for p in pos:
            StockProduct.objects.create(stock=stock, **p)
        return stock
    

        

    def update(self, instance, validated_data):        
        positions = validated_data.pop('positions')        
        stock = super().update(instance, validated_data)
        print(stock)
        for position in positions:
            StockProduct.objects.update_or_create(id=1, defaults=position)  
        return stock


