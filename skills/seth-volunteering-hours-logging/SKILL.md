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

If hours are missing and cannot be inferred, ask before proceeding.

## Step 2 — Compute Derived Values

**Sunday of the week** (needed for the form):
- From the activity date(s), find the most recent Sunday on or before that date.
- If activities span multiple weeks, submit one form per week.
- Format: `MM/DD/YYYY`

**Total hours**: sum all activity hours for the week.

**Volunteer Category** (select one or both):
- Check **On-site** if any activity takes place on school campus — e.g., onsite helper, lunchtime helper, classroom helper, library helper.
- Check **Off-site** if any activity takes place outside school campus — e.g., Yearbook planner, Field Trip planner, Website management, newsletter editing.
- Both boxes may be checked if activities span both categories.

**Description of Work**: a short comma-separated list of the activities, matching the style in the Reference section below.

## Step 3 — Fill the Google Form

Use the Chrome profile **"Zoey Bot"** to open:
`https://docs.google.com/forms/d/e/1FAIpQLSfLkd4OZIHvHpQdLgxxSNzo9_TX6oHQbPtzRbw96oKy9E2bAw/viewform`

Fill each field in order:

1. **Email checkbox** — select "Record tianqi.tong@svca.cc as the email to be included with my response"
2. **Family** — select `Tong (Samuel)` from the dropdown
3. **Week of (Starting Sunday)** — enter the Sunday date computed in Step 2
4. **Total Volunteer Hours** — enter the total hours computed in Step 2
5. **Volunteer Category** — check the appropriate box(es) per the logic in Step 2
6. **Description of Work** — enter the activity description from Step 2

Submit the form and confirm success to the user.

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
