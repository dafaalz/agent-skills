# CLI introspection and runtime discovery

Inspect the Laravel application using native terminal commands. Execute these commands using shell execution tools before proposing schema changes, modifying controllers, or writing queries.

## Discovery commands

Execute the narrowest relevant command to inspect state without guessing:

```bash
# Check Laravel version, PHP version, cache, and driver configuration
php artisan about

# Inspect database connection and table summary
php artisan db:show

# Inspect specific table schema, columns, attributes, and foreign keys
php artisan db:table users

# Inspect Eloquent model attributes, relationships, scopes, and casts
php artisan model:show User

# Filter registered routes by controller or URL fragment
php artisan route:list --path=api/v1 --except-vendor

# Inspect queued jobs or batches
php artisan queue:monitor default

# Run isolated PHP expressions within application context
php artisan tinker --execute="dump(App\Models\User::first()?->toArray());"
```

## Boost MCP detection

Before running CLI commands, check whether the project has Laravel Boost active:

1. Check if the `search-docs` tool is registered in your available tools.
2. If `search-docs` is present, use it to query version-specific framework documentation and packages.
3. If `search-docs` is absent, use the native CLI commands above and read vendor files directly when API contracts require verification.

## Log analysis

Inspect application logs directly when debugging errors:

```bash
# View the most recent application exceptions
tail -n 100 storage/logs/laravel.log

# Clear logs before reproducing an issue
truncate -s 0 storage/logs/laravel.log
```
