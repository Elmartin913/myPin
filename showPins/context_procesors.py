from .models import Photo, Card


def all_photos(request):
    all_photos = Photo.objects.all().order_by('-creation_date')
    len_card = len(Card.objects.filter(user_id=request.user.id))
    ctx = {
        'all_photos': all_photos,
        'len_card': len_card,
    }
    return ctx

