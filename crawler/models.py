from django.db import models
from django.utils import timezone

from core.manager import ActiveManager


# Create your models here.
class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.delete_date = timezone.now()
        self.save()


class ValuableGroup(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class ValuableObject(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(ValuableGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CrawlSourceType(models.TextChoices):
    WS = "ws", "WebSocket"
    TOKEN = "token", "Token"


class CrawlSource(BaseModel):
    title = models.CharField(max_length=255)
    base_url = models.URLField()
    config_string = models.TextField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=CrawlSourceType.choices)

    def __str__(self):
        return self.title


class CrawlConfig(BaseModel):
    crawl_source = models.ForeignKey(CrawlSource, on_delete=models.CASCADE)
    valuable_object = models.ForeignKey(ValuableObject, on_delete=models.CASCADE)
    helper_data = models.JSONField(null=True, blank=True)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.crawl_source.title} - {self.valuable_object.title}"

    def get_url(self):
        return list(self.helper_data.keys())[0]

    def increase_priority(self):
        self.priority += 1


class ValuableRecord(BaseModel):
    crawl_config = models.ForeignKey(CrawlConfig, on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.crawl_config.crawl_source.title} - {self.crawl_config.valuable_object.title}"
