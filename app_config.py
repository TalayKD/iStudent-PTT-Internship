from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from oauthlib.oauth2 import WebApplicationClient

############################
### AZURE AD CREDENTIALS ###
############################

CLIENT_ID = "17a73d29-860a-42d1-a07c-6db374d66334" # Application (client) ID of app registration

CLIENT_SECRET = "VcF8Q~2XE5E7HiRYcqMfO1vfA1pAhw85LUlFda8n" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

TENANT_ID = "381c23e7-37f0-412f-9372-a26ddda2b784"

# AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

##############################
### Config Azure Key Vault ###
##############################

KEYVAULT_NAME = "pttinternship"
KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"

_credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# _sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
# db_username = _sc.get_secret("istudent-db-username").value
# db_password = _sc.get_secret("istudent-db-password").value
# db_host = _sc.get_secret("istudent-db-host").value
# google_id = _sc.get_secret("google-client-id").value
# google_secret = _sc.get_secret("google-client-secret").value

###########################
### Config Google Login ###
###########################

GOOGLE_CLIENT_ID = "449626336870-g4enfj3de8lqudmlmg6tm43ukisopmae.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# OAuth2 client setup
clientGoogle = WebApplicationClient(GOOGLE_CLIENT_ID)
