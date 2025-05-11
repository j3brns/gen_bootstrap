# Design Principles

This document outlines the core design principles that guide the development of the GCP Generative AI ADK Scaffold and the applications built using it. Adhering to these principles helps ensure the scaffold is robust, maintainable, and effective.

1.  **Modularity and Separation of Concerns:**
    *   Code should be organized into distinct modules (`adk/`, `tools/`, `utils/`, `cli/`) with clear responsibilities.
    *   Minimize dependencies between modules where possible.
    *   This promotes reusability, testability, and maintainability.

2.  **Cloud-Native:**
    *   Leverage managed GCP services (Vertex AI, Cloud Run, Secret Manager, Logging, Trace, Monitoring, Firestore) where appropriate to reduce operational overhead and benefit from scalability and reliability.
    *   Design for deployment on serverless platforms like Cloud Run.

3.  **Modern Build Automation:**
    *   Utilize modern container build practices and tools, specifically leveraging Google Cloud Build with BuildKit support.
    *   Benefit from faster builds, improved caching, and enhanced security provided by BuildKit.

4.  **Land Cloud Innovation Directly:**
    *   Interact directly with core cloud services and APIs (e.g., Vertex AI models via SDK) rather than introducing unnecessary intermediate layers, facades, or internal gateways.
    *   Avoid introducing technical debt or latency by adding redundant abstraction layers over managed cloud services.

5.  **Developer Experience (DX):**
    *   Provide a user-friendly CLI to automate common tasks and simplify the development workflow.
    *   Offer a clear and intuitive project structure.
    *   Include comprehensive documentation (README, plan, ADRs, feature cards, troubleshooting, glossary, contributing).
    *   Integrate tools that enhance developer productivity (Poetry, pre-commit, notebooks).

6.  **Observability:**
    *   Integrate robust logging (Cloud Logging) and tracing (Cloud Trace) to provide visibility into application behavior, performance, and errors in production.
    *   Support monitoring and alerting (Cloud Monitoring/Alerting) for proactive issue detection.
    *   Offer optional enhanced observability tools (Weave) for deeper analysis and experimentation tracking.

7.  **Security:**
    *   Prioritize secure handling of sensitive information using managed services like Google Secret Manager.
    *   Follow GCP IAM best practices to ensure least privilege access for deployed services.

8.  **Testability:**
    *   Design code components to be easily testable in isolation.
    *   Integrate a testing framework (`pytest`) and mocking tools (`pytest-mock`).
    *   Provide a clear structure for unit and integration tests.

9.  **Experimentation Support:**
    *   Provide tools and structure (`notebooks/`, `evaluation/`, Vertex AI Prompt Classes, optional Weave) that facilitate rapid iteration, prototyping, and evaluation of models, prompts, and agent behaviors.

10. **Low-Fidelity GUIs for Testing and PoC:**
    *   Employ simple, low-fidelity graphical user interfaces (GUIs), such as Gradio or Streamlit, for rapid testing and demonstrating Proofs of Concept.
    *   Prioritize speed of development and ease of use over extensive customization for these testing interfaces.

11. **Standardization and Repeatability:**
    *   Use standard Python practices and widely adopted tools (Poetry, pytest, black, etc.).
    *   Document architectural decisions (ADRs) to provide context for key choices.
    *   Automate build and deployment processes to ensure repeatability.

12. **Resilience and Reliability:**
    *   Implement retry logic for interactions with external services.
    *   Design agents to handle errors gracefully.
    *   Leverage the reliability of managed GCP services.

## Technology Stack

*   **Language:** Python
*   **Package Manager:** Poetry
*   **Core Agent Framework:** Google Agent Development Kit (ADK)
*   **CLI Framework:** Typer/Click
*   **Web Framework (if needed for ADK app):** FastAPI/Uvicorn
*   **Testing Framework:** pytest

These principles will guide the ongoing development and evolution of the scaffold, ensuring it remains a valuable resource for building generative AI applications on GCP.
