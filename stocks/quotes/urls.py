from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('About.html', views.about, name="About"),
    path('Stock_data.html', views.show_stock_data, name="show_stock_data"),
    path('Add_stock.html', views.add_stock, name="Add Stock"),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('Delete_stock.html', views.delete_stock, name="Delete Stock"),
]