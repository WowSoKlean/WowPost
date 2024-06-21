from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .utils import *
from .forms import *

def activateEmail(request, user, to_email):
    messages.success(request, f"""Dear <b>{user}</b>, please go to your email <b>{to_email}</b>
                                inbox and click the activation link we just sent you! 
                                <b>Note:</b> Check your spam folder."""
                    )
    
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            messages.success(request, 'Your account has been created successfully! Back to home...')

            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

def home(request):
    posts = Card.objects.all().order_by('-created_at')
    user = request.user

    for post in posts:
        post.is_recommended = user in post.recommended_by.all()

    context  = {'user':user, 'posts': posts} 

    return render(request, 'Accounts/home.html', context)

@login_required(login_url="/login")
def profile(request):
    user = request.user
    user_card_image_urls = []
    
    for item in Card.objects.filter(owner=user):
        if item.image:
            user_card_image_urls.append(item.image.url)
        
    context = {
        'user': user,
        'user_card_image_urls': user_card_image_urls
    }
    
    return render(request, 'Accounts/profile.html', context)

@login_required(login_url="/login")
def profile_image_update(request):
    user = request.user
    user_image_instance = UserImage.objects.get_or_create(owner=user)[0]

    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES, instance=user_image_instance)
        if form.is_valid():
            form.save()
            return redirect('/profile')  
    else:
        form = UserImageForm(instance=user_image_instance)
    
    return render(request, 'registration/profile_image_update.html', {'form': form})

@login_required(login_url="/login")
def profile_bio_update(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserBioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile')  # Redirect to profile page after successful update
    else:
        form = UserBioForm(instance=user)
    
    return render(request, 'registration/profile_bio_update.html', {'form': form})

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)

        if form.is_valid():
            # Assign the current user as the owner of the card
            card = form.save(commit=False)
            card.owner = request.user  # Assuming the user object is stored in request.user
            card.save()

            return redirect('/home')
    else:
        form = CardForm()

    return render(request, 'Accounts/create_post.html', {"form": form})

@login_required(login_url="/login")
def update_recommendation(request, card_id):
    user = request.user
    posts = Card.objects.all().order_by('-created_at')
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        recommend = request.POST.get('recommend')

        if recommend == 'recommend':
            if user not in card.recommended_by.all():
                # User is recommending, add the association
                card.recommended_by.add(user)
                card.recommended_count += 1
                card.save()
        else:
            # User is un-recommending
            if user in card.recommended_by.all():
                # User had recommended, remove the association
                card.recommended_by.remove(user)
                card.recommended_count -= 1
                card.save()

        for post in posts:
            post.is_recommended = user in post.recommended_by.all()

        data = {
            'user': user,
            'posts': posts,
            'recommended_count': card.recommended_count,
            'is_recommended': user in card.recommended_by.all()
        }

        return render(request, 'Accounts/home.html', data)
    else:
        return JsonResponse({'error': 'Invalid request'})
    
@login_required(login_url="/login")
def delete_post(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        if card.owner == request.user:
            card.delete()

            messages.success(request, 'The post was sucessfully deleted!')
            return redirect('/home')
        else:
            return HttpResponseForbidden("")
    else:
        return JsonResponse({'error': 'Invalid request'})

class CustomPasswordResetView(LoginRequiredMixin, PasswordResetView):
    def post(self, request, *args, **kwargs):
        # Use the email of the authenticated user
        request.POST = request.POST.copy()
        request.POST['email'] = request.user.email
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Optionally, you can add any extra functionality here
        return super().form_valid(form)
    
#update_session_auth_hash(self.request, self.object)  # Update session
#

@login_required(login_url="/login")
def custom_logout(request):
    print("Logging out user: ", request.user)
    logout(request)
    
    return redirect('/login')
    
@login_required(login_url="/login")
def delete_account(request):
  if request.method == 'POST':
    try:
      # Account deletion logic (user removal, card updates)
      user = request.user

      for card in Card.objects.all():
        if user in card.recommended_by.all():
          card.recommended_by.remove(user)
          card.save()

      user.delete()
      messages.success(request, 'Your account has been deleted!')
      logout(request)  # Logout the user after deletion
      
      return redirect('/home')
    
    except Exception as e:
      # Handle deletion errors here
      return JsonResponse({'error': f'Account deletion failed: {e}'})
  else:
    return JsonResponse({'error': 'Invalid request'})

