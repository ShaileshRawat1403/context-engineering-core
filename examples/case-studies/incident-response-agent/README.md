# Case Study: Incident Response Agent

## 1. Goal and Mission

This case study demonstrates how to build an autonomous agent to assist with live incident response. The agent's mission is to analyze logs, identify the root cause of an issue, and suggest remediation steps. The primary challenge is managing a large volume of time-sensitive and often noisy data from multiple sources.

**Mission:** Given an alert like "High latency in checkout service," the agent should be able to investigate logs, metrics, and traces to propose a likely root cause.

## 2. Context Control Patterns Applied

-   **`Signal-vs-Noise`**: Aggressively filter logs to isolate error-level messages or specific keywords (e.g., "timeout").
-   **`Lifetimes`**: Use a time-windowed approach; data older than the incident's start time is considered stale.
-   **`Degradation`**: The agent monitors its own state; if its investigation spreads too thin, it escalates to a human.
-   **`Isolation`**: Each investigation runs in an isolated context to prevent interference between different incidents.
-   **`Validation`**: The agent forms hypotheses and seeks specific, validating data before concluding.
-   **`Ordering`**: Log entries are strictly ordered chronologically to construct a coherent narrative.
-   **`Agents` & `Memory`**: An autonomous agent uses tools, and a structured `Memory` system stores findings and hypotheses.

## 3. Agent Workflow

Upon receiving an alert, the agent begins a hypothesis-driven investigation loop.

```mermaid
graph TD
    A[Alert: "High latency in checkout service"] --> B{Triage & Scope};
    B --> C[Initial Data: Query logs for errors];
    C --> D{Generate Hypotheses};
    D -- H1: DB Issue --> E1[Validate H1: Run DB health check];
    D -- H2: Upstream issue --> E2[Validate H2: Check upstream metrics];
    E1 --> F{Observation};
    E2 --> F;
    F -- Confirmed? --> G[Propose Root Cause];
    F -- Not Confirmed? --> D;
```

### Step 1: Key Artifacts and Tools

The agent needs structured memory and tools to interact with its environment.

```python
# pseudo-code for agent memory and tools

from datetime import datetime

class LogEntry:
    """Represents a single, structured log entry."""
    def __init__(self, timestamp: datetime, service: str, level: str, message: str):
        self.timestamp = timestamp
        self.service = service
        self.level = level
        self.message = message

class IncidentMemory:
    """A structured memory for the agent's findings during one incident."""
    def __init__(self, incident_id: str):
        self.incident_id = incident_id
        self.hypotheses: list[str] = []
        self.validated_facts: list[str] = []
        self.discarded_leads: list[str] = []

    def add_hypothesis(self, hypo: str):
        """Adds a new hypothesis to investigate."""
        if hypo not in self.hypotheses and hypo not in self.validated_facts:
            self.hypotheses.append(hypo)

class LogStoreTool:
    """A tool for querying and filtering logs from an aggregator."""
    def query(self, service: str, start_time: datetime, level: str = "ERROR") -> list[LogEntry]:
        """Queries logs with strong filtering."""
        print(f"TOOL: Querying logs for '{service}' at level '{level}' since {start_time}...")
        # In a real system, this would query Splunk, Datadog, etc.
        # Returning a dummy entry for the walkthrough.
        return [
            LogEntry(datetime.now(), service, "ERROR", "Connection to checkout-db timed out.")
        ]
```

*Initial Design Flaw: A simple list of strings for memory is insufficient. A structured object like `IncidentMemory` allows the agent to reason about its own investigation, track what it has already tried, and explain its reasoning.*

### Step 2: Putting It All Together: A Walkthrough

Let's trace the agent's investigation for the alert: **"High latency in checkout service."**

1.  **TRIAGE & SCOPE**: The agent identifies the service ("checkout-service") and sets an initial time window (e.g., the last 15 minutes). It initializes an `IncidentMemory` for this investigation.

2.  **REASON**: The agent's first step is to find any immediate error signals from the affected service.
3.  **ACT**: It calls `LogStoreTool.query(service="checkout-service", start_time=...)`.

4.  **OBSERVE**: The tool returns a list of `LogEntry` objects.

    **Tool Output (LogEntry):**
    ```
    timestamp: ...,
    service: "checkout-service",
    level: "ERROR",
    message: "Connection to checkout-db timed out."
    ```

5.  **REASON**: The agent analyzes the log message. The timeout error points to a potential database issue. The agent generates a new hypothesis.
6.  **ACT**: It updates its memory: `memory.add_hypothesis("The checkout-db is unreachable.")`.

7.  **REASON**: The agent now needs to validate its new hypothesis. It checks its available tools and finds a `DatabaseHealthCheckTool`.
8.  **ACT**: It calls `DatabaseHealthCheckTool.run("checkout-db")`.

9.  **OBSERVE**: The tool returns a failure message: `"Health check failed: unable to connect."`

10. **REASON (Conclusion)**: The agent has validated its hypothesis. The log timeout corresponds with a live health check failure. It concludes this is the likely root cause.
11. **ACT (Final Response)**: The agent generates its final report.

    **Final Agent Report:**
    > **Root Cause Identified for Incident #123:** High latency in the `checkout-service` is caused by a failure to connect to `checkout-db`.
    > **Validation:**
    > 1. Service logs show "Connection to checkout-db timed out."
    > 2. A live health check against `checkout-db` failed.
    > **Recommendation:** Escalate to the on-call database administrator.

## 4. Challenges and Solutions

-   **Challenge:** The agent is flooded with thousands of log entries per second.
    -   **Solution:** Aggressive `Signal-vs-Noise` filtering. The agent never queries for "all logs." It always queries with specific filters for level, keywords, and time, as defined by the `Lifetimes` primitive.

-   **Challenge:** The agent gets stuck in a loop, investigating the same irrelevant lead.
    -   **Solution:** The structured `Memory` helps the agent recognize and prune repeated or failed lines of investigation. It can explicitly reason: "I have already investigated the `auth-service` and found no errors, so I will not investigate it again."

-   **Challenge:** Two separate incidents start at the same time, and the agent mixes up the data.
    -   **Solution:** The `Isolation` pattern is key. Each incident investigation is a separate process or object with its own dedicated `IncidentMemory`, preventing cross-contamination of context.
