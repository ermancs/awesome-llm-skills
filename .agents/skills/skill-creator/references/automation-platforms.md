# Layer 3 — Automation Platforms & Production Patterns

The platforms (n8n, Temporal, Inngest, AWS Step Functions, Azure Durable Functions) and
patterns that turn brittle scripts into production-grade, durable automation.

**Key insight:** the platforms make different tradeoffs. n8n optimizes for accessibility,
Temporal for correctness, Inngest for developer experience. Pick based on your actual needs,
not hype.

*Source: vibeship-spawner-skills (Apache 2.0). Code examples are illustrative.*

## Principles
- Durable execution is non-negotiable for money- or state-critical workflows.
- Events are the universal language of workflow triggers.
- Steps are checkpoints — each should be independently retryable.
- Start simple; add complexity only when reliability demands it.
- Observability isn't optional — you need to see where workflows fail.
- Workflows and agents co-evolve — design for both.

## Platform selection

| Platform | When to use | Note |
|----------|-------------|------|
| **n8n** | Low-code automation, quick prototyping, non-technical users | Self-hostable, 400+ integrations, great for visual workflows |
| **Temporal** | Mission-critical workflows, financial transactions, microservices | Strongest durability guarantees, steeper learning curve |
| **Inngest** | Event-driven serverless, TypeScript codebases, AI workflows | Best developer experience, works with any hosting |
| **AWS Step Functions** | AWS-native stacks, existing Lambda functions | Tight AWS integration, JSON-based workflow definition |
| **Azure Durable Functions** | Azure stacks, .NET or TypeScript | Good AI agent support, checkpoint and replay |

## Patterns

### Sequential workflow pattern
Steps execute in order; each output becomes the next input. **When to use**: content
pipelines, data processing, ordered operations.
```
Step 1 → Step 2 → Step 3 → Output
  ↓         ↓         ↓
(checkpoint at each step)
```

**Inngest (TypeScript):**
```typescript
export const processOrder = inngest.createFunction(
  { id: "process-order" },
  { event: "order/created" },
  async ({ event, step }) => {
    const validated = await step.run("validate-order", async () =>
      validateOrder(event.data.order));
    // Durable — survives crashes
    const payment = await step.run("process-payment", async () =>
      chargeCard(validated.paymentMethod, validated.total));
    const shipment = await step.run("create-shipment", async () =>
      createShipment(validated.items, validated.address));
    await step.run("send-confirmation", async () =>
      sendEmail(validated.email, { payment, shipment }));
    return { success: true, orderId: event.data.orderId };
  }
);
```

**Temporal (TypeScript):**
```typescript
const { validateOrder, chargeCard, createShipment, sendEmail } =
  proxyActivities<typeof activities>({
    startToCloseTimeout: '30 seconds',
    retry: { maximumAttempts: 3, backoffCoefficient: 2 },
  });

export async function processOrderWorkflow(order: Order): Promise<void> {
  const validated = await validateOrder(order);
  const payment = await chargeCard(validated.paymentMethod, validated.total);
  const shipment = await createShipment(validated.items, validated.address);
  await sendEmail(validated.email, { payment, shipment });
}
```

**n8n:** `[Webhook: order.created] → [Validate] → [Process Payment] → [Create Shipment] →
[Send Email]`. Configure each node with retry on failure; use an Error Trigger for dead-letter
handling.

### Parallel workflow pattern
Independent steps run simultaneously, then aggregate. **When to use**: multiple independent
analyses, data from multiple sources.
```
        ┌→ Step A ─┐
Input ──┼→ Step B ─┼→ Aggregate → Output
        └→ Step C ─┘
```

**Inngest:**
```typescript
export const analyzeDocument = inngest.createFunction(
  { id: "analyze-document" },
  { event: "document/uploaded" },
  async ({ event, step }) => {
    const [security, performance, compliance] = await Promise.all([
      step.run("security-analysis", () => analyzeForSecurityIssues(event.data.document)),
      step.run("performance-analysis", () => analyzeForPerformance(event.data.document)),
      step.run("compliance-analysis", () => analyzeForCompliance(event.data.document)),
    ]);
    return step.run("generate-report", () =>
      generateReport({ security, performance, compliance }));
  }
);
```

