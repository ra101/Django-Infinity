from django.db.models import query, signals


class GhostQuerySet(query.QuerySet):
    """
    QuerySet for GhostManager
    """

    def delete(self):
        """
        `ghost` the object, so it can resurrected later.
        """

        self.update(alive=False)
        for obj in self:
            signals.post_delete.send(sender=obj.__class__, instance=obj)

    def annihilate(self):
        """
        Permanently delete all the objects in queryset.
        """

        return super().delete()

    def resurrect(self):
        """
        Restore all the `ghosted` all the objects in queryset.
        """

        self.update(alive=True)
