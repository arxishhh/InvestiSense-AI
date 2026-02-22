# 🚀 InvestiSense AI — Financial Intelligence System

InvestiSense AI is a **multi-agent financial intelligence system** that retrieves evidence from filings, financial statements, and market news to produce **grounded financial explanations**.

Instead of a single chatbot, the system uses **coordinated agents and a supervisor workflow** to collect, verify, and synthesize financial information.

---

## 📝 Description

InvestiSense AI is designed to answer **financial reasoning queries using verifiable evidence**.

The system:
- Retrieves financial statements and filing sections
- Collects real-time market data and financial news
- Stores provenance metadata for traceable reasoning
- Produces grounded financial explanations using LLM analysis

The architecture follows a **supervisor-orchestrated multi-agent workflow** where agents iteratively collect evidence until sufficient information is available to answer a query.

---

## 🧠 System Architecture

InvestiSense AI uses a **LangGraph supervisor-orchestrated architecture** with shared state.

Agents in the system:

- **Supervisor Agent** — routes tasks and manages workflow execution
- **Auditor Agent** — retrieves 10-K / 10-Q filing evidence
- **Financer Agent** — retrieves financial statements and metrics
- **Newsroom Agent** — retrieves financial news and real-time stock data
- **Analyzer Node** — synthesizes collected financial evidence
- **Replier Node** — generates the final user explanation

Agents run **iteratively until evidence convergence or iteration limits are reached**.

---

## ✨ Features

- Multi-agent financial reasoning pipeline
- Supervisor-based orchestration using LangGraph
- Evidence-driven financial analysis
- Retrieval from:
  - SEC filings (10-K / 10-Q)
  - Financial statements
  - Market news
  - Real-time stock data
- Provenance-aware evidence storage
- FastAPI backend for query execution
- JWT authentication for API access
- Redis caching for retrieval optimization
- Structured logging and exception handling
- CLI interface for running financial-analysis queries

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- LangGraph
- Redis
- JWT Authentication

### AI / Retrieval
- LLM APIs (Gemini / ChatGroq)
- RAG-based evidence retrieval
- yFinance
- Filing retrieval tools

### System Design
- Multi-agent orchestration
- Shared-state execution model
- Provenance-aware evidence pipeline
- Structured logging

---

