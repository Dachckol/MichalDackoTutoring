from .models import Profile


def getProfile(request):
	return Profile.objects.filter(active=True)[0].getContext()