**AWS Step Functions (Amazon States Language):**
```json
{
  "Type": "Parallel",
  "Branches": [
    { "StartAt": "SecurityAnalysis", "States": { "SecurityAnalysis": {
        "Type": "Task", "Resource": "arn:aws:lambda:...:security-analyzer", "End": true } } },
    { "StartAt": "PerformanceAnalysis", "States": { "PerformanceAnalysis": {
        "Type": "Task", "Resource": "arn:aws:lambda:...:performance-analyzer", "End": true } } }
  ],
  "Next": "AggregateResults"
}
```

### Orchestrator-worker pattern
A central coordinator dispatches work to specialized workers. **When to use**: complex tasks
requiring different expertise, dynamic subtask creation.
```
┌─────────────────────────────┐
│         ORCHESTRATOR         │
│  analyze → subtasks →        │
│  dispatch → aggregate        │
└─────────────────────────────┘
      ┌───────┼───────┐
   Worker1  Worker2  Worker3
   Create   Modify   Delete
```

**Temporal:**
```typescript
export async function orchestratorWorkflow(task: ComplexTask) {
  const plan = await analyzeTask(task);
  const results = await Promise.all(
    plan.subtasks.map(subtask => {
      switch (subtask.type) {
        case 'create': return executeChild(createWorkerWorkflow, { args: [subtask] });
        case 'modify': return executeChild(modifyWorkerWorkflow, { args: [subtask] });
        case 'delete': return executeChild(deleteWorkerWorkflow, { args: [subtask] });
      }
    })
  );
  return aggregateResults(results);
}
```

**Inngest with AI orchestration:**
```typescript
export const aiOrchestrator = inngest.createFunction(
  { id: "ai-orchestrator" },
  { event: "task/complex" },
  async ({ event, step }) => {
    const plan = await step.run("create-plan", async () =>
      llm.chat({ messages: [
        { role: "system", content: "Break this task into subtasks..." },
        { role: "user", content: event.data.task }
      ]}));
    const results = [];
    for (const subtask of plan.subtasks) {
      results.push(await step.run(`execute-${subtask.id}`, async () => executeSubtask(subtask)));
    }
    return step.run("synthesize", async () => synthesizeResults(results));
  }
);
```

### Event-driven trigger pattern
Workflows triggered by events, not schedules. **When to use**: reactive systems, user actions,
webhook integrations.

**Inngest event-based:**
```typescript
type Events = {
  "user/signed.up": { data: { userId: string; email: string } };
  "order/completed": { data: { orderId: string; total: number } };
};

export const onboardUser = inngest.createFunction(
  { id: "onboard-user" },
  { event: "user/signed.up" },
  async ({ event, step }) => {
    await step.sleep("wait-for-exploration", "1 hour");
    await step.run("send-welcome", async () => sendWelcomeEmail(event.data.email));
    await step.sleep("wait-for-engagement", "3 days");
    const engaged = await step.run("check-engagement", async () =>
      checkUserEngagement(event.data.userId));
    if (!engaged) {
      await step.run("send-nudge", async () => sendNudgeEmail(event.data.email));
    }
  }
);

await inngest.send({ name: "user/signed.up", data: { userId: "123", email: "user@example.com" } });
```

**n8n webhook:** `[Webhook: POST /api/webhooks/order] → [Switch: event.type]` → route
`order.created` / `order.cancelled` to their respective subworkflows.

### Retry and recovery pattern
Automatic retry with backoff, dead-letter handling. **When to use**: any workflow with external
dependencies.

