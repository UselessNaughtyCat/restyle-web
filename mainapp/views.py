from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse

from mainapp.models import Style, Site

def hello(request):
    return HttpResponse("U EXPECT SOME HELLO SHIT?<BR><H1>GTFO</H1>")

class MainView(TemplateView):
    template_name = "mainpage.html"

class SiteListView(TemplateView):
    template_name = "site_catalog.html"

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context["sites"] = Site.objects.all()
        return context

class StyleListView(TemplateView):
    template_name = "style_catalog.html"
    site_name = None

    def get(self, request, *args, **kwargs):
        if not self.kwargs["site_name"] is None:
            self.site_name = self.kwargs["site_name"]

        return super(StyleListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleListView, self).get_context_data(**kwargs)
        if self.site_name:
            curr_site = Site.objects.get(name=self.site_name)
            context['styles'] = Style.objects.filter(site=curr_site)
        else:
            context['styles'] = Style.objects.all()

        return context

class StyleInfoView(TemplateView):
    template_name = "style_info.html"
    style = None
    is_self_person = False

    def get(self, request, *args, **kwargs):
        self.style = Style.objects.get(id=self.kwargs["style_id"])
        if not request.user is None:
            self.is_self_person = request.user == self.style.creator
        return super(StyleInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleInfoView, self).get_context_data(**kwargs)
        context['style'] = self.style
        context['is_self_person'] = self.is_self_person
        return context

class PersonInfoView(TemplateView):
    template_name = "person_info.html"
    curr_user = None
    is_self_person = False

    def get(self, request, *args, **kwargs):
        self.curr_user = User.objects.get(id=self.kwargs["person_id"])
        if not request.user is None:
            self.is_self_person = request.user == self.curr_user
        return super(PersonInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonInfoView, self).get_context_data(**kwargs)
        context['curr_user'] = self.curr_user
        context['curr_user_subs'] = self.curr_user.person.subscriptions.all()
        context['curr_user_works'] = Style.objects.filter(creator=self.curr_user)
        context['is_self_person'] = self.is_self_person
        return context