from django.views.generic import *
from certificates.models import *
from mainsite.views import ActiveTabMixin

import json

class CertificateCreate(ActiveTabMixin, CreateView):
    model = Certificate
    active_tab = 'certificates'
    

class CertificateDetail(ActiveTabMixin, DetailView):
    model = Certificate
    active_tab = 'certificates'
    # analysis = json.dumps(analyze_image_upload(object.image))

    def get_context_data(self, **kwargs):
    	context = super(CertificateDetail, self).get_context_data(**kwargs)
    	context['analysis'] = json.dumps(analyze_image_upload()



