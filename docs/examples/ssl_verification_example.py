"""
Example: Using WikibaseIntegrator with Self-Signed SSL Certificates

This example demonstrates how to disable SSL certificate verification
when working with Wikibase instances using self-signed certificates
(e.g., in intranet or development environments).

WARNING: Disabling SSL verification reduces security. Only use this 
in trusted environments where you control the network.
"""

from wikibaseintegrator import wbi_login, wbi_config, WikibaseIntegrator
from wikibaseintegrator.wbi_helpers import execute_sparql_query, download_entity_ttl

# ====================================================================================
# Method 1: Using verify parameter in login classes (Recommended for authenticated use)
# ====================================================================================

# This method is recommended when you need to authenticate with the Wikibase instance.
# The verify setting will be stored in the session and used for all API calls.

# Example with Clientlogin (username/password authentication)
login = wbi_login.Clientlogin(
    user='YourUsername',
    password='YourPassword',
    mediawiki_api_url='https://your-intranet-wikibase.local/w/api.php',
    verify=False  # Disable SSL certificate verification
)

# Use the login with WikibaseIntegrator
wbi = WikibaseIntegrator(login=login)

# All API calls through this WikibaseIntegrator instance will now respect
# the verify=False setting from the login

# ====================================================================================
# Method 2: Using global config (For application-wide setting)
# ====================================================================================

# At the start of your application, set the global config
wbi_config.config['VERIFY_SSL'] = False

# Now all operations will use verify=False by default

# ====================================================================================
# Method 3: Per-call override (Most flexible)
# ====================================================================================

# Example: SPARQL query with explicit verify parameter
results = execute_sparql_query(
    query='SELECT * WHERE { ?s ?p ?o } LIMIT 10',
    endpoint='https://your-intranet-wikibase.local/query/sparql',
    verify=False  # Override for this specific call
)

# Example: Download TTL with explicit verify parameter
ttl_content = download_entity_ttl(
    entity='Q42',
    wikibase_url='https://your-intranet-wikibase.local',
    verify=False  # Override for this specific call
)
