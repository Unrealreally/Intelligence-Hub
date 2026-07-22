from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.fast_collector import collect_fast_profile
from modules.collector import collect_deep_profile
from modules.analysis import analyze_profile

app = FastAPI(title="Intelligence Hub")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def empty_profile(username: str) -> dict:
    return {
        "username": username,

        "bio": "Developer footprint generated from GitHub activity patterns.",

        "stats": {
            "repositories": 0,
            "original_projects": 0,
            "stars": 0,
            "forks": 0,
        },

        "languages": [],

        "repos": [],
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None,
            "profile": None,
            "search_query": "",
        },
    )
# =====================================================
# STAGE 1 FAST PROFILE
# =====================================================


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(

    request: Request,

    username: str = Form(...)

):


    username = username.strip()



    collected = collect_fast_profile(
        username
    )



    if (

        not isinstance(collected, dict)

        or collected.get("success") is False

    ):


        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "error":
                collected.get(
                    "error",
                    "Unable to find profile"
                ),

                "profile": None,

                "search_query": username
            }

        )



    profile = collected



    return templates.TemplateResponse(

        request=request,

        name="profile.html",

        context={

            "profile": profile,

            "scores": None,

            "deep_analysis": False

        }

    )



# =====================================================
# STAGE 2 DEEP ANALYSIS
# =====================================================


@app.post(
    "/deep-analysis",
    response_class=HTMLResponse
)

async def deep_analysis(
    request: Request,
    username: str = Form(...)
):

    username = username.strip()

    collected = collect_deep_profile(username)



    if (

        not isinstance(collected, dict)
        or not collected.get("success")

    ):


        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "error":
                "Deep analysis failed",

                "profile": None,

                "search_query": username

            }

        )



    scores = analyze_profile(
        collected
    )



    return templates.TemplateResponse(

        request=request,

        name="profile.html",

        context={

            "profile": collected,

            "scores": scores,

            "deep_analysis": True

        }

    )


# =====================================================
# ALL REPOSITORIES
# =====================================================

@app.get(
    "/repositories/{username}",
    response_class=HTMLResponse
)
async def repositories(
    request: Request,
    username: str
):

    profile = collect_fast_profile(
        username
    )


    if not profile.get("success"):

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error":"Unable to load repositories",
                "profile":None,
                "search_query":username
            }
        )


    return templates.TemplateResponse(
        request=request,
        name="repo.html",
        context={
            "profile":profile
        }
    )

# =====================================================
# PROFILE PAGE
# =====================================================

@app.get(
    "/profile/{username}",
    response_class=HTMLResponse
)
async def profile_page(
    request: Request,
    username: str
):

    profile = collect_deep_profile(
        username
    )


    if not profile.get("success"):

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": "Unable to load profile",
                "profile": None,
                "search_query": username
            }
        )


    scores = analyze_profile(
        profile
    )


    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "profile": profile,
            "scores": scores,
            "deep_analysis": True
        }
    )