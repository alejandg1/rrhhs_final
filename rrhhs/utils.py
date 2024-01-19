from django.conf import settings
def get_image(image):
    if image:
        return '{}{}'.format(settings.MEDIA_URL, image)
    
    return '/static/assets/img/empty.png'