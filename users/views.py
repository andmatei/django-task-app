from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout, authenticate, login


class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        username = "user"
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get("next", reverse("index")))
        else:
            return render(
                request, "users/login.html", {"errors": "Invalid username or password"}
            )
