from django.db import models
import uuid


class ResourceModel(models.Model):
    """
        An abstract base class model that provides self-managed `id`, `is_deleted`, `created_at` and
        `updated_at` fields.
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name="Public Identifier")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Products(ResourceModel):
    """
        This table contains the products of ACME LtD
        with `sku` being a unique field.
    """
    name = models.TextField(null=True, blank=True)
    sku = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
