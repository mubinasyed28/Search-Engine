# Build a General-Purpose AI Research & Structured Data Engine

I want you to build a **fully working local web application**, not a prototype or demo.

The purpose of this application is to automate repetitive research work.

The system must accept a natural-language research request, optionally accept an uploaded file and user-provided URLs, research the web according to explicit source rules, extract and validate structured information, create a properly formatted Google Sheet, show the sources and research parameters, and allow the user to delete the temporary research data once the result has been verified.

## 1. CORE PRODUCT CONCEPT

This is NOT a university-only application.

It is a **general-purpose research and structured-data generation engine**.

Examples of valid requests:

- Find 500 universities with QS ranking, tuition, acceptance rate, official website, admissions email, etc.
- Find courses available after Grade 10 with eligibility, duration, fees, colleges, and career options.
- Find extracurricular activities for Grade 7–12 students with activity type, eligibility, fees, location, organizer, website, registration link, etc.
- Find competitions, Olympiads, internships, summer programs, volunteering opportunities, scholarships, companies, products, market information, or any other structured web research.
- Any research request where the user wants the information converted into rows/columns and exported to Google Sheets.

The application must be domain-agnostic.

Do not hard-code university-specific fields into the core engine.

The system must dynamically derive the entity type and requested fields from the user's request.

---

# 2. TECHNOLOGY STACK

Use:

- Python
- Streamlit
- MongoDB Atlas
- Tavily API
- Google Sheets API
- Google Drive API where needed
- An LLM provider through a configurable abstraction layer
- pandas
- openpyxl
- requests/httpx
- BeautifulSoup where useful
- pydantic for structured schemas/validation
- python-dotenv for environment configuration

Do NOT use MySQL.

Use MongoDB only for temporary research-job state and intermediate structured data.

Do not permanently retain completed research jobs.

---

# 3. APPLICATION UI

Build a polished, clean Streamlit interface.

The primary screen should contain:

## Header

"Research & Data Engine"

Short description:

"Turn research requirements into verified structured data."

## Research Request

Large chat/text input:

"What do you want me to research?"

Example:

"Find extracurricular activities for Grade 7–12 students in India. I need activity name, category, age eligibility, grade eligibility, location, online/offline, fees, organizer, official website, registration link and contact details."

## File Upload

Allow:

- CSV
- XLSX
- PDF

Uploaded files may contain:

- lists of entities
- existing rows
- requirements
- source information
- research data

The system should intelligently determine how the uploaded file should be used.

Examples:

"These are the 500 universities I want researched."

or

"Use these existing rows and fill the missing columns."

## Add URLs

Provide an "Add URLs" area.

Allow multiple URLs.

Each URL can optionally have an instruction.

Example:

URL:
https://example.com/rankings

Instruction:
"Use this source strictly for ranking."

Users should also be able to say in natural language:

"QS ranking must come only from QS."

The system should convert this into an explicit source rule.

## Search Mode

Allow:

- Auto
- Basic
- Advanced

Default: Auto.

Auto should use Basic Search first and escalate to Advanced Search when useful.

## Start Search button

When clicked, create a research job.

---

# 4. REQUEST INTERPRETER

Create a structured research-plan generator.

The LLM should convert the natural-language request into a machine-readable structure such as:

- entity_type
- scope
- entities
- fields
- field descriptions
- source rules
- fallback rules
- search mode
- output preferences
- validation requirements

Example:

{
  "entity_type": "Extracurricular Activity",
  "fields": [
    "name",
    "category",
    "age_eligibility",
    "grade_eligibility",
    "location",
    "online_offline",
    "fees",
    "organizer",
    "official_website",
    "registration_url",
    "contact"
  ],
  "source_rules": {
    "eligibility": {
      "primary": "official_organizer",
      "fallback": false
    },
    "fees": {
      "primary": "official_organizer",
      "fallback": false
    },
    "registration_url": {
      "primary": "official_organizer",
      "fallback": true
    }
  }
}

Do not allow the model to silently change source rules.

Before beginning a large research run, show the user an interpretable Research Plan.

Example:

RESEARCH PLAN

Entities:
500

Fields:
11

Source rules:
QS Ranking → QS only
Tuition → Official university website first, web fallback allowed
Acceptance Rate → Official university website only
Admissions Email → Official website, web fallback allowed

