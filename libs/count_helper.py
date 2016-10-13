from django.db import connection
from django.db import models
from django.db import connections


class ApproxCountPgQuerySet(models.query.QuerySet):
  """approximate unconstrained count(*) with reltuples from pg_class"""

  def count(self):
      if self._result_cache is not None and not self._iter:
          return len(self._result_cache)

      cursor = connections[self.db].cursor()
      if hasattr(connections[self.db].client.connection, 'pg_version'):
          query = self.query
          # not query.where and
          if (query.high_mark is None and query.low_mark == 0 and
              not query.select and not query.group_by and not query.having and not query.distinct):
              # If query has no constraints, we would be simply doing
              # "SELECT COUNT(*) FROM foo". Monkey patch so the we get an approximation instead.
              parts = [p.strip('"') for p in self.model._meta.db_table.split('.')]
              if len(parts) == 1:
                  cursor.execute("select reltuples::bigint FROM pg_class WHERE relname = %s", parts)
              else:
                  cursor.execute("select reltuples::bigint FROM pg_class c JOIN pg_namespace n on (c.relnamespace = n.oid) WHERE n.nspname = %s AND c.relname = %s", parts)

          return cursor.fetchall()[0][0]
      return self.query.get_count(using=self.db)

def estimate_count_fast(type):
    ''' postgres really sucks at full table counts, this is a faster version
    see: http://wiki.postgresql.org/wiki/Slow_Counting '''
    cursor = connection.cursor()
    cursor.execute("select reltuples from pg_class where relname='segmentation_%s';" % type)
    row = cursor.fetchone()
    return int(row[0])
