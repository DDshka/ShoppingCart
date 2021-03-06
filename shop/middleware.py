from django.db import connection
import logging

logger = logging.getLogger(__name__)


class QueryCountDebugMiddleware(object):
  """
  This middleware will log the number of queries run
  and the total time taken for each request (with a
  status code of 200). It does not currently support
  multi-db setups.
  """

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # some stuff is done before the view is called
    response = self.get_response(request)
    # some stuff is done after the view is called
    self.process_response(request, response)

    return response

  def process_response(self, request, response):
    if response.status_code == 200:
      total_time = 0

      for query in connection.queries:
        query_time = query.get('time')
        if query_time is None:
          # django-debug-toolbar monkeypatches the connection
          # cursor wrapper and adds extra information in each
          # item in connection.queries. The query time is stored
          # under the key "duration" rather than "time" and is
          # in milliseconds, not seconds.
          query_time = query.get('duration', 0)
        total_time += float(query_time)

      message = '{} queries run, total {:f} seconds'.format(len(connection.queries), total_time)
      logger.debug(message)
    return response