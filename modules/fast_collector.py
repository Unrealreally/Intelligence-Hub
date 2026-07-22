from modules.github import (
    get_user,
    get_repos,
    get_languages,
)


# =====================================================
# FAST REPOSITORY CLEAN
# =====================================================

def clean_fast_repositories(repos):

    cleaned = []


    for repo in repos:

        cleaned.append({

            "name": repo.get("name"),

            "description": repo.get("description"),

            "url": repo.get("html_url"),

            "language": repo.get("language"),

            "stars": repo.get(
                "stargazers_count",
                0
            ),

            "forks": repo.get(
                "forks_count",
                0
            ),

            "fork": repo.get(
                "fork",
                False
            )

        })


    return cleaned


# =====================================================
# FEATURED PROJECT SELECTOR
# =====================================================

def select_featured_projects(repos):

    ranked = sorted(
        repos,
        key=lambda r: (
            r["stars"] * 3
            + r["forks"] * 2
            + (0 if r["fork"] else 5)
        ),
        reverse=True
    )


    featured = []


    for repo in ranked[:6]:

        repo["project_type"] = (
            "Fork"
            if repo["fork"]
            else "Original Project"
        )

        featured.append(repo)


    return featured


# =====================================================
# FAST STATS
# =====================================================

def calculate_fast_stats(repos, user):

    return {

        "repositories": len(repos),


        "original_projects": sum(
            1
            for repo in repos
            if not repo["fork"]
        ),


        "stars": sum(
            repo["stars"]
            for repo in repos
        ),


        "forks": sum(
            repo["forks"]
            for repo in repos
        ),


        "followers": user.get(
            "followers",
            0
        ),


        "following": user.get(
            "following",
            0
        )

    }



# =====================================================
# STAGE 1 COLLECTOR
# =====================================================

def collect_fast_profile(username):


    user = get_user(username)

    repos = get_repos(username)



    if (
        not user.get("success")
        or not repos.get("success")
    ):

        return {

            "success": False,

            "error": "Failed to collect profile"

        }



    repo_data = clean_fast_repositories(
        repos["data"]
    )


    featured_projects = select_featured_projects(
            repo_data
    )


    user_data = user["data"]



    return {


        "success": True,


        "username": username,


        "user": {

            **user["data"],
            "bio":  user["data"].get("bio")
            or
            "Developer profile generated from GitHub activity."

        },


        "repos": repo_data,


        "featured_repos": featured_projects,


        "languages":
        get_languages(
            repos["data"]
        ),



        "stats":
        calculate_fast_stats(
            repo_data,
            user_data
        )


    }