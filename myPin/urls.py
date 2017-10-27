"""myPin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from showPins import views as core_views
from showPins.views import subscribe
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from showPins.views import (
    LPView,
    StartView,
    AddPhotoFormView,
    UserView,
    LogOutView,
    LogInFormView,
    MyCollectionView,
    UserUpdateView,
    PhotoInfoView,
    OtherGaleryView,
    add_to_collection,
    add_to_card,
    delete_collection_photo,
    CardView,
    card_delete,
    my_photo_delete,
    photo_update,
)


urlpatterns = [
    #dziala
    url(r'^admin/', admin.site.urls),
    url(r'^$', LPView.as_view(),
        name="lp"),
    url(r'^galery$', StartView.as_view(),
        name="galery"),
    url(r'^add_photo/(?P<pk>(\d)+)$', AddPhotoFormView.as_view(),
        name="add_photo"),
    url(r'^profile/(?P<pk>(\d)+)$', UserView.as_view(),
        name="profile"),
    url(r'^signup/$', core_views.signup,
        name='signup'),
    url(r'^logout$', LogOutView.as_view(),
        name="logout"),
    url(r'^login$', LogInFormView.as_view(),
        name="login"),
    url(r'^galery/(?P<user_id>(\d)+)$', MyCollectionView.as_view(),
        name="galery"),
    url(r'^update/(?P<pk>(\d)+)$', UserUpdateView.as_view(),
        name="update"),
    url(r'^info/(?P<photo_id>(\d)+)$', PhotoInfoView.as_view(),
        name="info"),
    url(r'^subscribe/', subscribe, name="subscribe"),
    url(r'^other_galery/(?P<user_id>(\d)+)$', OtherGaleryView.as_view(),
        name="other_galery"),
    url(r'^add_to_collection/(?P<photo_id>(\d)+)$', add_to_collection,
        name="add_to_collection"),
    url(r'^add_to_card/(?P<photo_id>(\d)+)$', add_to_card,
        name="add_to_card"),
    url(r'^delete_collection_photo/(?P<photo_id>(\d)+)$', delete_collection_photo,
        name="delete_collection_photo"),
    url(r'^card1$', CardView.as_view(),
        name="card"),
    url(r'^card_delete/(?P<card_id>(\d)+)$', card_delete,
        name="card_delete"),
    url(r'^my_photo_delete/(?P<photo_id>(\d)+)$', my_photo_delete,
        name="my_photo_delete"),
    url(r'^photo_update/(?P<photo_id>(\d)+)$', photo_update,
        name="photo_update"),

    #nie dziala


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
