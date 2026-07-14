# Design Decisions

## Decision: Layered Architecture

**Context:** Separate HTTP handling, business logic, and data access.

**Options Considered:**
- Keep all logic inside the API layer.
- Introduce a Router → Service → Repository architecture.

**Choice:** Used a layered architecture.

**Why:** Improves maintainability, keeps responsibilities clear, and makes the application easier to test and extend.

---

## Decision: Redis Native Data Structures

**Context:** Store products, carts, orders, coupons, and statistics efficiently.

**Options Considered:**
- Store everything as JSON.
- Use Redis hashes, lists, sets, and counters.

**Choice:** Used Redis-native data structures.

**Why:** Reduces serialization overhead and allows efficient field-level operations while making better use of Redis.

---

## Decision: Atomic Order ID Generation

**Context:** Every Nth order receives a reward coupon.

**Options Considered:**
- Count existing orders.
- Use Redis atomic counters.

**Choice:** Used Redis `INCR` to generate order IDs.

**Why:** Guarantees unique sequential IDs without race conditions and simplifies reward coupon generation.

---

## Decision: Pre-computed Store Statistics

**Context:** The admin dashboard needs fast access to analytics.

**Options Considered:**
- Aggregate statistics on every request.
- Maintain running totals during checkout.

**Choice:** Updated statistics during checkout.

**Why:** Makes the dashboard a constant-time lookup while keeping the implementation simple.

---

## Decision: Redis as the Primary Datastore

**Context:** Keep the implementation lightweight while demonstrating the required functionality.

**Options Considered:**
- PostgreSQL + Redis.
- Redis only.

**Choice:** Used Redis for the entire application.

**Why:** Simplifies the implementation and highlights Redis capabilities. In a production system, orders and payment data would be stored in PostgreSQL, while Redis would continue to manage carts, caching, and counters.