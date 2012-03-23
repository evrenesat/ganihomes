from django.db import connection
import time

class SqlProfilingMiddleware(object):
    Queries = []

    def process_request(self, request):
        return None
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    def process_template_response(self, request, response):
        self._add_sql_queries(request)
        return response
    def process_response(self, request, response):
        self._add_sql_queries(request)
        return response
    def process_exception(self, request, exception):
        return None

    def _add_sql_queries(self, request):
        for q in connection.queries:
            q["time"] = time.time() + float(q["time"])
            SqlProfilingMiddleware.Queries.insert(0, q)
            # add request info as a separator
        SqlProfilingMiddleware.Queries.insert(0, {"time": time.time(), "path" : request.path})
