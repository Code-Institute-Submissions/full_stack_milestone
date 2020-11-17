from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile, SubscriberList
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    subscribed = False
    profile = get_object_or_404(UserProfile, user=request.user)
    # Get value to subscriber toggle on profile page
    subTog = request.POST.get('subTogBtn', '')
    # Get user instance and user email
    user = get_object_or_404(User, username=request.user)
    user_email = str(user.email)

    if subTog == "on":
        print("User wants to subscribe")
        # if the user is already subscribed
        if SubscriberList.objects.filter(email=user_email).exists():
            print("Already Subscribed")
        else:
            # create and save subscriber instance.
            SubscriberList.objects.create(email=user_email)
        subscribed = True
    else:
        print("User does not want to Subscribe")
        if SubscriberList.objects.filter(email=user_email).exists():
            print("Subscribed. Now delete")
            # Delete subscriber instance.
            subscriber_instance = get_object_or_404(SubscriberList,
                                                    email=user_email)
            subscriber_instance.delete()
            print("Delete Subscription")
        else:
            print("No Subscription")
        subscribed = False

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        messages.error(request, 'Profile update Fail. Ensure\
                                all field are valid')
    # Use the profile and the related name on the order model
    # to get the users orders and return those to the template
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'subscribed': subscribed,
    }

    return render(request, template, context)


def order_history(request, order_number):
    # get order
    order = get_object_or_404(Order, order_number=order_number)
    # provide message to user
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def subscribe_List(request):
    # get email supplied
    email = request.POST.get('email', '')
    print(email)
    # check if email already exists in Subscriber List
    print(SubscriberList.objects.filter(email=email).exists())

    if SubscriberList.objects.filter(email=email).exists():
        # if the email is already on the subscriber list, providse
        # the user with a notification
        messages.info(request, ('Subscriber Already Exists'))
        print("Subscriber Exists")
        return redirect(reverse('home'))
    else:
        # if the email is not already in the subscriber list,
        # create and save subscriber instance.
        SubscriberList.objects.create(email=str(email))
        messages.success(request, ('Thanks for subscribing'))
        print("Subscriber to be saved")
        return redirect(reverse('home'))
