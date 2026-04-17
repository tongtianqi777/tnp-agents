---
name: seth-volunteering-hours-logging
description: Log volunteer hours to the Seth school Google Form. Trigger when the user says "log volunteer hours", "record volunteering", "submit hours for Seth", or describes school volunteering activities with a duration.
---

# Seth Volunteering Hours Logging

Submit volunteer hours to the Seth school Google Form on behalf of the Tong family.

## Step 1 — Extract Required Information

Parse the user's message for:

| Field | Rule |
|---|---|
| Activities | What was done (one or more) |
| Hours per activity | Must be a number; ask if missing |
| Day of each activity | Day of week or date; **default to today if not mentioned** |

If hours are missing and cannot be inferred, ask the user before proceeding.

## Step 2 — Compute Derived Values

**Sunday of the week** (needed for the form):
- Find the most recent Sunday on or before the activity date.
- If activities span multiple weeks, submit one form per week.
- Format: `MM/DD/YYYY`

**Total hours**: sum all activity hours for the week.

**Volunteer Category** (one or both checkboxes):
- **On-site** — activity on school campus: onsite helper, lunchtime helper, classroom helper, library helper.
- **Off-site** — activity off campus: Yearbook planner, Field Trip planner, Website management, newsletter editing.
- Both may be checked if the week includes both types.

**Description of Work**: short comma-separated list of activities (see Reference for style).

## Step 3 — Show Summary and Confirm

Before doing anything, show the user a summary and ask for confirmation:

> Ready to submit:
> - Week of: `<sunday date>`
> - Total hours: `<hours>`
> - Category: `<On-site / Off-site / Both>`
> - Description: `<description>`
>
> Confirm to submit?

Only proceed after the user confirms.

## Step 4 — Fill the Google Form via Local Playwright Script

### One-time setup (skip if already done)

Check if Python playwright is installed:
```bash
python3 -c "import playwright" 2>/dev/null || pip3 install playwright && python3 -m playwright install chromium
```

### Write and run the script

Write the following script to `/tmp/seth_volunteer.py`, substituting the actual values for `SUNDAY_DATE`, `TOTAL_HOURS`, `ONSITE`, `OFFSITE`, and `DESCRIPTION`:

```python
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfLkd4OZIHvHpQdLgxxSNzo9_TX6oHQbPtzRbw96oKy9E2bAw/viewform"
CHROME_USER_DATA = "/Users/tnpbot/Library/Application Support/Google/Chrome"
CHROME_PROFILE = "Profile 3"  # Zoey — already signed into Google

SUNDAY_DATE = "<MM/DD/YYYY>"
TOTAL_HOURS = "<number>"
ONSITE = <True or False>
OFFSITE = <True or False>
DESCRIPTION = "<description text>"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        CHROME_USER_DATA,
        channel="chrome",
        args=[f"--profile-directory={CHROME_PROFILE}"],
        headless=False,
    )
    page = ctx.new_page()
    page.goto(FORM_URL, wait_until="networkidle")

    # Email checkbox
    email_cb = page.get_by_text("Record tianqi.tong@svca.cc").locator("xpath=ancestor::*[contains(@class,'freebirdFormviewerViewItemsCheckboxChoice')]//div[@role='checkbox']")
    if email_cb.get_attribute("aria-checked") != "true":
        email_cb.click()

    # Family dropdown
    page.get_by_role("listbox").first.click()
    page.get_by_role("option", name="Tong (Samuel)").click()

    # Week of (Starting Sunday)
    page.get_by_label("Week of (Starting Sunday)").fill(SUNDAY_DATE)

    # Total Volunteer Hours
    page.get_by_label("Total Volunteer Hours").fill(str(TOTAL_HOURS))

    # Checkboxes
    if ONSITE:
        onsite = page.get_by_text("On-site").locator("xpath=ancestor::*[contains(@class,'freebirdFormviewerViewItemsCheckboxChoice')]//div[@role='checkbox']")
        if onsite.get_attribute("aria-checked") != "true":
            onsite.click()
    if OFFSITE:
        offsite = page.get_by_text("Off-site").locator("xpath=ancestor::*[contains(@class,'freebirdFormviewerViewItemsCheckboxChoice')]//div[@role='checkbox']")
        if offsite.get_attribute("aria-checked") != "true":
            offsite.click()

    # Description
    page.get_by_label("Description of Work").fill(DESCRIPTION)

    # Submit
    page.get_by_role("button", name="Submit").click()
    page.wait_for_url("**/formResponse*", timeout=10000)
    print("Submitted successfully.")
    ctx.close()
```

Run it:
```bash
python3 /tmp/seth_volunteer.py
```

### Troubleshooting

- **Chrome is already open with Profile 3**: close all Chrome windows, then retry.
- **`aria-checked` selector doesn't match**: use `page.screenshot(path="/tmp/form.png")` before the failing line to inspect the page visually.
- **Date field rejects input**: try `page.get_by_label("Week of (Starting Sunday)").click()` then `.fill()`.
- **Dropdown won't open**: scroll it into view with `.scroll_into_view_if_needed()` then `.click()`.

## Operating Rules

- If activities span two calendar weeks, run the script twice — once per week with adjusted dates and hours.
- Do not guess ambiguous activity categories; default to On-site if the activity location is unclear and note the assumption to the user.

## Reference — Example Activity Descriptions

| Activity | Category | Example description |
|---|---|---|
| Help at lunch | On-site | Lunchtime helper |
| Classroom aide | On-site | Classroom helper |
| Help set up/clean event on campus | On-site | Onsite event helper |
| Yearbook layout/design | Off-site | Yearbook planner |
| Plan a field trip | Off-site | Field Trip planner |
| School website updates | Off-site | Website management |
| Write/edit school newsletter | Off-site | Newsletter editing |
