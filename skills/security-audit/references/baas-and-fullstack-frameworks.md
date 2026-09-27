# BaaS and modern fullstack framework security

Reach for this file when the target uses Supabase, Firebase, Convex, Next.js App Router, or modern ORMs like Prisma. It covers declarative data access controls, edge execution boundaries, RPC Server Actions, and modern ORM query hazards.

## Supabase and PostgreSQL Row-Level Security

Tables created via SQL migrations or visual editors default to RLS disabled. A table lacking RLS is readable and writable by any client holding the public anon key.

### RLS activation and coverage
- Verify every table in public schemas enforces `ENABLE ROW LEVEL SECURITY`.
- Ensure junction tables, audit records, and auxiliary metadata tables have explicit RLS policies defined. A table with RLS enabled but zero policies denies all access.

### Dangerous policy clauses
- Detect and reject `USING (true)` or `USING (auth.uid() IS NOT NULL)` on SELECT, UPDATE, and DELETE policies. These allow any logged-in user to access all tenant rows.
- Ensure policies scope directly to row ownership using `USING ((SELECT auth.uid()) = user_id)`.

### Missing WITH CHECK clauses
- INSERT and UPDATE policies require `WITH CHECK` clauses matching ownership predicates. Without `WITH CHECK`, authenticated users can mutate `user_id` or insert records assigned to other users.

### Sensitive attributes on user-updatable tables
- When user tables permit self-service updates, verify that sensitive columns (`is_admin`, `role`, `credits`, `subscription_tier`) are protected.
- Enforce protection by moving sensitive columns to private schemas callable through `SECURITY DEFINER` functions or applying column-level grants.

### SECURITY DEFINER function isolation
- `SECURITY DEFINER` functions run with creator privileges and bypass RLS. Verify they explicitly set `SET search_path = ''` to prevent search path hijacking.
- Restrict execution permissions and keep functions inside non-public schemas.

### Storage bucket policies
- Storage buckets require dedicated access policies. Enforce folder isolation binding storage paths to user identities.

## Firebase Security Rules

### Default permissive rules
- Flag rules containing `allow read, write: if true;` or `allow read, write: if request.auth != null;`.
- Enforce explicit identity ownership matching `request.auth.uid == userId`.

### Subcollection rule inheritance trap
- Subcollections do not inherit security rules from parent document paths. Every subcollection path requires explicit, self-contained rule declarations.

### Field-level mutation restrictions
- Enforce update validations using `request.resource.data.diff(resource.data).affectedKeys()` to restrict mutable properties and protect role flags.
- Validate data types, size limits, and server-timestamp bindings on create operations.

## Convex access control

- Every public `query` and `mutation` must invoke `ctx.auth.getUserIdentity()` and reject unauthenticated requests.
- Verify resource ownership inside mutation bodies. Validating authentication status alone does not satisfy resource authorization.
- Mark internal functions as `internalQuery`, `internalMutation`, or `internalAction` to prevent exposure over public client transports.

## Next.js Server Actions and Route Handlers

Server Actions compile into public POST endpoints reachable directly via HTTP clients.

### Server Action invariants
- Authenticate and authorize at the top of every Server Action. Never assume execution originates exclusively from the trusted frontend UI.
- Validate incoming arguments using runtime schemas like Zod before database interactions. TypeScript types vanish at runtime and provide zero protection.
- Scope database mutations strictly to authenticated user identifiers:
```typescript
'use server';
export async function deleteResource(rawInput: unknown) {
  const parsed = schema.safeParse(rawInput);
  if (!parsed.success) return { error: 'Invalid input' };
  const session = await auth();
  if (!session?.user) redirect('/login');
  await db.resource.deleteMany({
    where: { id: parsed.data.id, userId: session.user.id }
  });
}
```

### Data leakage to Client Components
- Avoid passing raw database records across Server and Client component boundaries. Use explicit projections to prevent exposing internal fields, hashes, or tokens.
- Add `import 'server-only'` to internal data access modules to prevent bundling into client JavaScript.

### Middleware limitations
- Next.js middleware is a convenience routing layer, not a security boundary. Header manipulation and routing quirks can bypass edge middleware. Re-evaluate auth inside handlers and actions.

## Modern ORM safety with Prisma

### Operator injection defense
- Passing unsanitized objects into Prisma query filters permits operator injection. An attacker can supply nested filter keys to match unintended rows. Validate filter inputs with runtime schemas before query dispatch.

### Unsafe raw queries
- Prohibit `$queryRawUnsafe` and `$executeRawUnsafe` with concatenated inputs. Use parameterized tagged template literals.

### Mass assignment prevention
- Prohibit spreading raw request bodies directly into database update methods. Select validated fields explicitly.
