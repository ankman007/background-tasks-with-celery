from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from loguru import logger
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from a_messageboard.tasks import send_email
from a_messageboard.models import MessageBoard
from a_messageboard.forms import MessageCreateForm


def home(request):
    messageboards = MessageBoard.objects.annotate(subscriber_count=Count('subscribers'))
    context = {
        "messageboards": messageboards,
    }
    return render(request, 'a_messageboard/index.html', context)


@login_required
def messageboard_detail(request, board_id=1):
    messageboard = get_object_or_404(MessageBoard, id=board_id)
    subscriber_count = messageboard.subscribers.count()
    form = MessageCreateForm(request.POST or None)
        
    if request.method == 'POST' and form.is_valid():
        if request.user in messageboard.subscribers.all():
            message = form.save(commit=False)
            message.author = request.user
            message.messageboard = messageboard
            message.save()
            messages.success(request, 'Your message has been posted.')
            
            subscribers = messageboard.subscribers.all()
            for subscriber in subscribers.exclude(id=request.user.id):
                send_email.delay(recipient_email=subscriber.email, message=message.body, author=request.user.username)
        else:
            messages.warning(request, 'You must subscribe to post a message on this board.')
            
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('a_messageboard/partials/messages.html', {'messageboard': messageboard})
            return HttpResponse(html)

        return redirect('messageboard_detail', board_id=board_id)
        
    context = {
        'messageboard': messageboard,
        'form': form,
        'subscriber_count': subscriber_count,
    }
    return render(request, 'a_messageboard/messageboard.html', context)


@login_required
def subscribe(request, board_id):
    messageboard = get_object_or_404(MessageBoard, id=board_id)

    if not messageboard.subscribers.filter(pk=request.user.pk).exists():
        messageboard.subscribers.add(request.user)
    else:
        messageboard.subscribers.remove(request.user)
    return redirect('messageboard_detail', board_id=board_id)