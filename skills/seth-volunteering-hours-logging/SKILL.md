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

## Step 3 — Fill the Google Form via Firecrawl

Open the form using the Chrome profile **"Zoey"**:
`https://docs.google.com/forms/d/e/1FAIpQLSfLkd4OZIHvHpQdLgxxSNzo9_TX6oHQbPtzRbw96oKy9E2bAw/viewform`

Use Firecrawl interact prompts to fill the form in order:

1. Click the checkbox labeled **"Record tianqi.tong@svca.cc as the email to be included with my response"** to select it.
2. Click the **Family** dropdown and select **"Tong (Samuel)"**.
3. Click the **"Week of (Starting Sunday)"** field and type the Sunday date (MM/DD/YYYY).
4. Click the **"Total Volunteer Hours"** field and type the total hours.
5. Click the **"On-site"** checkbox if applicable; click the **"Off-site"** checkbox if applicable.
6. Click the **"Description of Work"** text area and type the activity description.

Before clicking Submit, **pause and show the user a summary** of what will be submitted:

> Ready to submit:
> - Week of: `<sunday date>`
> - Total hours: `<hours>`
> - Category: `<On-site / Off-site / Both>`
> - Description: `<description>`
>
> Confirm to submit?

Only proceed to click **Submit** after the user confirms. After submitting, confirm success to the user.

## Operating Rules

- If the form page does not load with Zoey Bot profile, retry once before reporting failure.
- If a dropdown or checkbox is not clickable (obscured or overlapped), scroll it into view first.
- If the week's activities span two calendar weeks, submit two separate forms — one per week.
- Do not guess ambiguous activity categories; default to On-site if the activity location is unclear and note the assumption to the user.

## Troubleshooting

- **Dropdown won't open**: use Firecrawl interact to scroll the element into view, then click.
- **Date field rejects input**: try clicking to focus first, then clear existing content, then type.
- **Form submission fails**: check that all required fields are filled; Google Forms marks required fields with a red asterisk on error.

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
