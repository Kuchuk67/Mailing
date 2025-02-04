from django.shortcuts import redirect, render
from django.views import View

class AnaliticView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mailing/index.html',
                      {'count_all': "json_mail.count_all", 'count_error': "json_mail.count_error"})