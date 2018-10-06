from github import Github
import json
import requests
import time
import math

auth_sha = "2de3535fc7b3198937e5fb926ae4f48996e90f91"


class gitHubProfileAnalyzer:

    URL = "https://api.github.com/users/"   # GitHub API
    repoURL = "https://api.github.com/repos/"

    def __init__(self, user_name):
        self.user_name = user_name
        self.api = Github(auth_sha)
        self.languages = {}
        self.commits = 0
        self.stars = 0

    def get_status(self):
        r = requests.get(self.user_url)
        return r.status_code, r.reason

    def get_info(self, url):
        r = requests.get(url)
        st = r.content.decode("utf-8")  # convert byte to str
        d = json.loads(st)              # convert str to dict
        return d

    def is_user(self):
        info = self.api.get_user(self.user_name)
        if info.type != "User":
            return False
        return True

    def user_info(self, verbose=False):
        user_dict = dict()
        info = self.api.get_user(self.user_name)

        user_dict['followers'] = info.followers
        user_dict['username'] = info.login
        user_dict['id'] = info.id
        user_dict['name'] = info.name
        user_dict['github_url'] = info.html_url
        user_dict['company'] = info.company
        user_dict['repo_count'] = info.public_repos
        user_dict['followers'] = info.followers
        user_dict['contributing_since'] = str(info.created_at)
        user_dict['years'] = math.floor((time.time() - (time.mktime(info.created_at.timetuple()))) / (60 * 60 * 24 * 30 * 12))
        user_dict['stars'] = self.stars
        user_dict['commits'] = self.commits
        user_dict['avatar_url'] = info.avatar_url

        # print(user_dict)

        if verbose:
            print(info.followers)
            print("User Info:")
            print("Username\t: " + str(info.login))
            print("ID\t\t: " + str(info.id))
            print(("Name\t\t: " + str(info.name)))
            print("GitHub URL\t: " + str(info.html_url))
            print("Comapny\t\t: " + str(info.company))
            print("Public Repos\t: " + str(info.public_repos))
            print("Followers\t: " + str(info.followers))
            print("Followings\t: " + str(info.following))
            print(str(info.name) + " is contributing since " + str(info.created_at))

        return user_dict
    # not useful
    # def user_followers(self):
    #     followers_url = self.user_url + "/followers"
    #     info = self.get_info(followers_url)
    #     print("\n\nFollowers:\nName\t\tGitHub URL")
    #     for follower in info:
    #         print(follower['login'] + "\t" + follower['html_url'])
    #
    # # ? ???? Not useful
    # def user_folllowing(self):
    #     following_url = self.user_url + "/following"
    #     info = self.get_info(following_url)
    #     print("\n\nFolLowings:\nName\t\tGitHub URL")
    #     for following in info:
    #         print(following['login'] + "\t" + following['html_url'])
    #
    # # Not useful
    # def user_starred(self):
    #     starred_url = self.user_url + "/starred"
    #     info = self.get_info(starred_url)
    #     print("\n\nStarred Repositories:")
    #     for starred in info:
    #         print(starred['name'])
    #         print("\t" + "Owner\t: " + starred['owner']['login'])
    #         print("\t " + "URL\t:" + starred['html_url'] + "\n")

    def user_repos(self, verbose=False):

        info = self.api.get_user(self.user_name).get_repos()
        repos = []

        for repo in info:

            if repo.parent != None:
                continue
            print(repo.name)
            # print(repo.parent)
            # print(dir(repo))
            # break
            repo_dic = dict()
            repo_dic['name'] = repo.name
            repo_dic['url'] = repo.html_url
            repo_dic['language'] = repo.language
            repo_dic['stars'] = repo.stargazers_count
            self.stars += repo.stargazers_count
            repo_dic['forks'] = repo.forks
            repo_dic['watchers'] = repo.watchers_count
            try:
                repo_dic['commits'] = repo.get_commits().totalCount

            except Exception as e:
                print(e)
                repo_dic['commits'] = 0

            self.commits += repo_dic['commits']

            lang = repo.language
            if lang is not None:
                if lang in self.languages.keys():
                    self.languages[lang] += 1
                else:
                    self.languages[lang] = 1

            # print(repo.get_commits().totalCount)

            if verbose:
                print("\n\nRepositories:")
                print(repo.name)
                print("\tURL : " + repo.html_url)
                print("\tLanguage : " + str(lang))
                #pr = self.get_info(self.repoURL + self.user_name + "/" + repo['name'] + "/pulls")
                #print("\tPull Requests : " + str(len(pr)))
                print("\tStargazers : " + str(repo.stargazers_count))
                print("\tForks : " + str(repo.forks) + "\n")
                #self.commits += len(comm)
            # break
            repos.append(repo_dic)

        return repos
        # repoJ = json.dumps(repos)
        # return repoJ

    def user_languages(self, verbose=False):
        lang_dict = dict()

        if verbose:
            print("Languages Used:")

        for lang in self.languages:
            lang_dict[lang] = self.languages[lang]
            if verbose:
                print(lang + " : " + str(self.languages[lang]))
        print("\nTotal Commits: " + str(self.commits))

        print(lang_dict)
        return lang_dict


if __name__ == '__main__':
    obj = gitHubProfileAnalyzer("Chaitya62")

    obj.user_info()
    obj.user_repos()
    obj.user_languages()
