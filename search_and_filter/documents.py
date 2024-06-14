# from django_elasticsearch_dsl.registries import registry
# from django_elasticsearch_dsl import Document,fields
# from catalog.models import Product


# @registry.register_document
# class ProductDocument(Document):
#     # to access a foreign key like the views you created you should declare a field for every foreign key
#     # the product foreign key will be indexed
#     # # the name of the field should be as the same as the related field
#     # product_detail = fields.ObjectField(
#     #     properties={
#     #         # the name will be indexed though
#     #         "units": fields.IntegerField()
#     #     }
#     # )
#     # review = fields.ObjectField(
#     #     properties = {
#     #         "rating":fields.IntegerField()
#     #     }
#     # )

#     class Index:
#         name = "product"


#     class Django:

#         model = Product
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "main_price",
#             "reviews_count",
#             "average_rating",
#             "main_image",
#         ]


# # python manage.py search_index --rebuild
