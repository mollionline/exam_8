from django.urls import path
from webapp.views.product_views import (ProductCreateView,
                                        ProductDetailView,
                                        ProductListView,
                                        UpdateProductView,
                                        ProductDeleteView)

from webapp.views.review_views import (ReviewDeleteView,
                                       ReviewDetailView,
                                       ReviewsListView,
                                       UpdateReviewView,
                                       NewAddReviewView)

urlpatterns = []

product_urls = [
    path('product/add', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail_product'),
    path('', ProductListView.as_view(), name='list_product'),
    path('product/<int:pk>/update', UpdateProductView.as_view(), name='update_product'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_product')
]

review_urls = [
    path('review/<int:pk>', ReviewDetailView.as_view(), name='detail_review'),
    path('reviews/', ReviewsListView.as_view(), name='list_review'),
    path('review/<int:pk>/update', UpdateReviewView.as_view(), name='update_review'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='delete_review'),
    path('products/<int:pk>/new', NewAddReviewView.as_view(), name='add_review')
]


urlpatterns += review_urls
urlpatterns += product_urls
