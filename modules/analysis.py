from datetime import datetime, timedelta


def safe_parse_date(date_string):

    if not date_string:
        return None

    try:
        return datetime.strptime(
            date_string,
            "%Y-%m-%dT%H:%M:%SZ"
        )

    except ValueError:
        return None

# =====================================================
# MOMENTUM
# =====================================================





# -------------------------
# Recent Activity Score
# -------------------------

def recent_activity_score(events):

    if not events:
        return 0


    cutoff = datetime.now() - timedelta(days=90)


    active_days = set()


    for event in events:

        date = safe_parse_date(
            event.get("created_at")
        )


        if date and date >= cutoff:

            active_days.add(
                date.strftime("%Y-%m-%d")
            )


    days = len(active_days)


    if days >= 30:
        return 30

    elif days >= 20:
        return 25

    elif days >= 10:
        return 15

    elif days >= 5:
        return 10

    elif days >= 1:
        return 5


    return 0



# -------------------------
# Commit Activity Score
# -------------------------

def commit_activity_score(commits):

    if not commits:
        return 0


    cutoff = datetime.now() - timedelta(days=90)


    commit_days = set()

    commit_count = 0


    for commit in commits:

        date = safe_parse_date(
            commit.get("date")
        )


        if date and date >= cutoff:

            commit_count += 1

            commit_days.add(
                date.strftime("%Y-%m-%d")
            )


    days = len(commit_days)



    score = 0


    # quantity
    if commit_count >= 60:
        score += 15

    elif commit_count >= 30:
        score += 12

    elif commit_count >= 15:
        score += 8

    elif commit_count >= 5:
        score += 5



    # consistency
    if days >= 25:
        score += 10

    elif days >= 15:
        score += 8

    elif days >= 7:
        score += 5


    return min(score, 25)



# -------------------------
# Contribution Rhythm Score
# -------------------------

def contribution_rhythm_score(contributions):

    try:

        calendar = (
            contributions["user"]
            ["contributionsCollection"]
            ["contributionCalendar"]
        )


        total = calendar.get(
            "totalContributions",
            0
        )


    except Exception:

        return 0



    if total >= 500:
        return 25

    elif total >= 300:
        return 20

    elif total >= 100:
        return 15

    elif total >= 50:
        return 10

    elif total >= 10:
        return 5


    return 0



# -------------------------
# Repository Movement Score
# -------------------------

def repository_movement_score(repos):

    if not repos:
        return 0


    cutoff = datetime.now() - timedelta(days=180)


    active_projects = 0


    for repo in repos:

        updated = safe_parse_date(
            repo.get("updated_at")
        )


        if updated and updated >= cutoff:

            active_projects += 1



    if active_projects >= 5:
        return 20

    elif active_projects >= 3:
        return 15

    elif active_projects >= 2:
        return 10

    elif active_projects >= 1:
        return 5


    return 0



# -------------------------
# Main Momentum Calculator
# -------------------------

def calculate_momentum(data):

    events = data.get(
        "events",
        []
    )


    commits = data.get(
        "commits",
        []
    )


    contributions = data.get(
        "contributions",
        {}
    )


    repos = data.get(
        "repos",
        []
    )



    recent = recent_activity_score(
        events
    )


    commit = commit_activity_score(
        commits
    )


    contribution = contribution_rhythm_score(
        contributions
    )


    repository = repository_movement_score(
        repos
    )



    total = min(
        recent +
        commit +
        contribution +
        repository,
        100
    )



    return {

        "recent_activity": recent,

        "commit_activity": commit,

        "contribution_rhythm": contribution,

        "repository_movement": repository,

        "total": total

    }

# =====================================================
# DISCIPLINE
# Measures consistency, habits and engineering routine
# =====================================================


# -------------------------
# Commit Routine
# -------------------------

def commit_routine_score(commits):

    if not commits:
        return 0


    cutoff = datetime.now() - timedelta(days=180)

    commit_days = set()


    for commit in commits:

        date = safe_parse_date(
            commit.get("date")
        )


        if not date:
            continue


        if date >= cutoff:

            commit_days.add(
                date.date()
            )


    days = len(commit_days)


    if days >= 60:
        return 35

    elif days >= 40:
        return 28

    elif days >= 25:
        return 20

    elif days >= 10:
        return 12

    elif days >= 5:
        return 5


    return 0




# -------------------------
# Contribution Habit
# -------------------------

