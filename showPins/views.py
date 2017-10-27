from django.http import HttpResponse, HttpResponseRedirect, request, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.template.response import TemplateResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, AbstractBaseUser, UserManager
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from pprint import pprint
from django.views.generic.list import ListView
from .utils import SendSubscribeMail

from .forms import (
    SignUpForm,
    AddPhotoForm,
    LoginForm,
    CommentForm,

)
from .models import (
    Photo,
    User,
    Like,
    Comment,
    Subscribe,
    Collection,
    Card,
    OrderId,
)

# Create your views here.

# dziala

class LPView(View):
    def get(self, requset):
        return TemplateResponse (requset, 'start.html')


class StartView(View):
    def get(self, request):
        return TemplateResponse(request, 'galery.html')


class AddPhotoFormView(CreateView):
    form_class = AddPhotoForm
    template_name = 'new_photo_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddPhotoFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.kwargs['pk']])


class UserView(View):

    def get(self, request, pk):
        user =User.objects.get(pk=int(pk))
        usr_photos = Photo.objects.filter(user_id=int(pk))
        return render(request, 'profile.html', {'user': user, 'usr_photos': usr_photos})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('lp')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('lp'))


class LogInFormView(LoginView):
    model = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('galery')


class MyCollectionView(View):
    def get(self, request, user_id):
        photos = Collection.objects.filter(user_id=int(user_id))
        return render(request, 'my_galery.html', {'photos': photos})


class UserUpdateView(UpdateView):
    model = User
    template_name = 'update_form.html'
    fields = ['first_name', 'last_name', 'email', 'user_desc']

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.kwargs['pk']])


class PhotoInfoView(View):

    def get(self, request, photo_id):
        form = CommentForm()
        photo_info =Photo.objects.get(pk=int(photo_id))
        comments = Comment.objects.filter(photo_id=int(photo_id)).order_by('-add_comment')
        likes = Like.objects.filter(photo_id=int(photo_id))
        num_comments = str(len(comments))
        num_likes = str(len(likes))
        ctx = {
            'photo_info': photo_info,
            'comments': comments,
            'likes': likes,
            'num_comments': num_comments,
            'num_likes': num_likes,
            'form': form,
        }
        return render(request, 'photo_info.html', ctx)

    def post(self, request, photo_id):
        like = int(request.POST['like'])
        Like.objects.create(
            like_type=like,
            user_id=self.request.user.id,
            photo_id=int(photo_id)
        )
        form = CommentForm(request.POST)
        if form.is_valid():

            comment = form.cleaned_data['comment']
            Comment.objects.create(
                comment=comment,
                user_id = self.request.user.id,
                photo_id = int(photo_id)
            )

        return HttpResponseRedirect('/info/{}'.format(str(photo_id)))


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email_id']
        email_qs = Subscribe.objects.filter(email_id = email)
        if email_qs.exists():
            data = {"status" : "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id = email)
            SendSubscribeMail(email) # Send the Mail, Class available in utils.py

    return HttpResponseRedirect('/galery')


class OtherGaleryView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=int(user_id))
        photos = user.photo_set.all()
        return render(request, 'other_galery.html', {'photos': photos, 'user': user})


def add_to_collection(request, photo_id):
    photo_id = int(photo_id)
    if request.method == 'GET':
        check_photo_id = Collection.objects.filter(photo_id = photo_id)
        if len(check_photo_id)==0:
            Collection.objects.create(
                user_id = request.user.id,
                photo_id = int(photo_id)
            )
        return HttpResponseRedirect('/info/{}'.format(str(photo_id)))


def delete_collection_photo(request, photo_id):
    if request.method == 'GET':
        photo = Collection.objects.get(photo_id=int(photo_id))
        photo.delete()
        return HttpResponseRedirect('/galery/{}'.format(str(photo.user_id)))


def add_to_card(request, photo_id):
    if request.method == 'GET':
        photo = Photo.objects.get(pk=int(photo_id))
        in_card = Card.objects.filter(
            photo_id=int(photo_id)).filter(
            user_id=request.user.id)
        if len(in_card)==0:
            Card.objects.create(
                user_id=request.user.id,
                photo_id=int(photo_id),
                buy_price=photo.price,
                )
            return HttpResponseRedirect('/info/{}'.format(str(photo_id)))
        else:
            return HttpResponse('Zdjęcie jest już w koszyku')


def card_delete(request, card_id):
        card = Card.objects.filter(pk=int(card_id))
        card.delete()
        return redirect('/card1')


def my_photo_delete(request, photo_id):
    photo = Photo.objects.filter(pk=int(photo_id))
    photo.delete()
    return redirect('/profile/{}'.format(request.user.id))


class CardView(View):
    def get(self, request):
        card = Card.objects.filter(user_id=self.request.user.id)
        sum = 0
        for price in card:
            sum += price.buy_price
        return render(request, 'card_form.html', {'card': card, 'sum': sum})

    def post(self,request):
        # optradio =request.POST.get('optradio')
        # delivery_target = request.POST.get('delivery_target')
        # sum = request.POST.get('sum')
        # card = Card.objects.filter(user_id=self.request.user.id)
        #
        # order = OrderId.objects.create(
        #     total_price=sum,
        #     buy_price=[c.buy_price for c in card],
        #     quantity=1,
        #     delivery=optradio,
        #     delivery_target=delivery_target,
        #     user_id=self.request.user.id,
        #     photo=[c.photo_id for c in card],
        # )

        return HttpResponse('Formularz przelewu')

def photo_update(request, photo_id):
    return HttpResponse('Formularz modyfikacji zdjęcia')