Search mode:
Auto

Button:
START RESEARCH

---

# 5. SOURCE RULE ENGINE

This is one of the most important components.

Every field must have an explicit source policy.

Support:

## Strict source

Example:

"QS ranking only from QS."

Meaning:

- Search QS
- Accept QS sources
- Reject all other sources
- If not found → N/A

## Preferred source + fallback

Example:

"Tuition from official university website, otherwise search the web."

Meaning:

1. Research official source
2. If missing, search fallback sources
3. Validate fallback result
4. Record that fallback was used

## Web search allowed

Example:

"Find the city."

Meaning:

Use web research as appropriate.

## Strict official source

Example:

"Acceptance rate from official university website only. If unavailable, put N/A."

Meaning:

NEVER search other sources.

This rule must be enforced programmatically, not merely by the LLM.

---

# 6. RESEARCH PIPELINE

The core engine should work in progressive passes.

For each entity:

## PASS 1 — PRIMARY SOURCE RESEARCH

Identify the most appropriate primary source.

If an official domain is known, prioritize that domain.

Do NOT perform one independent search for every field.

Instead:

- identify the relevant domain
- search/discover relevant pages
- collect relevant pages
- extract ALL requested fields that can be found
- store source information for each extracted value

For example, for a university:

- admissions
- tuition
- fees
- deadlines
- international students
- requirements
- contact
- program pages

should be researched together where appropriate.

For an extracurricular activity:

- organizer
- eligibility
- fees
- registration
- location
- schedule
- contact

can be gathered from the organizer's relevant pages.

The engine should be intelligent about grouping fields.

---

# 7. TAVILY RESEARCH STRATEGY

Use Tavily for web discovery and retrieval.

Implement a Tavily service abstraction.

Support:

- Basic Search
- Advanced Search
- Extract where appropriate

Do not blindly perform thousands of searches.

Use the following strategy:

1. Search for the entity/primary source.
2. Identify relevant pages.
3. Retrieve/extract relevant content.
4. Extract multiple fields from the available sources in one pass.
5. Identify unresolved fields.
6. Check source rules.
7. Only search unresolved fields if fallback is allowed.
8. Escalate from Basic to Advanced when necessary.

Cache results during a research job so identical searches are not repeatedly executed.

Avoid duplicate URLs.

Track Tavily credits/search counts.

---

# 8. USER-PROVIDED URL HANDLING

When the user provides URLs:

Treat these as explicit sources.

If the user says:

"QS ranking strictly from this URL"

then the engine must:

- prioritize that source
- use it only for the relevant field
- not replace it with another source
- return N/A if the information is unavailable there

Allow one URL to apply to multiple fields.

Allow separate URLs for different fields.

---

# 9. EXTRACTION ENGINE

All extracted data must be structured.

Every field result should contain at least:

- value
- source_url
- source_type
- source_title if available
- evidence
- confidence
- retrieved_at
- status

Example:

{
  "field": "tuition",
  "value": "$61,000",
  "source_url": "https://...",
  "source_type": "official",
  "evidence": "Relevant source passage",
  "confidence": 0.95,
  "status": "verified"
}

Do not allow unsupported values.

Do not hallucinate missing information.

If a field cannot be verified according to its source policy, return:

N/A

and explain why in the audit data.

---

# 10. ENTITY MATCHING

The system must confirm that the retrieved source actually belongs to the requested entity.

For example:

"University of Toronto"

must not accidentally match:

- another University of Toronto-related institution
- an unrelated page
- a similarly named institution

Build normalized entity matching.

Use:

- exact/normalized names
- domain verification
- location/country where relevant
- source context
- LLM verification only as an additional signal

Do not rely solely on semantic similarity.

---

# 11. VALIDATION ENGINE

Implement deterministic validators wherever possible.

Examples:

QS Rank:
- numeric
- appropriate ranking year
- source must meet configured rule

Acceptance Rate:
- numeric percentage where applicable
- between 0 and 100

Email:
- valid email format

Website:
- valid URL
- HTTPS where possible
- domain relevance check

Tuition:
- preserve currency
- preserve annual/semester terminology
- do not arbitrarily convert currencies unless specifically requested

Dates:
- normalize consistently
- retain original source wording in audit data

Do not silently normalize away important meaning.

---

