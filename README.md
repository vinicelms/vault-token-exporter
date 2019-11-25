# Vault Token Expire Time Exporter
Monitor tokens used in applications as token service, returning the time for the token to expire.

This project collects information stored in a Vault entry, collecting the token and checking how long it takes for the key to expire.

## How to use

The project has as a premise to analyze information already available, allowing you to have control of what will be verified.

This way the service token is stored in the vault securely, allowing it to be updated if necessary and no sensitive information is exposed.

This will require 2 perspectives of information:
1. **Vault information**
- Vault Access URL
- Vault Access Token
- Entry where keys are located
  - The data is stored in a secret engine as Key/Value
2. **Mapeamento de informações** (map entry with keys that will be used)
- Key name where Token is stored
- Key name where Token display name is stored (optional)

> If the Token display name is not entered, it will default to **display_name** when the key was created

Summing up the process that the code will perform:
1. Get settings (either through file or environment variables)
2. Lists entries defined with the "entry_location" setting
3. Read each listing entry returned in step 2
4. Collect the value of the "entry_map_token" setting to get the token to check.
5. If "entry_map_name" is set, it will be named.
6. Collects the token information returned in step 3, returning the time to expire the token and also the "display_name" if the "entry_map_name" setting has not been set.

### Externalization of settings

You can use information loading in two ways:
- Environment variables
- Using a file named "config.ini"

Environment variables have preference for settings.

#### Environment variables

- VAULT_URL
- VAULT_TOKEN
- VAULT_ENTRY_LOCATION
- VAULT_ENTRY_MAP_NAME
- VAULT_ENTRY_MAP_TOKEN

To do this, run (Linux):
```
export VAULT_URL=https://myvault.example.com
export VAULT_TOKEN=my_token_to_access_key_value_secret
export VAULT_ENTRY_LOCATION=secret_name/entry_location
export VAULT_ENTRY_MAP_NAME=reference_to_key_with_display_name
export VAULT_ENTRY_MAP_TOKEN=reference_to_key_with_token
```

#### Configuration file

The file name must be **config.ini**. File configuration example:
```
[vault]
url=https://myvault.example.com
token=my_token_to_access_key_value_secret
entry_location=secret_name/entry_location

[entry_map]
name=reference_to_key_with_display_name
token=reference_to_key_with_token
```