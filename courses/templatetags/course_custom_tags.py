from django import template
import math
from courses.models import *

register = template.Library()

# 100 -> 10% --> mrp - (mrp * discount * 0.01) = selprice

@register.simple_tag
def cal_sellprice(price, discount):
    if discount is None or discount is 0 :
        return price
    sellprice = price
    sellprice = price - (price * discount * 0.01)
    return math.floor(sellprice)


@register.filter
def taka(price):
    return f'৳{price}'

@register.simple_tag
def is_enrolled(request, course):
    user = None
    if not request.user.is_authenticated:
        return False
    user = request.user
    try:
        user_course = UserCourse.objects.get(user = user, course = course)
        return True
    except:
        return False