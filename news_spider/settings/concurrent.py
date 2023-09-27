# -----------------------------------------------------------------------------
# CONCURRENT
# -----------------------------------------------------------------------------

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also author settings and docs
# DOWNLOAD_DELAY = 1 / CONCURRENT_REQUESTS
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS
# CONCURRENT_REQUESTS_PER_IP = 32