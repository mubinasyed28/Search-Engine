# ReimburseAI — AI-Powered Reimbursement Automation

## Inspiration

A reimbursement claim shouldn't require someone from finance to spend 15 minutes opening receipts, checking calculations, searching for duplicates and cross-checking company policies.

We noticed how much of this process is still manual, especially for incubators managing expenses across multiple startups. As claims pile up, processing becomes slower, errors become more likely, and tracking every reimbursement becomes increasingly difficult.

That's what inspired us to build **ReimburseAI** — an AI-powered reimbursement platform that takes over the repetitive work while keeping financial decisions transparent and accountable.

## What We Built

ReimburseAI is an agentic reimbursement automation platform designed for incubators, startups and growing organizations.

A founder uploads receipts or invoices, and a coordinated pipeline of agents takes over the entire verification and decision-making workflow.

- **Ingestion & OCR:** Reads uploaded PDFs and images using Tesseract.js and converts documents into readable information.
- **AI Extraction:** Uses OpenAI and Azure OpenAI to extract vendors, dates, amounts, taxes and expense categories into structured data.
- **Verification Agent:** Checks calculations, missing fields, document inconsistencies and confidence levels.
- **Duplicate Detection Agent:** Identifies previously submitted or potentially manipulated receipts using document matching.
- **Policy Agent:** Evaluates expenses against reimbursement rules, spending limits, eligible categories and receipt requirements.
- **Reconciliation Agent:** Compares claimed and eligible amounts against available budgets and financial records.
- **Risk Scoring Agent:** Assigns a risk score and routes claims for automatic approval, human review or rejection.

We also built a dedicated finance workspace using **AG Grid**, allowing reviewers to inspect flagged claims, understand why they were flagged, correct extracted information inline and approve or reject claims individually or in bulk.

The payment workflow is designed around **PayPal Payouts**, with payout instructions, payment states and reconciliation incorporated into the architecture.

## How We Built It

We built the MVP using Next.js, TypeScript, OpenAI, Azure OpenAI, Tesseract.js and AG Grid.

The agents work together through an orchestrated workflow, combining AI-powered document extraction and analysis with deterministic rules for financial calculations, policy enforcement and approval decisions.

We also designed the application around a multi-tenant architecture, where each organization can have its own users, reimbursement policies, spending limits, risk thresholds and approval workflows.

## Challenges and Learnings

One of our biggest challenges was deciding where AI should make suggestions and where it should never have the final say. Financial calculations and approvals cannot depend entirely on an LLM.

We addressed this by separating AI-driven intelligence from deterministic validation and decision logic, ensuring that every financial decision has an understandable reason behind it.

Handling blurry receipts, inconsistent invoice formats, duplicate documents and edge cases in reimbursement policies also pushed us to think beyond simply extracting text.

The biggest thing we learned was that building an AI agent isn't just about making an LLM perform a task. It's about designing a reliable system where multiple agents collaborate, decisions remain explainable and humans stay in control when it matters.

**Our goal is to make reimbursements faster for founders, more reliable for organizations and significantly less repetitive for finance teams.**
