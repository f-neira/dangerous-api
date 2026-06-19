from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Show
from .auth import require_jwt


@require_jwt
@require_GET
def show_list(request):
    Show.objects.archive_expired()
    shows = Show.objects.filter(archived=False)
    data = [
        {
            "id": show.id,
            "date": show.date.isoformat(),
            "country": show.country,
            "city": show.city,
            "venue": show.venue,
            "time": show.time.isoformat(),
            "tickets_url": show.tickets_url,
            "instagram_post_url": show.instagram_post_url,
        }
        for show in shows
    ]
    return JsonResponse({"results": data})
