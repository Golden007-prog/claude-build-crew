---
description: Deploy the latest default-branch commit — staging + smoke tests, then production only after your explicit yes. Usage: /deploy [staging-only]
argument-hint: [staging-only]
---

Deploy. Options: $ARGUMENTS

1. Run the `build-crew:deployer` subagent in mode `staging`. If it returns STOPPED or any smoke test fails, show why and END.
2. If `$ARGUMENTS` contains `staging-only`, report the staging URL and END.
3. **Human, every time:** "Staging OK at <url> (<short sha>). Smoke: <summary>. Deploy this exact commit to PRODUCTION? (yes / no)". Wait. Anything but a clear yes means no, so END.
4. Run the `build-crew:deployer` subagent in mode `production`, including these lines verbatim:
   `USER_APPROVED_PRODUCTION: yes`
   `APPROVED_SHA: <full sha from staging>`
5. Report the result, URL, smoke checks, and rollback target. If it was ROLLED_BACK, explain and suggest `/fix`.

Never write `USER_APPROVED_PRODUCTION: yes` unless the user typed yes in step 3 of this run.
