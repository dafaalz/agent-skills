# Testing patterns and assertions

Write automated tests before or alongside application logic. Detect whether the project uses Pest or PHPUnit by inspecting `tests/Pest.php` or `phpunit.xml`.

## HTTP feature tests

Test endpoints from HTTP entry to database assertion:

### Pest syntax

```php
it('creates an article when input is valid', function () {
    $author = User::factory()->create();

    $response = $this->actingAs($author)->postJson('/api/v1/articles', [
        'title' => 'Building deep modules',
        'slug' => 'building-deep-modules',
        'body' => 'Content body',
        'category_id' => Category::factory()->create()->id,
    ]);

    $response->assertCreated()
        ->assertJsonPath('data.title', 'Building deep modules');

    $this->assertDatabaseHas('articles', [
        'slug' => 'building-deep-modules',
        'user_id' => $author->id,
    ]);
});
```

### PHPUnit syntax

```php
public function test_creates_article_when_input_is_valid(): void
{
    $author = User::factory()->create();

    $response = $this->actingAs($author)->postJson('/api/v1/articles', [
        'title' => 'Building deep modules',
        'slug' => 'building-deep-modules',
        'body' => 'Content body',
        'category_id' => Category::factory()->create()->id,
    ]);

    $response->assertCreated()
        ->assertJsonPath('data.title', 'Building deep modules');

    $this->assertDatabaseHas('articles', [
        'slug' => 'building-deep-modules',
        'user_id' => $author->id,
    ]);
}
```

## Faking external services

Fake queues, mail notifications, and outbound HTTP calls during automated tests to isolate external side effects:

```php
it('dispatches invoice generation job', function () {
    Queue::fake();
    Mail::fake();

    $order = Order::factory()->create();

    $this->postJson("/api/v1/orders/{$order->id}/pay");

    Queue::assertPushed(ProcessOrderPaymentJob::class);
    Mail::assertNothingSent();
});
```

## Testing HTTP clients

Mock outbound API calls with `Http::fake()`:

```php
Http::fake([
    'api.stripe.com/*' => Http::response(['id' => 'ch_123', 'status' => 'succeeded'], 200),
]);
```

## Database state management

Use `LazilyRefreshDatabase` or `RefreshDatabase` traits in feature test suites:

```php
use Illuminate\Foundation\Testing\LazilyRefreshDatabase;

uses(LazilyRefreshDatabase::class);
```
