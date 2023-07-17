from django.db.models import Lookup, CharField
from django.db.models.functions import Cast


class ArrayIContains(Lookup):
    lookup_name = "icontains"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = rhs_params + lhs_params
        
        rhs = Cast(rhs, CharField())
        
        return "%s ILIKE ANY(%s)" % (rhs, lhs), params
