from modules.github import (
    get_user,
    get_repos,
    get_languages,
    get_events,
    get_commits,
    get_readme,
    get_topics
)

from modules.graphql import (
    get_contribution_data,
    get_profile_data
)


# =====================================================
# CLEAN REPOSITORIES
# =====================================================

def clean_repositories(repos):

    cleaned = []


    for repo in repos:

        cleaned.append({

            # Identity

            "name": repo.get(
                "name"
            ),

            "description": repo.get(
                "description"
            ),

            "url": repo.get(
                "html_url"
            ),


            # Technology

            "language": repo.get(
                "language"
            ),


            # Popularity

            "stars": repo.get(
                "stargazers_count",
                0
            ),

            "forks": repo.get(
                "forks_count",
                0
            ),


            # Ownership

            "fork": repo.get(
                "fork",
                False
            ),


            # Timeline

            "created_at": repo.get(
                "created_at"
            ),

            "updated_at": repo.get(
                "updated_at"
            ),


            # Quality

            "license": (
                repo.get("license") is not None
            ),

            "issues": repo.get(
                "has_issues",
                False
            ),

            "open_issues_count": repo.get(
                "open_issues_count",
                0
            ),


            # Engineering

            "size": repo.get(
                "size",
                0
            ),

            "default_branch": repo.get(
                "default_branch"
            ),

            "archived": repo.get(
                "archived",
                False
            ),


            # Intelligence fields

            "has_readme": False,

            "readme_length": 0,

            "topics": [],

            "topic_count": 0,

            "commit_count": 0,

            "active_months": 0

        })


    cleaned.sort(
        key=lambda x:
        x["updated_at"]
        if x["updated_at"]
        else "",
        reverse=True
    )


    return cleaned


# =====================================================
# README INTELLIGENCE
# =====================================================

def analyze_readme_quality(repo):

    score = 0


    if repo.get("has_readme"):
        score += 30


    length = repo.get(
        "readme_length",
        0
    )


    if length > 300:
        score += 30


    if length > 1000:
        score += 20


    if repo.get("topic_count", 0) > 0:
        score += 20


    return score




# =====================================================
# EVENTS
# =====================================================


def clean_events(events):

    activity = []


    for event in events:

        activity.append({

            "type": event.get(
                "type"
            ),

            "repo": (
                event.get(
                    "repo",
                    {}
                )
                .get(
                    "name"
                )
            ),

            "created_at": event.get(
                "created_at"
            )

        })


    return activity



# =====================================================
# REPOSITORY INTELLIGENCE
# =====================================================


def collect_repository_details(username, repos):

    details = []


    for repo in repos:

        name = repo.get(
            "name"
        )


        topics = get_topics(
            username,
            name
        )

    

        readme = get_readme(
            username,
            name
        )


        topic_list = []


        if (
            topics.get("success")
        and isinstance(
            topics.get("data"),
            dict
            )
    ):

            topic_list = topics["data"].get(
                "names",
             []
         )



        readme_text = ""


        if  readme.get("success"):

            readme_text = readme.get(
                "data",
                ""
            )



        details.append({

            "name": name,

            "topics": topic_list,

            "topic_count": len(
                topic_list
            ),

            "has_readme": bool(
                readme.get(
                    "success"
                )
            ),

            "readme_length": len(
                readme_text
            )

        })


    return details



# =====================================================
# COMMITS
# =====================================================


def collect_commits(username, repos):

    commits = []


    for repo in repos[:10]:


        response = get_commits(
            username,
            repo["name"]
        )


        if not response.get(
            "success"
        ):
            continue



        for commit in response["data"]:

            author = (
                commit
                .get(
                    "commit",
                    {}
                )
                .get(
                    "author",
                    {}
                )
            )


            commits.append({

                "repo": repo["name"],

                "date": author.get(
                    "date"
                ),

                "message": (
                    commit
                    .get(
                        "commit",
                        {}
                    )
                    .get(
                        "message"
                    )
                )

            })


    return commits



# =====================================================
# BASIC STATS
# =====================================================

def calculate_basic_stats(repos):

    return {

        "repositories": len(repos),


        "original_projects": sum(
            1
            for repo in repos
            if not repo["fork"]
        ),


        "stars": sum(
            repo.get("stars", 0)
            for repo in repos
        ),


        "forks": sum(
            repo.get("forks", 0)
            for repo in repos
        ),


        "documented_projects": sum(
            1
            for repo in repos
            if (
                repo.get("description")
                and repo.get("has_readme")
            )
        ),


        "licensed_projects": sum(
            1
            for repo in repos
            if repo.get("license")
        ),


        "documented_quality_score": sum(
            repo.get(
                "readme_score",
                0
            )
            for repo in repos
        )

    }


# =====================================================
# PROFILE COLLECTOR
# =====================================================


def collect_deep_profile(username):


    user = get_user(username)

    repos = get_repos(username)

    events = get_events(username)

    contributions = get_contribution_data(
        username
    )

    profile = get_profile_data(
        username
    )



    if (
        not user.get("success")
        or not repos.get("success")
    ):

        return {

            "success": False,

            "error":
            "Failed to collect profile data"

        }



    repo_data = clean_repositories(
        repos["data"]
    )



    repository_details = collect_repository_details(
        username,
        repos["data"][:10]
    )



    # Attach intelligence data

    for repo in repo_data:


        detail = next(
            (
                item
                for item in repository_details
                if item["name"] == repo["name"]
            ),
            {}
        )


        repo["has_readme"] = detail.get(
            "has_readme",
            False
        )


        repo["readme_length"] = detail.get(
            "readme_length",
            0
        )


        repo["topics"] = detail.get(
            "topics",
            []
        )


        repo["topic_count"] = detail.get(
            "topic_count",
            0
        )

        repo["readme_score"] = analyze_readme_quality(
            repo
        )



    event_data = clean_events(

        events["data"]

        if events.get("success")

        else []

    )



    commit_data = collect_commits(
        username,
        repo_data
    )



    languages = get_languages(
        repos["data"]
    )

        # =====================================================
    # Featured repositories
    # =====================================================

    featured_repos = sorted(
        repo_data,
        key=lambda r: (
            (r.get("stars", 0) * 10)
            + (r.get("forks", 0) * 5)
            + (r.get("readme_score", 0) * 3)
            + (r.get("topic_count", 0) * 2)
            + (20 if not r.get("fork", False) else 0)
        ),
        reverse=True
    )[:6]



    return {


        "success": True,


        "username": username,


        "user": user["data"],


        "repos": repo_data,


        "events": event_data,


        "repository_details":
        repository_details,


        "featured_repos": featured_repos,


        "commits": commit_data,


        "commit_count":
        len(commit_data),


        "languages": languages,


        "stats":
        calculate_basic_stats(
            repo_data
        ),



        "contributions": (

            contributions["data"]["data"]["user"]["contributionsCollection"]

            if (
                contributions
                and contributions.get("success")
                and contributions.get("data")
                and contributions["data"].get("data")
                and contributions["data"]["data"].get("user")
            )

            else {}

        ),



        "graphql_profile": (

            profile["data"]

            if profile
            and profile.get("data")

            else {}

        )


    }