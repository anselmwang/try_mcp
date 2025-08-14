# Notification Rules for Cline

WHEN:
1. A long-running plan or command finishes (success or failure).
2. All tests pass and goals are met.
3. A blocking error requires human input.
4. Waiting for credentials or ambiguous decision.

THEN:
- Call `email-notify.send_email` with:
  - subject: `[Cline] ${projectOrRepoName} — ${eventKind}`
  - text: Summary + next required input + short log tail.

STYLE:
- Keep under 30 lines.
- Include next-action checklist.
- Include exit code or test stats if relevant.
