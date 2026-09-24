# Security and hardening

Follow these rules to prevent authorization bypasses, SQL injection, and data leaks.

## Authorization with policies

Enforce access control using Model Policies instead of inline boolean checks in controllers:

```php
final class ArticlePolicy
{
    public function update(User $user, Article $article): bool
    {
        return $user->id === $article->user_id || $user->hasRole('admin');
    }
}
```

Authorize actions at the controller or Form Request entrypoint:

```php
// Inside controller action
$this->authorize('update', $article);

// Or inside FormRequest authorize() method
public function authorize(): bool
{
    $article = $this->route('article');
    return $this->user()?->can('update', $article) ?? false;
}
```

## SQL injection prevention

Pass values through parameterized bindings. Never interpolate variables directly into raw SQL strings.

Direct string interpolation exposes raw queries to SQL injection:

```php
Article::whereRaw("slug = '{$slug}'")->first();
```

Parameterized bindings safely escape user input:

```php
Article::whereRaw('slug = ?', [$slug])->first();
```

## Mass assignment protection

Define `$fillable` explicitly on models, or unguard models only when all inputs pass through validated Form Requests:

```php
final class Article extends Model
{
    protected $fillable = [
        'title',
        'slug',
        'body',
        'category_id',
        'user_id',
    ];
}
```

Pass `$request->validated()` into `Model::create()` or `$model->update()`. Never pass raw `$request->all()` into model mutators:

```php
$article->update($request->validated());
```

## Sensitive attribute hiding

Hide sensitive fields like passwords, tokens, and secret keys in model serialization:

```php
protected $hidden = [
    'password',
    'remember_token',
    'two_factor_secret',
    'two_factor_recovery_codes',
];
```