def contribution_habit_score(contributions):

    if not contributions:
        return 0


    calendar = (
        contributions
        .get("user", {})
        .get("contributionsCollection", {})
        .get("contributionCalendar", {})
    )


    weeks = calendar.get(
        "weeks",
        []
    )


    active_weeks = 0


    for week in weeks:

        days = week.get(
            "contributionDays",
            []
        )


        if any(
            day.get(
                "contributionCount",
                0
            ) > 0
            for day in days
        ):
            active_weeks += 1



    if active_weeks >= 20:
        return 30

    elif active_weeks >= 15:
        return 25

    elif active_weeks >= 10:
        return 18

    elif active_weeks >= 5:
        return 10

    elif active_weeks >= 1:
        return 5


    return 0




# -------------------------
# Repository Maintenance
# -------------------------

def maintenance_behavior_score(repos):

    if not repos:
        return 0


    cutoff = datetime.now() - timedelta(days=180)

    maintained = 0


    for repo in repos:

        updated = safe_parse_date(
            repo.get("updated_at")
        )


        if updated and updated >= cutoff:

            maintained += 1



    if maintained >= 8:
        return 20

    elif maintained >= 5:
        return 15

    elif maintained >= 3:
        return 10

    elif maintained >= 1:
        return 5


    return 0




# -------------------------
# Work Distribution
# -------------------------

def work_distribution_score(commits):

    if not commits:
        return 0


    months = set()


    for commit in commits:

        date = safe_parse_date(
            commit.get("date")
        )


        if date:

            months.add(
                date.strftime("%Y-%m")
            )



    active_months = len(months)



    if active_months >= 6:
        return 15

    elif active_months >= 4:
        return 10

    elif active_months >= 2:
        return 5


    return 0




# -------------------------
# Discipline Calculator
# -------------------------

def calculate_discipline(data):


    commits = data.get(
        "commits",
        []
    )


    repos = data.get(
        "repos",
        []
    )


    contributions = data.get(
        "contributions",
        {}
    )



    routine = commit_routine_score(
        commits
    )


    habit = contribution_habit_score(
        contributions
    )


    maintenance = maintenance_behavior_score(
        repos
    )


    distribution = work_distribution_score(
        commits
    )



    total = min(
        routine +
        habit +
        maintenance +
        distribution,
        100
    )


    return {

        "commit_routine": routine,

        "contribution_habit": habit,

        "maintenance": maintenance,

        "work_distribution": distribution,

        "total": total

    }

    
# =====================================================
# CRAFT SCORE
# Measures engineering quality and project maturity
# =====================================================

def documentation_quality_score(repos):

    if not repos:
        return 0


    documented = 0


    for repo in repos:

        has_description = bool(
            repo.get("description")
        )

        has_readme = repo.get(
            "has_readme",
            False
        )

        readme_length = repo.get(
            "readme_length",
            0
        )


        if (
            has_description
            and has_readme
            and readme_length > 100
        ):
            documented += 1



    ratio = documented / len(repos)



    if ratio >= 0.8:
        return 25

    elif ratio >= 0.6:
        return 20

    elif ratio >= 0.4:
        return 15

    elif ratio > 0:
        return 10


    return 0



def maintenance_quality_score(repos):

    if not repos:
        return 0


    quality = 0


    for repo in repos:

        score = 0


        if repo.get("license"):
            score += 1


        if repo.get("issues"):
            score += 1


        if repo.get("open_issues_count",0) > 0:
            score += 1


        if score >= 2:
            quality += 1



    ratio = quality / len(repos)


    if ratio >= 0.7:
        return 25

    elif ratio >= 0.5:
        return 20

    elif ratio >= 0.3:
        return 15

    elif ratio > 0:
        return 10


    return 0



def original_project_quality_score(repos):

    if not repos:
        return 0


    original = sum(
        1
        for repo in repos
        if not repo.get("fork",False)
    )


    ratio = original / len(repos)


    if ratio >= 0.8:
        return 25

    elif ratio >= 0.6:
        return 20

    elif ratio >= 0.4:
        return 15

    elif ratio > 0:
        return 10


    return 0



def project_depth_score(data):

    commits = data.get(
        "commits",
        []
    )


    if not commits:
        return 0


    count = len(commits)


    if count >= 100:
        return 25

    elif count >= 50:
        return 20

    elif count >= 20:
        return 15

    elif count >= 5:
        return 10


    return 5



def calculate_craft(data):

    repos = data.get(
        "repos",
        []
    )


    documentation = documentation_quality_score(
        repos
    )

    maintenance = maintenance_quality_score(
        repos
    )

    originality = original_project_quality_score(
        repos
    )

    depth = project_depth_score(
        data
    )


    total = min(
        documentation +
        maintenance +
        originality +
        depth,
        100
    )


    return {

        "documentation": documentation,

        "maintenance_quality": maintenance,

        "original_projects": originality,

        "project_depth": depth,

        "total": total
    }





