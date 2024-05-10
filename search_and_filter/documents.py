from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from catalog.models import Product


@registry.register_document
class ProductDetailDocument(Document):
    # to access a foreign key like the views you created you should declare a field for every foreign key
    # the product foreign key will be indexed
    # product = fields.ObjectField(
    #     properties={
    #         # the name will be indexed though
    #         "name": fields.TextField()
    #     }
    # )
    # # the name of the field should be as the same as the related field
    # product_detail = fields.ObjectField(
    #     properties={
    #         # the name will be indexed though
    #         "units": fields.IntegerField()
    #     }
    # )
    # review = fields.ObjectField(
    #     properties = {
    #         "rating":fields.IntegerField()
    #     }
    # )

    product_t = fields.NestedField(properties={'price':fields.DoubleField()})

    class Index:
        name = "product"

    class Django:

        model = Product
        # we need to match the expected fields from elastic search with the serialzier
        fields = [
            "id",
            "name",
            "slug",
            
            # "images",
            # "uploaded_images"
        ]


# python manage.py search_index --rebuild
