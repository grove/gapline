# Investigation recipes

Use the recipe that helps resolve the current question. These are optional reasoning aids; they do not add required report sections, new evidence states, or permission to execute anything.

## 1. Consequential coupling

Start with a requested change, an observed change, or an operational scenario that matters. Trace the policy it affects and the other behavior connected by a dependency or shared representation.

- What would have to change together, and why?
- Do those changes serve the same responsibility, or can one harm an unrelated responsibility?
- Is the consequence visible in a current path, supported by inspected history, or only predicted?
- Would a small seam, relocation, or contract clarification address it?

Look for coherent policies, generated code, stable interfaces, and deliberate tradeoffs. Do not infer historical maintenance cost from file size. If no consequence can be traced, keep the concern unresolved. A dependency direction or a SOLID label supplies a question, not proof.

## 2. Mechanisms affecting decisions

Follow translations between an external representation and an important decision. Ask whether a change in formatting, storage, host output, or dependency shape could alter the conclusion while the underlying evidence remains the same.

- Find where failures, unavailable results, and unknown states are interpreted.
- Check whether presentation merely displays a decision or also changes it.
- Identify which assumptions the consumer actually needs.
- Preserve exact representations when identity, signatures, hashes, or protocol requirements make those representations part of the contract.

Importing an infrastructure library alone is insufficient evidence. Report the effect on a relevant policy or currently needed variation. A valid implementation change must preserve externally significant behavior, including bytes when required.

## 3. Repeated logic and independent validation

First establish whether similar code expresses the **same obligation**. Compare actual inputs, entry points, authority boundaries, and consumers.

One rule implemented differently on two live paths can support a drift concern. Similar syntax can instead represent policies that should evolve independently. For repeated validation, determine whether each check protects an independently reachable trust boundary: removing the receiving check may make it trust data it must validate itself.

Neither "intentional" nor "duplicated" settles the question. Identify the contract and a concrete consequence. A small comparison table can make the differing rules clear; a shared validator is a proposed remedy only when its coupling cost is justified.

## 4. Local successes and global invariants

Trace multiple operations sharing an entity, collection, resource, or transition. Read what the tests check after the combined operation.

- Do two updates preserve one entity's identity?
- Is a required quantity conserved?
- Can retrying repeat an externally significant side effect?
- Does one operation preserve unrelated information?
- Are state transitions and their ordering allowed by the actual contract?

Require a source for the invariant. Duplicate values, multiple observations of one entity, and repeated calls may be legitimate. Distinguish a supported source-level concern from an executed reproduction. Clean local functions and passing local assertions do not settle the combined behavior.

## 5. Protection supplied by tests

Identify the real oracle: assertion, expected exception, framework expectation, process result, snapshot, or invariant. Inspect helpers and relevant neighboring tests before claiming an omission.

Ask two separate questions:

1. Which plausible **wrong behavior** should this test reject? Can the observed assertion distinguish it, or does a mock bypass the relevant path? Does the expected value simply repeat the implementation's calculation?
2. Which **valid change** should the test allow? Is a private call or class structure incidental, or does an interaction protect required caching, ordering, side effects, or another operational promise?

Preserve the full contract when judging equivalence. Equal return values do not establish equivalent effects. A smoke test without a conventional assertion can detect exceptions and protect a narrow property; do not call it adequate for a wider promise it does not check. Coverage locates executed or unexecuted areas, not assertion strength.

State a test gap only for the inspected scope. The source of the intended behavior remains necessary: neither a test name nor agreement between generated code and generated tests makes an expectation authoritative. Propose executable comparisons as **NOT RUN**.

Apply the same wrong-behavior/valid-change questions to consequential checks you propose. A direct scan of a primary-key column constrained NOT NULL cannot supply a NULL operand; use an input that can actually be NULL on the selected path. Confirm the caller's role actually selects the snapshot branch of interest, rather than a privileged shortcut. If no inspected seam reaches the boundary, disclose that gap instead of inventing a runnable harness.

For a paused-snapshot/concurrent-refresh probe, requiring refresh to commit before releasing the snapshot can deadlock a valid serializing repair. Propose a bounded wait, release the pause whether refresh completes or blocks, then bound completion of both operations and check the contract's consistency invariant. A timeout alone does not prove the suspected race; unreleased barriers and unknown session behavior remain harness gaps. These are planning examples, **PROPOSED — NOT RUN**, not runtime evidence or required report fields.

## 6. Scope and the cost of a remedy

Before calling a capability missing, locate its current promise. An advertised option that is ignored differs from an explicitly deferred feature. An accepted limitation may be reasonable when its cost is contained and infrequent.

Explain the recurring cost or risk and the smallest useful action. Identify a condition for revisiting a deliberate compromise when relevant. Avoid recommending an extensibility layer, shared runtime, new platform, or service solely because it might help later. Refactoring preserves defined behavior; distinguish it from fixing a defect or changing a contract.

## Reading behind these questions

The recipes apply the authors' arguments to investigations; neither author prescribed this checklist. The linked articles are background reading, not required input to an audit. Do not fetch them during an audit unless the user and host authorize that access.

- Martin Fowler, [Code Smell](https://martinfowler.com/bliki/CodeSmell.html): investigate a symptom and its possible innocent explanation.
- Robert C. Martin, [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html): connect responsibilities to reasons for change.
- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html): preserve policy across mechanism boundaries.
- Martin Fowler, [Test Coverage](https://martinfowler.com/bliki/TestCoverage.html): examine what test evidence can and cannot establish.
- Martin Fowler, [Assertion Free Testing](https://martinfowler.com/bliki/AssertionFreeTesting.html): recognize the narrow value of execution-only tests.
- Martin Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html): examine state and interaction verification in context.
- Robert C. Martin, [Test Contra-variance](https://blog.cleancoder.com/uncle-bob/2017/10/03/TestContravariance.html): preserve freedom to restructure internals.
- Robert C. Martin, [Functional Duplications](https://blog.cleancoder.com/uncle-bob/2021/10/28/functional-duplication.html): inspect invariants omitted by locally relevant assertions.
- Martin Fowler, [Yagni](https://martinfowler.com/bliki/Yagni.html) and [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html): assess present need, learning, and the cost of a compromise.
