from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'notification/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

@login_required
def mark_all_notifications_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notification_list')
