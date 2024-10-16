from django.db import models


class StreamBlockSignatureBlocks(models.Model):
    """Store the signatures for the HTML blocks."""

    signature = models.CharField(max_length=255, unique=True)
    block_name = models.CharField(max_length=255)
    block_kwargs = models.JSONField(blank=True, null=True)
    model = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.signature

    class Meta:
        verbose_name_plural = "Stream Block Signature Blocks"
        ordering = ["signature"]
