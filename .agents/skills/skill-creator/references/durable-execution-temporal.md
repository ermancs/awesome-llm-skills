# Layer 2 — Durable Execution with Temporal

Workflow-orchestration architecture with Temporal: the fundamental design decisions,
resilience patterns, and best practices for building reliable long-running distributed
systems. The concepts (workflows-vs-activities boundary, determinism, saga, idempotency)
generalize to other durable-execution engines (Inngest, Azure Durable Functions).

## When durable orchestration is the right tool

### Ideal use cases (Source: docs.temporal.io)
- **Multi-step processes** spanning machines/services/databases
- **Distributed transactions** requiring all-or-nothing semantics
- **Long-running workflows** (hours to years) with automatic state persistence
- **Failure recovery** that must resume from the last successful step
- **Business processes**: bookings, orders, campaigns, approvals
- **Entity lifecycle management**: inventory tracking, account management, cart workflows
- **Infrastructure automation**: CI/CD pipelines, provisioning, deployments
- **Human-in-the-loop** systems requiring timeouts and escalations

### When NOT to use
- Simple CRUD operations (use direct API calls)
- Pure data processing pipelines (use Airflow, batch processing)
- Stateless request/response (use standard APIs)
- Real-time streaming (use Kafka, event processors)

## Critical design decision: Workflows vs Activities

**The fundamental rule** (Source: temporal.io/blog/workflow-engine-principles):
- **Workflows** = orchestration logic and decision-making
- **Activities** = external interactions (APIs, databases, network calls)

### Workflows (orchestration)
- Contain business logic and coordination
- **MUST be deterministic** (same inputs → same outputs)
- **Cannot** perform direct external calls
- State automatically preserved across failures
- Can run for years despite infrastructure failures

Example workflow tasks: decide which steps to execute; handle compensation logic; manage
timeouts and retries; coordinate child workflows.

### Activities (external interactions)
- Handle all external system interactions
- Can be non-deterministic (API calls, DB writes)
- Include built-in timeouts and retry logic
- **Must be idempotent** (calling N times = calling once)
- Short-lived (seconds to minutes typically)

Example activity tasks: call payment gateway API; write to database; send emails/
notifications; query external services.

### Design decision framework
```
Does it touch external systems?     → Activity
Is it orchestration/decision logic? → Workflow
```

## Core workflow patterns

### 1. Saga pattern with compensation
**Purpose**: distributed transactions with rollback capability.
(Source: temporal.io/blog/compensating-actions-part-of-a-complete-breakfast-with-sagas)
```
For each step:
  1. Register compensation BEFORE executing
  2. Execute the step (via activity)
  3. On failure, run all compensations in reverse order (LIFO)
```
**Example — payment workflow:**
1. Reserve inventory (compensation: release inventory)
2. Charge payment (compensation: refund payment)
3. Fulfill order (compensation: cancel fulfillment)

Critical requirements: compensations must be idempotent; register compensation BEFORE
executing the step; run compensations in reverse order; handle partial failures gracefully.

### 2. Entity workflows (actor model)
**Purpose**: a long-lived workflow representing a single entity instance.
(Source: docs.temporal.io/evaluate/use-cases-design-patterns)
- One workflow execution = one entity (cart, account, inventory item)
- Workflow persists for the entity's lifetime
- Receives signals for state changes; supports queries for current state

Example use cases: shopping cart (add items, checkout, expiration); bank account (deposits,
withdrawals, balance checks); product inventory (stock updates, reservations).
Benefits: encapsulates entity behavior; guarantees per-entity consistency; natural event sourcing.

### 3. Fan-out / fan-in (parallel execution)
**Purpose**: execute multiple tasks in parallel, aggregate results.
- Spawn child workflows or parallel activities; wait for all; aggregate; handle partial failures.
- **Scaling rule** (Source: temporal.io/blog/workflow-engine-principles): don't scale individual
  workflows. For 1M tasks, spawn 1K child workflows × 1K tasks each. Keep each workflow bounded.

