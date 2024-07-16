
from django.urls import path
from cart.views import CartListView, AddToCartView, IncreaseCartItemView, DecreaseCartItemView, RemoveCartItemView, CheckoutView

app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name='order-list'),
    path('add/', AddToCartView.as_view(), name='cart-add'),
    path('plus/<int:pk>/', IncreaseCartItemView.as_view(), name='cart-plus'),
    path('minus/<int:pk>/', DecreaseCartItemView.as_view(), name='cart-minus'),
    path('remove/<int:pk>/', RemoveCartItemView.as_view(), name='cart-remove'),
    path('<int:pk>/checkout/', CheckoutView.as_view(), name='cart-checkout'),


]

