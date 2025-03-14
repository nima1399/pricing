from django.contrib import admin

from crawler.models import (
    CrawlConfig,
    CrawlSource,
    User,
    ValuableGroup,
    ValuableObject,
    ValuableRecord,
)


@admin.register(ValuableObject)
class ValuableObjectAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "group")
    search_fields = ("title", "description")
    list_filter = ("group",)
    actions = ["delete_selected"]


@admin.register(ValuableGroup)
class ValuableGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")
    actions = ["delete_selected"]


@admin.register(ValuableRecord)
class ValuableRecordAdmin(admin.ModelAdmin):
    list_display = ("crawl_config", "date", "value")
    search_fields = ("crawl_config__valuable_object__title", "value")
    list_filter = ("date",)
    actions = ["delete_selected"]


@admin.register(CrawlConfig)
class CrawlConfigAdmin(admin.ModelAdmin):
    list_display = ("crawl_source", "valuable_object", "priority")
    search_fields = ("crawl_source__title", "valuable_object__title")
    list_filter = ("priority",)
    actions = ["delete_selected"]


@admin.register(CrawlSource)
class CrawlSourceAdmin(admin.ModelAdmin):
    list_display = ("title", "base_url", "is_valid", "type")
    search_fields = ("title", "base_url")
    list_filter = ("is_valid", "type")
    actions = ["delete_selected"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "get_subscribed_valuables")
    search_fields = ("email", "subscribed_valuables__title")
    actions = ["delete_selected"]

    def get_subscribed_valuables(self, obj):
        return ", ".join(
            [
                valuable.title
                for valuable in obj.subscribed_valuables.all()
                if not valuable.is_deleted
            ]
        )

    get_subscribed_valuables.short_description = "Subscribed Valuables"
