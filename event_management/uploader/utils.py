from os import system
from time import time
from .collect_data import Profile
from threading import Thread
from .persistant_data import ProfileSingleton
import xlrd
import pickle
import os
from .resume_tokenizer import summarize


def postpone(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = False
        t.start()
    return decorator


def get_remote_resume(link):
    output_file = "/home/jigar/Desktop/EventManagement/event_management/resumes/" + str(time()) + ".pdf"
    system("wget -O " + output_file + " \"" + link + "\"")
    return output_file


def get_scale(num, mini, maxi):
    return (num - mini) / (maxi - mini)


@postpone
def generate_profile_async(file):
    work_book = xlrd.open_workbook(file_contents=file.read())
    sheet = work_book.sheet_by_index(0)
    for i in range(sheet.nrows):
        name = sheet.cell_value(i, 0)
        resume = sheet.cell_value(i, 1)
        print("Constructing Profile: " + resume)
        resume_path = get_remote_resume(resume)
        print(resume_path)
        resume_summary = summarize(resume_path)
        print(resume_summary)
        profile = Profile(resume_path)
        if not profile.success:
            continue

        for key, val in profile.gLanguages.items():

            if not key in ProfileSingleton.languages_profile:
                ProfileSingleton.languages_profile[key] = []

            ProfileSingleton.languages_profile[key].append(profile)

        print(ProfileSingleton.languages_profile)
        profile.summary = resume_summary
        ProfileSingleton.profiles.append(profile)
        ProfileSingleton.profiles[-1].id = len(ProfileSingleton.profiles) - 1

        # print(profile.gDetails)
        # print(profile.codechefData)
    cp_min = 1e9
    cp_max = 0
    dev_min = 1e9
    dev_max = 0

    for profile in ProfileSingleton.profiles:
        cp_max = max(cp_max, profile.cp_score)
        cp_min = min(cp_min, profile.cp_score)
        dev_max = max(dev_max, profile.dev_score)
        dev_min = min(dev_min, profile.dev_score)
    print(cp_max)
    print(cp_min)
    print(dev_max)
    print(dev_min)
    for profile in ProfileSingleton.profiles:
        if(cp_max == cp_min):
            profile.cp_score = 5.0
        else:
            profile.cp_score = round((get_scale(profile.cp_score, cp_min, cp_max)) * 5, 1)
        if(dev_max == dev_min):
            profile.dev_score = 5.0
        else:
            profile.dev_score = round((get_scale(profile.dev_score, dev_min, dev_max)) * 5, 1)
        overall_score = round((profile.dev_score + profile.cp_score) / 2, 1)
        profile.overall_score = overall_score
        if(overall_score <= 0.0):
            profile.badge = "Newbie"
        elif overall_score > 0.0 and overall_score <= 2.0:
            profile.badge = "Beginner"
        elif overall_score > 2.0 and overall_score <= 4.0:
            profile.badge = "Advanced"
        elif overall_score > 4.0 and overall_score < 5.0:
            profile.badge = "Expert"
        elif overall_score == 5.0:
            profile.badge = "God"
        else:
            profile.badge = "Unknown"
        print("CP Score: " + str(profile.cp_score) + " of " + str(profile.githubUN))
        print("Dev Score: " + str(profile.dev_score) + " of " + str(profile.githubUN))

    os.chdir('/home/jigar/Desktop/EventManagement/event_management/')

    pickle_o = open('languages_profile', 'wb')
    pickle.dump(ProfileSingleton.languages_profile, pickle_o)
    pickle_o.close()

    pickle_out = open("profiles.pickle", "wb")
    pickle.dump(ProfileSingleton.profiles, pickle_out)
    pickle_out.close()
    ProfileSingleton.loaded_flag = True
