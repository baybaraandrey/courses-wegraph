import uuid

from django.db.models import (
    CharField,
    DateTimeField,
    JSONField,
    UUIDField,
)

from model_utils.models import TimeStampedModel


class DelayedTask(TimeStampedModel):
    uid = UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )

    task_type = CharField(
        db_index=True,
        max_length=256,
        null=False,
        blank=False,
    )
    status = CharField(
        db_index=True,
        max_length=256,
        null=False,
        blank=False,
    )
 

    eta = DateTimeField(
        db_index=True,
        null=False,
        blank=False,
    )

    def __repr__(self):
        return 'DelayedTask(id=%d, task_type="%s", status="%s", eta="%s")' % (
            self.id,
            self.task_type,
            self.status,
            self.eta,
        )

    def __str__(self):
        return self.__repr__()
