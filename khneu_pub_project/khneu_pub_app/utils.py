
from django.core.paginator import Paginator


def custom_pagination(page,query_set,number_of_items,*args,**kwargs):
    paginator = Paginator(query_set, number_of_items)
    return paginator.get_page(page) 
    