# =====================================================
# INFLUENCE SCORE
# Measures external impact and recognition
# =====================================================


def star_impact_score(repos):

    total_stars = sum(
        repo.get("stars", 0)
        for repo in repos
    )


    if total_stars >= 50:
        return 25

    elif total_stars >= 20:
        return 20

    elif total_stars >= 10:
        return 15

    elif total_stars >= 5:
        return 10

    elif total_stars >= 1:
        return 5


    return 0



def fork_impact_score(repos):

    total_forks = sum(
        repo.get("forks", 0)
        for repo in repos
    )


    if total_forks >= 15:
        return 25

    elif total_forks >= 10:
        return 20

    elif total_forks >= 5:
        return 15

    elif total_forks >= 1:
        return 10


    return 0



def follower_presence_score(user):

    followers = (
        user.get("followers", {})
        .get("totalCount", 0)
        if isinstance(user.get("followers"), dict)
        else user.get("followers", 0)
    )


    if followers >= 100:
        return 20

    elif followers >= 20:
        return 15

    elif followers >= 5:
        return 10

    elif followers >= 1:
        return 5


    return 0


def reusable_project_score(repos):

    if not repos:
        return 0


    reusable = 0


    for repo in repos:

        score = 0


        if repo.get("stars",0) >= 5:
            score += 1


        if repo.get("forks",0) >= 2:
            score += 1


        if repo.get("description"):
            score += 1


        if repo.get("has_readme"):
            score += 1


        if score >= 3:
            reusable += 1



    ratio = reusable / len(repos)



    if ratio >= 0.5:
        return 30

    elif ratio >= 0.3:
        return 20

    elif ratio > 0:
        return 10


    return 0


def calculate_influence(data):

    repos = data["repos"]

    user = data["user"]


    stars = star_impact_score(
        repos
    )


    forks = fork_impact_score(
        repos
    )


    followers = follower_presence_score(
        user
    )


    reuse = reusable_project_score(
        repos
    )


    total = min(
        stars +
        forks +
        followers +
        reuse,
        100
    )


    return {

        "stars": stars,

        "forks": forks,

        "followers": followers,

        "project_reuse": reuse,

        "total": total
    }
# =====================================================
# INSIGHT SCORE
# Measures developer identity and technical direction
# =====================================================


def language_identity_score(repos):

    languages = {}


    for repo in repos:

        lang = repo.get("language")


        if lang:

            languages[lang] = (
                languages.get(lang,0)+1
            )


    if not languages:
        return 0


    count = len(languages)


    if count >= 6:
        return 25

    elif count >= 4:
        return 20

    elif count >= 2:
        return 15

    return 10



def specialization_score(repos):

    languages = {}


    for repo in repos:

        lang = repo.get("language")


        if lang:

            languages[lang] = (
                languages.get(lang,0)+1
            )


    if not languages:
        return 0


    highest = max(
        languages.values()
    )


    if highest >= 10:
        return 25

    elif highest >= 5:
        return 20

    elif highest >= 3:
        return 15


    return 10


def technology_growth_score(data):

    repos = data.get(
        "repos",
        []
    )


    details = data.get(
        "repository_details",
        []
    )


    topics = set()


    # Collect repository topics
    for item in details:

        for topic in item.get(
            "topics",
            []
        ):
            topics.add(topic)



    topic_count = len(topics)



    # Documentation signal
    documented_projects = sum(
        1
        for repo in repos
        if repo.get(
            "has_readme",
            False
        )
    )



    # README + topics together show technical maturity
    growth_signal = (
        topic_count +
        documented_projects
    )



    if growth_signal >= 15:
        return 25

    elif growth_signal >= 10:
        return 20

    elif growth_signal >= 5:
        return 15


    return 5


def project_variety_score(repos):

    if not repos:
        return 0


    original = sum(
        1
        for repo in repos
        if not repo.get("fork",False)
    )


    if original >= 10:
        return 25

    elif original >= 5:
        return 20

    elif original >= 2:
        return 15


    return 5



def calculate_insight(data):

    repos = data["repos"]


    identity = language_identity_score(
        repos
    )


    specialization = specialization_score(
        repos
    )


    technology = technology_growth_score(
        data
    )


    variety = project_variety_score(
        repos
    )


    total = min(
        identity +
        specialization +
        technology +
        variety,
        100
    )


    return {

        "language_identity": identity,

        "specialization": specialization,

        "technology_growth": technology,

        "project_variety": variety,

        "total": total
    }


