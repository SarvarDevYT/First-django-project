from django.shortcuts import render
from .models import Member

def members_list(request):
    mymembers = Member.objects.all().values()
    context = {
        'mymembers': mymembers,
    }
    return render(request, 'members/index.html', context)
