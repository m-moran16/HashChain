from django.db import models
from django.utils import timezone
from .hashing import compute_hash


class AuditEntry(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    actor = models.CharField(max_length=150)
    action = models.Charfield(max_length=150)
    details = models.JSONField
    previous_hash = models.CharField(max_length=64, blank=True)
    current_hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Audit entries are append only and cannot be changed.")
        last = AuditEntry.objects.order_by(-id).first()
        self.previous_hash = last.current_hash if last else ""
        self.current_hash = compute_hash(
            self.previous_hash,
            self.timestamp,
            self.actor,
            self.action,
            self.details,
        )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Audits are append only and cannot be deleted.")

    def __str__(self):
        return f"{self.timestamp.isoformat()} {self.actor} {self.action}"
    