# =====================================================
# RESOLVE SCORE
# Measures completion, maintenance and finishing ability
# =====================================================


def maintenance_score(repos):

    if not repos:
        return 0


    cutoff = datetime.now() - timedelta(days=180)

    maintained = 0


    for repo in repos:

        update_date = safe_parse_date(
            repo.get("updated_at")
        )


        if update_date and update_date >= cutoff:

            maintained += 1



    ratio = maintained / len(repos)



    if ratio >= 0.7:
        return 30

    elif ratio >= 0.5:
        return 25

    elif ratio >= 0.3:
        return 15

    elif ratio > 0:
        return 10


    return 0




# -------------------------
# Completion Score
# -------------------------

def completion_score(repos):

    if not repos:
        return 0


    completed = 0


    for repo in repos:

        has_description = bool(
            repo.get("description")
        )


        has_readme = repo.get(
            "has_readme",
            False
        )


        has_activity = bool(
            repo.get("updated_at")
        )


        # Better project completion signal
        if (
            has_description
            and has_activity
            and has_readme
        ):
            completed += 1



    ratio = completed / len(repos)



    if ratio >= 0.8:
        return 30

    elif ratio >= 0.5:
        return 25

    elif ratio >= 0.3:
        return 15

    elif ratio > 0:
        return 10


    return 0



# -------------------------
# Project Continuity
# -------------------------

def project_continuity_score(repos):

    if not repos:
        return 0


    active_projects = 0


    for repo in repos:

        created_date = safe_parse_date(
            repo.get("created_at")
        )

        updated_date = safe_parse_date(
            repo.get("updated_at")
        )


        if not created_date or not updated_date:
            continue



        lifespan = (
            updated_date - created_date
        ).days



        if lifespan >= 30:

            active_projects += 1



    ratio = active_projects / len(repos)



    if ratio >= 0.6:
        return 25

    elif ratio >= 0.4:
        return 20

    elif ratio >= 0.2:
        return 10


    return 0



# -------------------------
# Commit Follow Through
# -------------------------

def commit_followthrough_score(data):

    commits = data.get(
        "commits",
        []
    )


    if not commits:
        return 0



    count = len(commits)



    if count >= 200:
        return 15

    elif count >= 100:
        return 12

    elif count >= 30:
        return 8

    elif count >= 10:
        return 5


    return 0




# -------------------------
# Resolve Calculator
# -------------------------

def calculate_resolve(data):


    repos = data.get(
        "repos",
        []
    )


    maintenance = maintenance_score(
        repos
    )


    completion = completion_score(
        repos
    )


    continuity = project_continuity_score(
        repos
    )


    commits = commit_followthrough_score(
        data
    )



    total = min(
        maintenance +
        completion +
        continuity +
        commits,
        100
    )



    return {

        "maintenance": maintenance,

        "completion": completion,

        "project_continuity": continuity,

        "commit_followthrough": commits,

        "total": total

    }



# =====================================================
# ENGINEERING SIGNALS
# Supporting intelligence indicators
# =====================================================


def activity_signal(data):
    """
    Measures how active the repositories have been recently.
    Score is based on repositories updated within the last 180 days.
    """

    repos = data.get("repos", [])

    if not repos:
        return 0

    cutoff = datetime.now() - timedelta(days=180)

    active = 0

    for repo in repos:
        updated = safe_parse_date(repo.get("updated_at"))

        if updated and updated >= cutoff:
            active += 1

    score = round((active / len(repos))*70)

    if active >= 5:
        score += 20

    if active >= 10:
        score += 10

    return max(0, min(score, 100))


def project_depth_signal(data):

    repos = data.get("repos", [])

    if not repos:
        return 0


    total = 0


    for repo in repos:

        score = 0


        # Documentation foundation
        if repo.get("has_readme"):
            score += 15


        # Project explanation
        if repo.get("description"):
            score += 10


        # Community validation
        if repo.get("stars",0) > 0:
            score += 10

        if repo.get("forks",0) > 0:
            score += 10


        # Repository activity
        updated = safe_parse_date(repo.get("updated_at"))

        if updated:
            cutoff = datetime.now() - timedelta(days=180)

            if updated >= cutoff:
                score += 15


        # Repository complexity signals
        if repo.get("size",0) > 500:
            score += 15


        if repo.get("language"):
            score += 5


        if repo.get("topics"):
            score += 5


        total += min(score,100)


    return round(total / len(repos))