**Temporal retry configuration:**
```typescript
const activities = proxyActivities<typeof activitiesType>({
  startToCloseTimeout: '30 seconds',
  retry: {
    initialInterval: '1 second',
    backoffCoefficient: 2,
    maximumInterval: '1 minute',
    maximumAttempts: 5,
    nonRetryableErrorTypes: ['ValidationError', 'InsufficientFunds'],
  }
});
```

**Inngest retry + non-retriable:**
```typescript
export const processPayment = inngest.createFunction(
  { id: "process-payment", retries: 5 },
  { event: "payment/initiated" },
  async ({ event, step }) => step.run("charge-card", async () => {
    try { return await stripe.charges.create({/* ... */}); }
    catch (error) {
      if (error.code === 'card_declined') throw new NonRetriableError("Card declined");
      throw error; // retry other errors
    }
  })
);
```

**Dead-letter handling:**
```typescript
// n8n: [Error Trigger] → [Log to DB] → [Slack Alert] → [Create Jira ticket]
// Inngest: onFailure handler
export const myFunction = inngest.createFunction(
  { id: "my-function", onFailure: async ({ error, event, step }) => {
      await step.run("alert-team", async () =>
        slack.postMessage({ channel: "#errors", text: `Function failed: ${error.message}` }));
  }},
  { event: "..." },
  async ({ step }) => { /* ... */ }
);
```

### Scheduled workflow pattern
Time-based triggers for recurring tasks. **When to use**: daily reports, periodic sync, batch
processing.

**Inngest cron:**
```typescript
export const dailyReport = inngest.createFunction(
  { id: "daily-report" },
  { cron: "0 9 * * *" },  // 9 AM daily
  async ({ step }) => {
    const data = await step.run("gather-metrics", async () => gatherDailyMetrics());
    await step.run("generate-report", async () => generateAndSendReport(data));
  }
);
```

**Temporal cron:**
```typescript
const handle = await client.workflow.start(dailyReportWorkflow, {
  taskQueue: 'reports', workflowId: 'daily-report', cronSchedule: '0 9 * * *',
});
```

**n8n:** `[Schedule Trigger: daily 9 AM] → [Get Metrics] → [Generate Report] → [Send Email]`.

---

## Sharp Edges (anti-patterns)

The most expensive workflow bugs are a small, known set. Situation → symptoms → why → fix.

### Non-idempotent steps in durable workflows — CRITICAL
**Situation:** workflow steps that modify external state.
**Symptoms:** customer charged twice; email sent three times; duplicate DB records; retries
cause duplicate side effects.
**Why:** durable execution replays workflows from the beginning on restart. If step 3 crashes
and the workflow resumes, steps 1 and 2 run again. Without idempotency keys, external services
don't know these are retries.
**Fix — always use idempotency keys for external calls:**
```typescript
// Stripe
await stripe.paymentIntents.create({
  amount: 1000, currency: 'usd',
  idempotency_key: `order-${orderId}-payment`  // Critical!
});
// Email — check before send
await step.run("send-confirmation", async () => {
  if (await checkEmailSent(orderId)) return { skipped: true };
  return sendEmail(customer, orderId);
});
// DB — upsert
await db.query(`INSERT INTO orders (id, ...) VALUES ($1, ...) ON CONFLICT (id) DO NOTHING`, [orderId]);
```
Generate the idempotency key from stable inputs, not random values.

### Workflow runs for hours/days without checkpoints — HIGH
**Situation:** long-running workflows with infrequent steps.
**Symptoms:** memory grows; worker timeouts; lost progress after crashes; "exceeded maximum
duration" errors.
**Why:** workflows hold state in memory until checkpointed. A 24-hour workflow with one step
per hour accumulates 24h of state; workers have memory limits.
**Fix — break long work into many small checkpointed steps:**
```typescript
// WRONG — one long step
await step.run("process-all", async () => {
  for (const item of thousandItems) await processItem(item);
});
// CORRECT — checkpoint after each
for (const item of thousandItems) {
  await step.run(`process-${item.id}`, async () => processItem(item));
}
// For long waits use sleep (no resource use while waiting)
await step.sleep("wait-for-trial", "14 days");
// Consider child workflows for long processes
await step.invoke("process-batch", { function: batchProcessor, data: { items: batch } });
```

