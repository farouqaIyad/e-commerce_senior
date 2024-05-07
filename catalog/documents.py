from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from .models import ProductDetail


@registry.register_document
class ProductDetailDocument(Document):
    # to access a foreign key like the views you created you should declare a field for every foreign key
    # the product foreign key will be indexed
    product = fields.ObjectField(
        properties={
            # the name will be indexed though
            "name": fields.TextField()
        }
    )
    # the name of the field should be as the same as the related field
    product_detail = fields.ObjectField(
        properties={
            # the name will be indexed though
            "units": fields.IntegerField()
        }
    )

    class Index:
        name = "productdetail"

    class Django:

        model = ProductDetail
        fields = ["id", "sku"]
