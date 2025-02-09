from django.contrib import admin

# Register your models here.
from crawler.models import (
    ValuableObject,
    ValuableGroup,
    ValuableRecord,
    CrawlConfig,
    CrawlSource,
)

admin.site.register(ValuableObject)
admin.site.register(ValuableGroup)
admin.site.register(ValuableRecord)
admin.site.register(CrawlConfig)
admin.site.register(CrawlSource)
