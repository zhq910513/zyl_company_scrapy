# -----------------------------------------------------------------------------
# AUTOTHROTTLE
# -----------------------------------------------------------------------------

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

DOWNLOAD_FAIL_ON_DATALOSS = False

MEDIA_ALLOW_REDIRECTS = True