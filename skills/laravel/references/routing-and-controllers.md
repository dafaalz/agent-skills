# Routing, controllers, and validation

Keep controllers thin, isolate business logic into dedicated actions or services, and validate every request through Form Request classes.

## Controllers

Controllers coordinate the request lifecycle, invoke domain actions, and return HTTP responses. Keep business calculations and database queries out of controller methods.

For endpoints handling dedicated business processes, use single action controllers:

```php
final class RegisterUserController
{
    public function __invoke(RegisterUserRequest $request, RegisterUserAction $action): JsonResponse
    {
        $user = $action->execute($request->validated());

        return response()->json([
            'data' => new UserResource($user),
        ], 201);
    }
}
```

## Form requests and validation

Extract validation into Form Request classes for mutation endpoints (`POST`, `PUT`, `PATCH`, `DELETE`). Access only validated data via `$request->validated()` instead of `$request->all()`:

```php
final class StoreArticleRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Article::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'alpha_dash', 'unique:articles,slug'],
            'body' => ['required', 'string'],
            'category_id' => ['required', 'integer', 'exists:categories,id'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['integer', 'exists:tags,id'],
        ];
    }
}
```

Rules for validation arrays:
- Use array syntax for validation rules instead of pipe strings (`['required', 'string']` instead of `'required|string'`).
- Always validate nested array items with wildcards (`tags.*`).
- Pass only validated array keys from `$request->validated()` into Eloquent `create()` or `update()`. Never pass unvalidated inputs.

## Route model binding and scoping

Use implicit route model binding to automatically resolve models from route parameters:

```php
Route::get('/users/{user}', [UserController::class, 'show']);
```

For parent-child nested resources, scope child lookups automatically to prevent cross-tenant data leaks:

```php
Route::get('/teams/{team}/projects/{project}', [TeamProjectController::class, 'show'])
    ->scopeBindings();
```

## API resources

Transform responses explicitly with JsonResource classes instead of returning raw Eloquent models directly to callers:

```php
final class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'team' => new TeamResource($this->whenLoaded('team')),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}
```
