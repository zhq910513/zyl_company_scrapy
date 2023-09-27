import logging

LOG_LEVEL = logging.INFO


# project_root = PurePosixPath(os.path.dirname(__file__)).parent
#
# client = Client(dsn=(
#     'http://'  # scheme
#     '2331abeeb88243c18814e97d4f324533:'  # username
#     'dac484c71a5c4b5aac7d7f0e819155cb@'  # password
#     'sentry.socialbird.cn:9000'  # netloc
#     '/18'),  # path
#     # inform the client which parts of code are yours
#     # include_paths=['my.app']
#     # include_paths=[__name__.split('.', 1)[0]],
#
#     # release=raven.fetch_git_sha(str(project_root))
# )
#
# client.logger.setLevel(logging.WARNING)
#
# handler = SentryHandler(client)
#
# handler.setLevel(logging.INFO)
#
# setup_logging(handler)
