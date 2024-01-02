from django.http import HttpResponse
import os
from django.conf import settings
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
from requests_oauthlib import OAuth2Session
import json
from django.shortcuts import render

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
oauth = OAuth2Session(CLIENT_ID,
  redirect_uri="http://127.0.0.1:8000/kefilwe/complete/ion/",
  scope=["read","write"])
authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

def index(request):
  # return HttpResponse('<a href="%s">Login with Ion</a>' % authorization_url)
  # return render(request, "login.html", {"authorization_url": authorization_url})
  return render(request, "kefilwe/login.html", {"authorization_url": authorization_url})

def complete(request):
  CODE = request.GET.get("code")
  token = oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/",
    code=CODE, 
    client_secret=CLIENT_SECRET)

  try:
    profile = oauth.get("https://ion.tjhsst.edu/api/profile")
  except TokenExpiredError as e:
    args = { "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET }
    token = oauth.refresh_token("https://ion.tjhsst.edu/oauth/token/", **args)


  # return HttpResponse("Welcome to TJMaps, %s!" % json.loads(profile.content.decode())["short_name"])
  return render(request, "kefilwe/home.html", {"name": json.loads(profile.content.decode())["short_name"]})