# 12. CONFLICT DETECTION

If multiple allowed sources disagree:

Do not randomly choose a value.

Store all candidate values.

Example:

Acceptance Rate:
35%
41%
38%

Then:

- identify the conflict
- determine whether one source has higher authority
- determine whether one is more recent
- choose a value only when the rules support that choice
- otherwise mark "REVIEW REQUIRED"

The audit sheet must expose the conflict.

---

# 13. SOURCE PROVENANCE

Every field must have a source.

Never output an important value without source provenance.

For each field store:

- source URL
- source type
- retrieval timestamp
- evidence
- confidence/status

Source types may include:

- user_provided
- official
- ranking_source
- government
- reputable_secondary
- web_search
- other

---

# 14. CONFIDENCE / RESEARCH PARAMETERS

Do not use an arbitrary AI-generated confidence score alone.

Build a transparent research-quality indicator.

Consider:

- source authority
- source compliance
- entity match
- extraction quality
- corroboration
- recency
- conflict status
- whether fallback was used

Show a Research Parameters panel.

Example:

RESEARCH PARAMETERS

Universities: 500
Fields requested: 5,500
Fields collected: 5,071
N/A: 291
Needs Review: 138
Primary-source coverage: 94.8%
Source compliance: 99.1%
High-confidence results: 91.7%
Web searches: 1,142
URLs analyzed: 4,386
Tavily credits used: XXX

These values must be calculated from the actual job.

---

# 15. RESULTS UI

After research, show:

## Google Sheet

A prominent button:

OPEN GOOGLE SHEET

Also show:

- spreadsheet name
- creation time
- number of rows
- number of fields

## Sources

Show a source summary below the Google Sheet.

Example:

University of Toronto

Official website:
https://...

QS:
https://...

Additional sources:
...

Allow users to inspect field-level sources.

## Research Parameters

Show the calculated metrics.

## Review Required

Show only problematic results.

Examples:

- missing allowed value
- source conflict
- low confidence
- entity mismatch
- strict-source value unavailable

This allows the user to focus on exceptions rather than manually inspect everything.

---

# 16. GOOGLE SHEETS

Use Google Sheets API to create a new spreadsheet.

The output should contain at least:

## Sheet 1 — Final Data

One row per entity.

Columns dynamically generated based on requested fields.

Example:

University | QS Rank | Tuition | Acceptance Rate | Website | Email

or:

Activity | Category | Grade Eligibility | Fee | Organizer | Registration URL

## Sheet 2 — Sources / Audit

Columns:

Entity
Field
Value
Source URL
Source Type
Evidence
Confidence
Status
Retrieved At
Fallback Used

## Sheet 3 — Review Required

Include only records requiring attention.

Automatically format the sheet:

- freeze header
- enable filters
- reasonable column widths
- readable headers
- wrapped text where needed
- preserve URLs
- consistent formatting

Return the Google Sheet URL to the user.

---

# 17. GOOGLE SHEET SHARING

Implement Google Drive permission handling.

After creation:

- share the file with the authenticated user
- return the accessible link

Do not expose the spreadsheet publicly by default.

Use the least-permissive sharing configuration necessary.

---

# 18. TEMPORARY MONGODB STORAGE

Use MongoDB Atlas only for research-job state.

A job should contain information such as:

- job_id
- request
- interpreted_plan
- entity list
- source rules
- progress
- results
- sources
- validation
- Google Sheet URL
- created_at
- expires_at
- status

Do not use MongoDB as an unnecessary permanent archive.

After the user clicks:

DONE & PERFECT

delete the research job and associated temporary data.

Also implement an automatic expiry mechanism using expires_at / MongoDB TTL so abandoned jobs are eventually deleted automatically.

Do not retain scraped content permanently.

Prefer storing concise evidence/source metadata rather than huge raw website dumps.

---

# 19. JOB RESUMPTION AND FAILURE HANDLING

The system must be robust.

If researching 500 entities and the process encounters an error:

- do not lose all completed work
- update job progress
- retry transient errors
- continue with remaining entities where safe
- record failures
- allow the user to resume or re-run failed items

Create clear statuses such as:

- pending
- researching
- completed
- needs_review
- failed
- expired

Do not restart a completed university/entity unnecessarily.

---

# 20. CONCURRENCY

500 entities should not be processed sequentially if parallelism is safe.