### Activities without timeout configuration — HIGH
**Situation:** calling external services from workflow activities.
**Symptoms:** workflows hang indefinitely; worker pool exhausted; dead workflows that never
complete; manual intervention needed.
**Why:** external APIs can hang forever. Unlike HTTP clients, workflow activities don't have
default timeouts on most platforms.
**Fix — always set timeouts (activity timeout < workflow timeout):**
```typescript
// Temporal
const activities = proxyActivities<typeof activitiesType>({
  startToCloseTimeout: '30 seconds',   // Required!
  scheduleToCloseTimeout: '5 minutes',
  heartbeatTimeout: '10 seconds',
  retry: { maximumAttempts: 3, initialInterval: '1 second' }
});
// Inngest
await step.run("call-api", { timeout: "30s" }, async () =>
  fetch(url, { signal: AbortSignal.timeout(25000) }));
// AWS Step Functions
{ "Type": "Task", "TimeoutSeconds": 30, "HeartbeatSeconds": 10, "Resource": "arn:aws:lambda:..." }
```

### Side effects outside step/activity boundaries — CRITICAL
**Situation:** code that runs during workflow replay.
**Symptoms:** random failures on replay; "workflow corrupted"; different behavior on replay;
non-determinism errors.
**Why:** workflow code runs on EVERY replay. A random ID or current-time read yields a
different value each replay, breaking determinism.
**Fix — move side effects into activities (or use replay-safe primitives):**
```typescript
// WRONG — side effects in workflow code
const orderId = uuid();       // Different every replay!
const now = new Date();       // Different every replay!
// CORRECT — in activities (recorded)
const orderId = await activities.generateOrderId();
const now = await activities.getCurrentTime();
// Also CORRECT — Temporal replay-safe primitives
const id = await sideEffect(() => uuid());
const t  = workflow.now();
```
Safe in workflow code: reading arguments, simple calculations (no randomness), logging.

### Retry without exponential backoff — MEDIUM
**Situation:** configuring retry behavior for failing steps.
**Symptoms:** overwhelming failing services; rate limiting; cascading failures; retry storms.
**Why:** immediate retries against a struggling service make it worse. Backoff gives it time to
recover.
**Fix — always use exponential backoff (with jitter to avoid thundering herd):**
```typescript
// Temporal
retry: { initialInterval: '1 second', backoffCoefficient: 2, maximumInterval: '1 minute', maximumAttempts: 5 }
// Inngest — exponential backoff by default: { id: "my-function", retries: 5 }
// Manual
const backoff = (attempt) => {
  const delay = Math.min(1000 * Math.pow(2, attempt), 60000);
  return delay + delay * 0.1 * Math.random(); // jitter
};
```

### Storing large data in workflow state — HIGH
**Situation:** passing large payloads between steps.
**Symptoms:** slow execution; memory errors; "payload too large"; expensive storage; slow replays.
**Why:** workflow state is persisted and replayed. A 10MB payload is serialized/deserialized on
every step. Some platforms have hard limits (Step Functions: 256KB).
**Fix — store a reference, not the data:**
```typescript
// WRONG — 100MB in workflow state
await step.run("fetch-data", async () => await fetchAllRecords());
// CORRECT — store reference
const { s3Key } = await step.run("fetch-data", async () => {
  const data = await fetchAllRecords();
  return { s3Key: await uploadToS3(data) };
});
const processed = await step.run("process-data", async () =>
  processData(await downloadFromS3(s3Key)));
```

