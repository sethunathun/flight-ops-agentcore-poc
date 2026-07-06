# Flight Ops Agent: A Hands-On Build on Amazon Bedrock AgentCore

## Why this repo exists

I have spent thirty years designing enterprise architecture, managing enterprise databases, building mission critical SaaS/Cloud Operations, leading techno-commercial part of presales for strategic pursuits  and selling it to CXOs. What I had not done, until now, was build an agentic AI system with my own hands, permission by permission, and watch it fail in the specific ways real systems fail. This repo is that build.

AWS is moving its agent story from Bedrock Agents to AgentCore, its new managed platform for agent runtimes, tool gateways, memory, and governance. I built a small flight-status agent end to end on this platform, not to ship a product, but to understand the architecture the way you only understand architecture, by breaking it and fixing it yourself.

## What I built

A flight-status assistant that answers questions like "what's the status of EK522" using live data, not a hardcoded answer:

- **DynamoDB** holds a mock flight-status table, one partition key (Flight_number), Status_Code, Departure_Time. PLUS three sample rows for three Flights.
- **Lambda** reads a single item from that table and returns a formatted status. Its execution role has exactly one permission: read that one table.
- **AgentCore Gateway** exposes the Lambda as an MCP tool, with its own scoped execution role that can invoke that one Lambda and nothing else.
- **AgentCore Harness** runs the agent loop against Claude Sonnet, calling the Gateway's tool when a flight number comes up, with short-term memory enabled so a follow-up question like "what gate is that" resolves correctly.
- **AgentCore Policy**, backed by Cedar, sits at the Gateway boundary as a deterministic authorization layer, separate from and outside the model's own reasoning. This Cedar is "supposed" to enable the AWS Guardrail.

Four IAM roles, four boundaries, each one scoped to exactly the next hop it needed and nothing more. That discipline, not the demo itself, is the part worth noticing.

## What actually taught me something

The build worked eventually. The debugging is where the real learning happened.

A Gateway target that silently failed to save on first creation, discovered only because a downstream symptom, no Lambda invocation, no Gateway logs, forced a walk back up the chain to find where the trail went cold.

A missing IAM permission between the Harness and the Gateway, diagnosed not by reading an error message but by reasoning through which of four separate roles could be the gap, then verifying each one in turn rather than guessing.

A Cedar policy engine that rejected my first attempts for three distinct and correctly diagnosed reasons: an invented keyword that Cedar simply does not have, an unscoped action clause, and finally a legitimate design warning about an overly broad policy that I had to consciously override rather than fight.

And the one still open: a guardrail I enforced but have not yet proven blocks anything, because my Cedar condition was checking the tool's input when the sensitive data lived in the tool's output. A clean, polite model response nearly convinced me the guardrail worked. It did not. The model was simply staying in its own scope. Telling the difference between "the model behaved" and "the system enforced" turned out to be the hardest and most useful distinction in the whole exercise.

## Honest status

Working: DynamoDB, Lambda, Gateway, Harness, Memory, multi-turn context.
Configured but unproven: Policy-based PII redaction at the Gateway boundary. The forbid condition needs to reference the tool's output context, not its input, before I can call this closed.

I am leaving that open on purpose (of course afetr spending 3 hours on it :-D ) rather than papering over it. An unfinished, honestly labeled result is worth more to me, and to anyone reading this, than a demo that looks clean because I stopped asking questions too early.

## Why this matters for the work I want to do next

Anyone can describe an agent architecture on a slide. Fewer people have scoped four IAM roles by hand, watched a policy engine's automated reasoning catch a design mistake before it shipped, and know exactly where in a request pipeline a guardrail needs to sit to actually stop something rather than just sound like it did. That distinction, between architecture that is described and architecture that is proven, is the one I intend to bring into every pre-sales conversation from here.

Are we designing the control, or just describing it?

