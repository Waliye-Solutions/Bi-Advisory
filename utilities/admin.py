from django.contrib import admin
from django.contrib.sites.models import Site

from django_summernote.models import Attachment
from hitcount.models import HitCount, Hit, BlacklistIP, BlacklistUserAgent

# no need to register Attachment model in admin since it's only used for storing uploaded files from Summernote editor 
# and doesn't require any custom admin interface or management.
admin.site.unregister(Attachment)

# no need to register HitCount, Hit, BlacklistIP, and BlacklistUserAgent models in admin since they are only used for tracking and managing 
# hits and blacklists for the hitcount app and don't require any custom admin interface or management.
admin.site.unregister(HitCount)
admin.site.unregister(Hit)
admin.site.unregister(BlacklistIP)
admin.site.unregister(BlacklistUserAgent)


# no need to register Site model in admin since it's only used for managing multiple sites in a Django project and doesn't require any 
# custom admin interface or management.
admin.site.unregister(Site)
