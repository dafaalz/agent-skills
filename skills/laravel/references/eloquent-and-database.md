# Eloquent and database performance

Follow these patterns when designing models, writing migrations, or executing queries.

## Preventing N+1 queries

Always eager load relationships before iterating over collections.

Iterating over models without eager loading triggers an N+1 query cascade:

```php
$orders = Order::all();
foreach ($orders as $order) {
    echo $order->customer->name;
}
```

Eager load relationships to fetch records in two queries:

```php
$orders = Order::with('customer')->get();
foreach ($orders as $order) {
    echo $order->customer->name;
}
```

When selecting specific columns on relationships, include foreign keys and primary keys needed for matching:

```php
$users = User::with([
    'posts' => fn ($query) => $query->select('id', 'user_id', 'title', 'created_at')
])->get();
```

Enforce strict lazy loading protection in `app/Providers/AppServiceProvider.php`:

```php
public function boot(): void
{
    Model::preventLazyLoading(! app()->isProduction());
}
```

## Large dataset processing

Process large datasets using chunking or lazy streams instead of loading entire tables into memory with `all()` or `get()`:

```php
// For updates where records remain in query scope
Order::where('status', 'pending')->chunkById(200, function ($orders) {
    foreach ($orders as $order) {
        $order->markAsProcessed();
    }
});

// For memory-efficient read streams
foreach (User::cursor() as $user) {
    $user->generateMonthlyInvoice();
}
```

## Database migrations and indexing

Index columns used in `WHERE`, `ORDER BY`, and foreign keys. Define foreign keys with explicit cascade actions:

```php
Schema::create('orders', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->string('reference')->unique();
    $table->string('status')->index();
    $table->unsignedInteger('amount_cents');
    $table->timestamps();
});
```

Always use standard Blueprint types:
- `unsignedInteger` or `unsignedBigInteger` for financial cents or positive counters.
- `decimal('amount', 12, 2)` for currency when exact decimal arithmetic is required.
- `json` or `jsonb` for dynamic metadata, with validation enforced at the Form Request layer.

## Eloquent casts and attributes

Declare explicit casts using the `casts()` method instead of property arrays in modern Laravel:

```php
protected function casts(): array
{
    return [
        'email_verified_at' => 'datetime',
        'is_active' => 'boolean',
        'metadata' => 'immutable_array',
        'role' => UserRole::class,
    ];
}
```