def language_range_signal(data):
    """
    Measures Technology Ecosystem.

    Evaluates:
    - Language diversity
    - Engineering domains
    - Technology concentration
    - Modern tooling
    - Technical specialization
    """

    raw_languages = data.get("languages", [])


    if not raw_languages:
        return 0



    languages = []

    for lang in raw_languages:

        if isinstance(lang, tuple):
            languages.append(lang[0].lower())

        else:
            languages.append(lang.lower())



    languages = list(set(languages))


    score = 0



    # ----------------------------
    # 1. Language Diversity (20)
    # ----------------------------

    count = len(languages)


    if count >= 8:
        score += 15

    elif count >= 5:
        score += 12

    elif count >= 3:
        score += 8

    else:
        score += 4



    # ----------------------------
    # 2. Engineering Domains (30)
    # ----------------------------

    domains = 0


    backend = {
        "python",
        "java",
        "go",
        "rust",
        "php",
        "c#"
    }


    frontend = {
        "javascript",
        "typescript",
        "html",
        "css"
    }


    data_ai = {
        "python",
        "jupyter notebook",
        "r"
    }


    systems = {
        "c",
        "c++",
        "rust"
    }


    devops = {
        "dockerfile",
        "shell"
    }



    if backend.intersection(languages):
        domains += 1


    if frontend.intersection(languages):
        domains += 1


    if data_ai.intersection(languages):
        domains += 1


    if systems.intersection(languages):
        domains += 1


    if devops.intersection(languages):
        domains += 1



    score += min(domains * 5, 20)



    # ----------------------------
    # 3. Technology Usage Spread (20)
    # ----------------------------

    repos = data.get("repos", [])


    used_languages = []


    for repo in repos:

        if repo.get("language"):
            used_languages.append(
                repo["language"].lower()
            )



    used_languages = list(set(used_languages))



    if len(used_languages) >= 6:
        score += 20

    elif len(used_languages) >= 4:
        score += 15

    elif len(used_languages) >= 2:
        score += 10



    # ----------------------------
    # 4. Modern Engineering Tools (20)
    # ----------------------------

    tools = {
        "dockerfile",
        "shell",
        "jupyter notebook",
        "typescript"
    }


    modern = len(
        tools.intersection(languages)
    )


    score += min(modern * 5,20)



    # ----------------------------
    # 5. Technical Direction (10)
    # ----------------------------

    if (
        "python" in languages
        and "jupyter notebook" in languages
    ):
        score += 10

    elif domains >= 3:
        score += 7


    # ----------------------------
    # Real ecosystem usage bonus
    # ----------------------------

    repos = data.get("repos", [])

    active_projects = 0

    for repo in repos:

        if (
            repo.get("description")
            or repo.get("stars",0) > 0
            or repo.get("topics")
        ):
            active_projects += 1


    if active_projects >= 10:
        score += 10

    elif active_projects >= 5:
        score += 5





    return max(0,min(round(score),95))




def documentation_signal(data):

    repos = data.get("repos", [])

    if not repos:
        return 0

    total = 0

    for repo in repos:

        score = 0

        if repo.get("has_readme"):
            score += 60

        if repo.get("description"):
            score += 25

        if repo.get("topics"):
            score += 15

        total += score


    return round(total / len(repos))


def get_rank(score):

    if score >= 85:
        return "Elite"

    elif score >= 65:
        return "Advanced"

    elif score >= 40:
        return "Consistent"

    elif score >= 20:
        return "Emerging"

    else:
        return "Dormant"



def calculate_signals(data):

    signals = {

        "activity": activity_signal(data),

        "project_depth": project_depth_signal(data),

        "language_range": language_range_signal(data),

        "documentation": documentation_signal(data)

    }


    ranks = {}

    for key, value in signals.items():

        ranks[key + "_rank"] = get_rank(value)


    signals.update(ranks)


    return signals


# =====================================================
# MAIN ANALYZER
# =====================================================


def analyze_profile(data):


    momentum = calculate_momentum(data)


    discipline = calculate_discipline(data)


    craft = calculate_craft(data)


    influence = calculate_influence(data)


    insight = calculate_insight(data)


    resolve = calculate_resolve(data)


    signals = calculate_signals(data)


    # Overall developer score
    overall = round(
        (
            momentum["total"] +
            discipline["total"] +
            craft["total"] +
            influence["total"] +
            insight["total"] +
            resolve["total"]
        ) / 6
    )


    return {

    "overall_score": overall,


    "stats": {

        "momentum": momentum,

        "discipline": discipline,

        "craft": craft,

        "influence": influence,

        "insight": insight,

        "resolve": resolve

    },


    "signals": signals

}

