from .resume_parser import convert_pdf_to_txt, get_codechef_username, get_linkedin_username, get_github_username, get_links, get_mobile_number
from .githubapi import gitHubProfileAnalyzer
from .codechefapi import get_data_by_username


class Profile:

    cp_weights = {"fully_solved": 15, "partially_solved": 5, "rating": 80}
    dev_weights = {"followers": 25, "stars": 50, "commits": 10, "years": 15}

    min_dict = {"stars": 0, "commits": 0, "years": 0, "followers": 0, "fully_solved": 0, "partially_solved": 0, "rating": 0}
    max_dict = {"stars": 1000, "commits": 1000, "years": 40, "followers": 1000, "fully_solved": 1000, "partially_solved": 2000, "rating": 3310}

    def get_scale(self, num, mini, maxi):
        return (num - mini) / (maxi - mini)

    def __init__(self, resume_link):
        self.summary = dict()
        self.success = True
        print("Calling pdf to text")
        self.content = str(convert_pdf_to_txt(resume_link).encode('ascii', 'ignore')).replace(r"\n", " ")
        print(self.content)
        self.githubUN = get_github_username(get_links(self.content, "github.com"))

        if self.githubUN == "":
            self.success = False
            return

        self.linkedinUN = get_linkedin_username(get_links(self.content, "linkedin.com"))
        self.codechefUN = get_codechef_username(get_links(self.content, "codechef.com"))

        self.github = gitHubProfileAnalyzer(self.githubUN)

        if self.codechefUN != "":

            self.codechefData = get_data_by_username("https://codechef.com/users/" + self.codechefUN)
            self.cp_score = self.calculate_cp()
        else:

            self.cp_score = 0

        try:
            self.mNumber = get_mobile_number(self.content)
        except Exception as e:
            print(e)
            self.mNumber = "Mobile number not found"

        # obj.user_info()
        # obj.user_repos()
        # obj.user_languages()
        self.gRepos = self.github.user_repos()
        self.gLanguages = self.github.user_languages()
        self.gDetails = self.github.user_info()

        self.dev_score = self.calculate_dev()
        self.overall_score = 0.0

    def calculate_cp(self):
        score = 0.0
        for key, val in Profile.cp_weights.items():
            score += val * self.get_scale(self.codechefData[key], Profile.min_dict[key], Profile.max_dict[key])
        score /= 100
        return score

    def calculate_dev(self):
        score = 0.0
        for key, val in Profile.dev_weights.items():
            score += val * self.get_scale(self.gDetails[key], Profile.min_dict[key], Profile.max_dict[key])
        score /= 100
        return score


if __name__ == '__main__':
    p = Profile('resume4.pdf')

    print(p.gDetails)
