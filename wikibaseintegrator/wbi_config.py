"""
Config global options
Options can be changed at run time. See tests/test_backoff.py for usage example

Options:
BACKOFF_MAX_TRIES: maximum number of times to retry failed request to wikidata endpoint.
                   Default: None (retry indefinitely)
                   To disable retry, set value to 1
BACKOFF_MAX_VALUE: maximum number of seconds to wait before retrying. wait time will increase to this number
                   Default: 3600 (one hour)
USER_AGENT:        Complementary user agent string used for http requests. Both to Wikibase api, query service and others.
                   See: https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy
VERIFY_SSL:        Whether to verify SSL certificates for HTTPS requests. Set to False to disable verification (e.g., for self-signed certificates).
                   Default: None (uses requests library default behavior - verify=True)
                   Note: For authenticated requests, the verify parameter passed to login classes takes precedence.
"""

from typing import Union

config: dict[str, Union[str, int, None, bool]] = {
    'BACKOFF_MAX_TRIES': 5,
    'BACKOFF_MAX_VALUE': 3600,
    'USER_AGENT': None,
    'PROPERTY_CONSTRAINT_PID': 'P2302',
    'DISTINCT_VALUES_CONSTRAINT_QID': 'Q21502410',
    'COORDINATE_GLOBE_QID': 'http://www.wikidata.org/entity/Q2',
    'CALENDAR_MODEL_QID': 'http://www.wikidata.org/entity/Q1985727',
    'MEDIAWIKI_API_URL': 'https://www.wikidata.org/w/api.php',
    'MEDIAWIKI_INDEX_URL': 'https://www.wikidata.org/w/index.php',
    'MEDIAWIKI_REST_URL': 'https://www.wikidata.org/w/rest.php',
    'SPARQL_ENDPOINT_URL': 'https://query.wikidata.org/sparql',
    'WIKIBASE_URL': 'http://www.wikidata.org',
    'DEFAULT_LANGUAGE': 'en',
    'DEFAULT_LEXEME_LANGUAGE': 'Q1860',
    'VERIFY_SSL': None  # None = use requests default, True = verify, False = don't verify
}
