from django.shortcuts import render, redirect
from courses.models import *
from django.shortcuts import HttpResponse
from gotolearing.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


@login_required(login_url='login')
def checkOut(request, slug):
    course = Course.objects.get(slug = slug)
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    coupon_code_message = None
    coupon = None
    order = None
    payment = None
    error = None
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "Your are Already Enrolled in this Course"
    except:
        pass
    amount = None
    if error is None:
        amount = int((course.price - (course.price * course.discount * 0.01)) * 100)

    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            amount = course.price - (course.price * coupon.discount *0.01)
            amount = int(amount) * 100
        except:
            coupon_code_message = 'Invalid CouponCode'
            print('Cupon Code invalid')

    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        return redirect('my-courses')

    if action == 'create_payment':

            currency = "BDT"
            notes = {
                "email": user.email,
                "name": f'{user.first_name} {user.last_name}'
            }
            receipt = f"gotolearning-{int(time())}"
            order = client.order.create({'receipt':receipt, 'notes':notes, 'amount':amount, 'currency' :currency})

            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()




    context = {
        "course" : course,
        "order" : order,
        "payment" : payment,
        "user" : user,
        "error" : error,
        "coupon":coupon,
        "coupon_code_message": coupon_code_message,
    }
    return render(request, template_name="courses/check_out.html", context=context)


@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            userCourse = UserCourse(user=payment.user, course=payment.course)
            userCourse.save()

            print("UserCourse", userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return redirect('my-courses')

        except:
            return HttpResponse("Invalid Payment Details")