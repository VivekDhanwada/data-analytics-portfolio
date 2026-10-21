# Automated tracking tests

Playwright tests that check the tracking on vivekdhanwada.github.io against the event specification. They run in Chromium and in WebKit, the engine Safari uses (Playwright's WebKit build, not Safari itself).

## What they check

Each test loads the live site, clicks a link the way a visitor would, and checks two things:

1. **The dataLayer push.** The event name, every parameter in the specification, each parameter's type, and that no value is empty.
2. **The GA4 request.** The request GTM sends to GA4 carries the same values as the push. This catches a break between the push and the tag, such as a renamed key.

Events covered: `resume_download`, `project_click` (landing page and projects index), `contact_click` (email, LinkedIn, GitHub), `outbound_click`, and `scroll_depth` (25, 50, 75, 100, once each per page load). One test also confirms that an internal link is not counted as outbound.

## How test data stays out of GA4

The tests answer the GA4 request locally, so nothing reaches the property. Pages load with `?internal=1`, the internal traffic flag.

## Run

    npm install
    npx playwright install chromium webkit
    npx playwright test

Set `BASE_URL` to test a different address.

## Limits

The tests confirm that events fire and reach GA4 with the right values. They do not check how GA4 processes or reports them. They depend on the site's current link structure, so a redesign may need updated selectors. The tests were written with GenAI (Claude) from the event specification and run by me.

`tests/event-spec.js` holds the specification as code, and `tests/tracking.spec.js` holds the tests.
