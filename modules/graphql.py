import requests

from config import GRAPHQL_API, HEADERS



# =====================================================
# GRAPHQL REQUEST HANDLER
# =====================================================

def graphql_request(query, variables=None):

    try:

        response = requests.post(
            GRAPHQL_API,
            json={
                "query": query,
                "variables": variables
            },
            headers=HEADERS,
            timeout=15
        )


    except requests.RequestException as e:

        return {

            "success": False,

            "error": str(e)

        }



    if response.status_code != 200:

        return {

            "success": False,

            "error":
            f"HTTP Error {response.status_code}"

        }



    data = response.json()



    if data.get("errors"):

        return {

            "success": False,

            "error":
            data["errors"]

        }



    return {

        "success": True,

        "data": data

    }





# =====================================================
# CONTRIBUTION INTELLIGENCE
# =====================================================


def get_contribution_data(username):


    query = """

    query($username:String!) {


        user(login:$username) {


            contributionsCollection {


                totalCommitContributions


                totalIssueContributions


                totalPullRequestContributions


                totalRepositoryContributions



                contributionCalendar {


                    totalContributions



                    weeks {


                        contributionDays {


                            contributionCount


                            date


                        }

                    }

                }

            }

        }

    }

    """



    return graphql_request(

        query,

        {
            "username":username
        }

    )






# =====================================================
# USER PROFILE INTELLIGENCE
# =====================================================


def get_profile_data(username):


    query = """

    query($username:String!) {


        user(login:$username) {


            login


            name


            bio


            createdAt



            followers {

                totalCount

            }



            following {

                totalCount

            }



            repositories(
                first:100,
                ownerAffiliations:OWNER
            ) {


                totalCount



                nodes {


                    name


                    stargazerCount


                    forkCount



                    primaryLanguage {


                        name

                    }


                }

            }


        }


    }


    """



    return graphql_request(

        query,

        {
            "username":username
        }

    )






# =====================================================
# ADVANCED DEVELOPER SIGNALS
# =====================================================


def get_developer_metrics(username):


    query = """

    query($username:String!) {


        user(login:$username) {


            createdAt



            contributionsCollection {


                totalCommitContributions


                totalIssueContributions


                totalPullRequestContributions


                totalRepositoryContributions


            }



            repositories(
                first:100,
                ownerAffiliations:OWNER
            ){


                totalCount



                nodes{


                    name


                    stargazerCount


                    forkCount



                    isFork



                    createdAt


                    updatedAt



                    primaryLanguage {


                        name

                    }



                }

            }



        }


    }

    """



    return graphql_request(

        query,

        {
            "username":username
        }

    )






# =====================================================
# REPOSITORY DATA
# =====================================================


def get_repositories(username):


    query = """

    query($username:String!) {


        user(login:$username) {


            repositories(
                first:100,
                ownerAffiliations:OWNER
            ){


                nodes{


                    name


                    description



                    createdAt


                    updatedAt



                    stargazerCount



                    forkCount



                    isFork



                    primaryLanguage {


                        name

                    }


                }


            }


        }


    }


    """



    return graphql_request(

        query,

        {
            "username":username
        }

    )