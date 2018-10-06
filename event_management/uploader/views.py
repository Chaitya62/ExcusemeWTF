from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .utils import generate_profile_async
from .persistant_data import ProfileSingleton
import pickle
import math


# Create your views here.
def show_view(request):
    return render(request, 'dragAndDrop.html', {'title': "upload"});


def upload_view(request):

    ProfileSingleton.loaded_flag = False
    ProfileSingleton.profiles = []
    ProfileSingleton.languages_profile = dict()
    if request.method == 'POST':
        _, file = request.FILES.popitem()
        file = file[0]
        generate_profile_async(file)
    return HttpResponseRedirect("/uploader/get_status_loader")


def search_view(request):
    pickle_in = open("profiles.pickle", "rb")
    pickle_i = open('languages_profile', 'rb')
    ProfileSingleton.languages_profile = pickle.load(pickle_i)
    profiles = pickle.load(pickle_in)
    print(profiles)
    print("Language Profiles1: " + str(ProfileSingleton.languages_profile))

    ProfileSingleton.profiles = profiles
    ProfileSingleton.loaded_flag = True
    cp = False
    dev = False
    lang = None

    if request.method == 'GET':

        cp = True if request.GET.get('cp') == 'on' else False
        dev = True if request.GET.get('dev') == 'on' else False
        lang = request.GET.get('lang')

        if lang:
            profiles = ProfileSingleton.languages_profile[lang]
        else:
            profiles = ProfileSingleton.profiles

        if cp and dev:
            profiles.sort(key=lambda x: x.overall_score, reverse=True)
        elif cp:
            profiles.sort(key=lambda x: x.cp_score, reverse=True)

        elif dev:
            profiles.sort(key=lambda x: x.dev_score, reverse=True)
        else:
            profiles.sort(key=lambda x: x.overall_score, reverse=True)

        print(cp)
        print(dev)
        print(ProfileSingleton.profiles)

        return render(request, 'search.html', {'cp': cp, 'dev': dev, 'profiles': profiles, 'lang_profiles': ProfileSingleton.languages_profile.items(), 'lang': lang}, )

    else:
        return HttpResponse('403 forbidden')


def profile_view(request, id):
    # print("CHUT")
    pickle_in = open("profiles.pickle", "rb")
    profiles = pickle.load(pickle_in)
    print(profiles)
    print("Language Profiles1: " + str(ProfileSingleton.languages_profile))

    ProfileSingleton.profiles = profiles
    ProfileSingleton.loaded_flag = True
    profile = profiles[int(id)]
    lang_data = [value for key, value in profile.gLanguages.items()]
    languages = [key for key, value in profile.gLanguages.items()]
    cp_stars = ("x" * round(profile.cp_score))
    print(cp_stars)
    dev_stars = ("x" * round(profile.dev_score))
    print(dev_stars)
    print("Language Profiles: " + str(ProfileSingleton.languages_profile))
    badge_styles = {"Newbie": "badge-dark", "Beginner": "bage-secondary", "Advanced": "badge-success", "Expert": "badge-primary", "God": "badge-danger", "Unknown": "badge-light"}
    return render(request, 'profile.html', {"user_name": profile.gDetails['name'], "cp_score": profile.cp_score, "dev_score": profile.dev_score, "badge": profile.badge, "repos": profile.gRepos, "languages": languages, "lang_data": lang_data, "cp_score_stars": cp_stars, "dev_score_stars": dev_stars, "cp_no_stars": "x" * (5 - len(cp_stars)), "dev_no_stars": "x" * (5 - len(dev_stars)), 'summary': profile.summary.items(), 'avatar_url': profile.gDetails['avatar_url'], "badge_style": badge_styles[profile.badge]})


def loader_view(request):
    return render(request, 'loader.html', {})


def get_status_loader(request):
    return HttpResponse(ProfileSingleton.loaded_flag)