### 4. Async callback pattern
**Purpose**: wait for an external event or human approval.
- Workflow sends a request and waits for a signal; the external system processes
  asynchronously and sends a signal to resume; the workflow continues with the response.
- Use cases: human approval workflows, webhook callbacks, long-running external processes.

## State management and determinism

### Automatic state preservation (Source: docs.temporal.io/workflows)
- Complete program state preserved automatically; Event History records every command and event.
- Seamless recovery from crashes; applications restore pre-failure state.

### Determinism constraints
Workflows execute as state machines: replay behavior must be consistent; same inputs →
identical outputs every time.

**Prohibited in workflows** (Source: docs.temporal.io/workflows):
- ❌ Threading, locks, synchronization primitives
- ❌ Random number generation (`random()`)
- ❌ Global state or static variables
- ❌ System time (`datetime.now()`)
- ❌ Direct file I/O or network calls
- ❌ Non-deterministic libraries

**Allowed in workflows:**
- ✅ `workflow.now()` (deterministic time)
- ✅ `workflow.random()` (deterministic random)
- ✅ Pure functions and calculations
- ✅ Calling activities (non-deterministic operations)

### Versioning strategies
Challenge: changing workflow code while old executions are still running.
1. **Versioning API**: use `workflow.get_version()` for safe changes
2. **New workflow type**: create a new workflow, route new executions to it
3. **Backward compatibility**: ensure old events replay correctly

## Resilience and error handling

### Retry policies
Default: Temporal retries activities forever. Configure: initial retry interval; backoff
coefficient (exponential backoff); maximum interval (cap retry delay); maximum attempts.
Non-retryable errors: invalid input (validation failures), business rule violations,
permanent failures (resource not found).

### Idempotency requirements (Source: docs.temporal.io/activities)
Activities may execute multiple times; network failures trigger retries; duplicate
execution must be safe. Strategies: idempotency keys (deduplication); check-then-act with
unique constraints; upsert instead of insert; track processed request IDs.

### Activity heartbeats
Detect stalled long-running activities: activity sends periodic heartbeat with progress;
timeout if no heartbeat received; enables progress-based retry.

## Best practices

### Workflow design
1. **Keep workflows focused** — single responsibility per workflow
2. **Small workflows** — use child workflows for scalability
3. **Clear boundaries** — workflow orchestrates, activities execute
4. **Test locally** — use the time-skipping test environment

### Activity design
1. **Idempotent operations** — safe to retry
2. **Short-lived** — seconds to minutes, not hours
3. **Timeout configuration** — always set timeouts
4. **Heartbeat for long tasks** — report progress
5. **Error handling** — distinguish retryable vs non-retryable

### Common pitfalls
**Workflow violations**: using `datetime.now()` instead of `workflow.now()`; threading or
async operations in workflow code; calling external APIs directly from workflow;
non-deterministic logic in workflows.
**Activity mistakes**: non-idempotent operations (can't handle retries); missing timeouts
(activities run forever); no error classification (retrying validation errors); ignoring
payload limits (2MB per argument).

### Operational considerations
**Monitoring**: workflow execution duration; activity failure rates; retry attempts and
backoff; pending workflow counts.
**Scalability**: horizontal scaling with workers; task-queue partitioning; child-workflow
decomposition; activity batching when appropriate.

## Key principles
1. Workflows = orchestration, Activities = external calls
2. Determinism is non-negotiable for workflows
3. Idempotency is critical for activities
4. State preservation is automatic
5. Design for failure and recovery

## Additional resources
- Temporal core concepts: docs.temporal.io/workflows
- Workflow patterns: docs.temporal.io/evaluate/use-cases-design-patterns
- Best practices: docs.temporal.io/develop/best-practices
- Saga pattern: temporal.io/blog/saga-pattern-made-easy
