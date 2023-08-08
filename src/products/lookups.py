from django.contrib.postgres.fields import ArrayField
from django.db.models import Lookup


@ArrayField.register_lookup
class ArrayIContains(Lookup):
    """
    Without it I'd be forsed to use `.extra()` method::

        class Foo(models.Model):
            values = ArrayField(base_field=models.CharField(max_length=255))

        >>> value = "bar"
        >>> Foo.objects.extra(
        ...     where=['%s ILIKE ANY (values)'],
        ...     params=[value],
        ... )
    """

    lookup_name = "icontains"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = rhs_params + lhs_params

        return "%s ILIKE ANY(%s)" % (rhs, lhs), params
