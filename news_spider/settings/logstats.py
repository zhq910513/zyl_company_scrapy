from . import EXTENSIONS

EXTENSIONS.update({
    'scrapy.extensions.logstats.LogStats': None,
    'scrapy_extensions.extensions.logstats.LogStats': 0,
})

# -----------------------------------------------------------------------------
# SCRAPY_LOG
# -----------------------------------------------------------------------------
# LOGSTATS_CACHE_ENABLED = True
# LOGSTATS_CACHE_INTERVAL = 30
# LOGSTATS_CACHE_STORAGE = 'scrapy_log.storages.influxdb_storage.InfluxDBCacheStorage'
#
# INFLUXDB_HOST = '10.255.255.249'
# INFLUXDB_PORT = 8086
# INFLUXDB_DATABASE = 'test'
# INFLUXDB_MEASUREMENT = 'yelu'
#
# EXTENSIONS.update({
#     'scrapy_log.extensions.logstats.LogStatsCache': 900
# })