Implement controlled asynchronous/concurrent processing.

Do not exceed API rate limits.

Use:

- bounded concurrency
- retries
- backoff
- caching

Avoid uncontrolled parallel requests.

---

# 21. CONFIGURATION

Create a .env example:

TAVILY_API_KEY=
MONGODB_URI=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
LLM_API_KEY=
LLM_PROVIDER=

Never hard-code credentials.

Create a configuration module.

---

# 22. PROJECT STRUCTURE

Create a clean project structure approximately like:

research_engine/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── config/
│   └── settings.py
│
├── ui/
│   ├── research_form.py
│   ├── plan_view.py
│   ├── progress_view.py
│   ├── results_view.py
│   └── components.py
│
├── ingestion/
│   ├── csv_reader.py
│   ├── excel_reader.py
│   └── pdf_reader.py
│
├── planning/
│   ├── request_parser.py
│   ├── schema_generator.py
│   └── source_rules.py
│
├── research/
│   ├── orchestrator.py
│   ├── tavily_client.py
│   ├── search_strategy.py
│   ├── url_discovery.py
│   └── cache.py
│
├── extraction/
│   ├── extractor.py
│   ├── normalizer.py
│   └── schemas.py
│
├── validation/
│   ├── validators.py
│   ├── entity_matcher.py
│   ├── provenance.py
│   └── conflicts.py
│
├── storage/
│   ├── mongodb.py
│   └── job_repository.py
│
├── sheets/
│   ├── google_auth.py
│   ├── google_sheets.py
│   └── formatting.py
│
├── models/
│   ├── research_job.py
│   ├── research_plan.py
│   └── research_result.py
│
└── utils/
    ├── logging.py
    ├── retries.py
    └── helpers.py

You may improve this structure if a better engineering structure is appropriate.

---

# 23. IMPORTANT DESIGN PRINCIPLES

These rules are mandatory:

1. Do not hallucinate data.
2. Every extracted value must have provenance.
3. Strict source rules must be enforced.
4. If a strict source does not contain the requested information, return N/A.
5. Do not silently use fallback sources.
6. Research fields in grouped passes where possible.
7. Avoid duplicate Tavily searches.
8. Cache research within the job.
9. Validate data before putting it in the final spreadsheet.
10. Preserve source evidence.
11. Flag conflicts instead of hiding them.
12. Keep temporary research data temporary.
13. The engine must remain domain-agnostic.
14. The user should be able to research any structured topic.
15. The application should work for 5 entities and 500 entities using the same architecture.

---

# 24. DEVELOPMENT EXPECTATION

I want actual working code.

Do not only generate pseudocode.

Create the files.

Install/use the required packages.

Run the Streamlit application.

Run tests for core components.

Fix errors that arise.

Provide:

1. Complete source code.
2. requirements.txt
3. .env.example
4. README.md
5. Google API setup instructions.
6. Tavily setup instructions.
7. MongoDB Atlas setup instructions.
8. How to run locally.
9. How to test using a small example.
10. Any known limitations.

Do not stop at scaffolding.

---

# 25. FIRST TEST CASE

After implementation, test the application with a small but realistic request such as:

"Find 5 extracurricular activities suitable for Grade 7–12 students in India. I need activity name, category, grade eligibility, age eligibility, location, online/offline, fee, organizer, official website, registration link and contact details. Use official organizer websites for eligibility, fees and registration. If those fields are unavailable on the official source, use N/A. Other discovery information may use web search."

Verify that:

- the research plan is generated
- source rules are correctly interpreted
- official-source restrictions are enforced
- missing strict-source fields become N/A
- sources are recorded
- validation works
- the Google Sheet is created
- the audit sheet is created
- the result can be reviewed
- DONE & PERFECT deletes temporary job data

Then test a second scenario with an uploaded CSV containing universities.

---

# 26. USER EXPERIENCE GOAL

The application should feel like:

"I tell it what research I need, define where the information should come from, click Search, and receive a trustworthy structured Google Sheet."

The user should NOT have to:

- write complicated search prompts
- manually search each entity
- copy/paste data
- manually identify sources
- manually format the spreadsheet
- repeatedly prompt an LLM
- manually clean up hundreds of rows

That repetitive work is exactly what this application is supposed to automate.

Build the complete working system now.