### Missing dead-letter queue or failure handler — HIGH
**Situation:** workflows that exhaust all retries.
**Symptoms:** failed workflows silently disappear; no alerts; customer issues found days later;
manual recovery impossible.
**Why:** even with retries, some workflows fail permanently. Without dead-letter handling you
don't know they failed.
**Fix — Inngest onFailure handler:**
```typescript
export const myFunction = inngest.createFunction(
  { id: "process-order", onFailure: async ({ error, event, step }) => {
      await step.run("log-error", () => sentry.captureException(error, { extra: { event } }));
      await step.run("alert", () => slack.postMessage({ channel: "#alerts",
        text: `Order ${event.data.orderId} failed: ${error.message}` }));
      await step.run("queue-review", () => db.insert(failedOrders, { orderId, error, event }));
  }},
  { event: "order/created" },
  async ({ event, step }) => { /* ... */ }
);
// n8n: [Error Trigger] → [Log to DB] → [Slack Alert] → [Create Ticket]
```

### n8n workflow without Error Trigger — MEDIUM
**Situation:** building production n8n workflows.
**Symptoms:** workflow fails silently; errors only in execution logs; no alerts until someone
notices.
**Why:** n8n doesn't notify on failure by default.
**Fix — every production n8n workflow needs:**
1. An **Error Trigger** node (catches any node failure, provides error context).
2. Connected error handling: `[Error Trigger] → [Set: Extract Error] → [HTTP: Log] → [Slack/Email Alert]`.
3. Consider a dead-letter pattern: `[Error Trigger] → [Redis/Postgres: Store Failed Job] → [Recovery Workflow]`.
Also use: node-level retry, node timeouts, workflow timeout.

### Long-running Temporal activities without heartbeat — MEDIUM
**Situation:** activities that run more than a few seconds.
**Symptoms:** activity timeouts even when progressing; lost work on worker restart; can't cancel.
**Why:** Temporal detects stuck activities via heartbeat. Without it, long activities appear hung.
**Fix — for any activity > 10s, heartbeat and check for cancellation:**
```typescript
import { heartbeat, activityInfo } from '@temporalio/activity';
export async function processLargeFile(fileUrl: string): Promise<void> {
  const chunks = await downloadChunks(fileUrl);
  for (let i = 0; i < chunks.length; i++) {
    if (activityInfo().cancelled) throw new CancelledFailure('Activity cancelled');
    await processChunk(chunks[i]);
    heartbeat({ progress: (i + 1) / chunks.length });
  }
}
// Configure: startToCloseTimeout: '10 minutes', heartbeatTimeout: '30 seconds'
```

---

## Validation checks

A quick lint list to run against any workflow code before shipping.

| Check | Severity | Message |
|-------|----------|---------|
| External call without idempotency key | ERROR | Payment call without `idempotency_key` — add one to prevent duplicate charges on retry. |
| Email send without deduplication | WARNING | Email sent in workflow without a dedup check — retries may send duplicates. |
| Temporal activity without timeout | ERROR | `proxyActivities` without timeout — add `startToCloseTimeout` to prevent indefinite hangs. |
| Inngest step calling external API without timeout | WARNING | External API call in step without timeout — add one to prevent workflow hangs. |
| Random value in workflow code | ERROR | Random value breaks determinism on replay — move to activity/step or use `sideEffect`. |
| `Date.now()` in workflow code | ERROR | Current time breaks determinism on replay — use `workflow.now()` or move to activity/step. |
| Inngest function without onFailure handler | WARNING | Production functions should have failure handlers — add one for reliability. |
| Step without error handling | WARNING | Step without try/catch — consider handling specific error cases. |
| Potentially large data returned from step | INFO | Large data in workflow state slows execution — store in S3/DB and return a reference. |
| Retry without backoff configuration | WARNING | Retry configured without backoff — add `backoffCoefficient` and `initialInterval`. |

## Delegation triggers
- Multi-agent coordination → Layer 1 (`agent-workflow-patterns.md`).
- Deep durable-execution semantics → Layer 2 (`durable-execution-temporal.md`).
- Building the tool/app code a workflow invokes → `kidemli-yazilim-muhendisi`.
- Standing up an MCP server → `mcp-builder`.
