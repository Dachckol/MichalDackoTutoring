from .models import Notification

def getNotifications(request):
	if not request.user.is_authenticated:
		return {}
	notifications = Notification.objects.all().filter(target=request.user.profile)
	for n in notifications:
		if n.expired:
			n.delete()
		else:
			n.expired=True
			n.save()
	notifications = Notification.objects.all().filter(target=request.user.profile)
	return {"notifications":notifications}