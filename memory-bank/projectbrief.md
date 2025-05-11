# Project Brief

This document outlines the core requirements and goals of the project.

## Project Name:
GCP Generative AI Scaffold (gen-bootstrap)

## Project Goals:
To accelerate the development of generative AI projects using the official Google Agent Development Kit (google-adk) on Google Cloud Platform (GCP). Provide a well-structured project foundation, integrate google-adk for agent logic, and automate common tasks throughout the development lifecycle, from local development to deployment on Cloud Run.

## Key Requirements:
- Use Python 3.9+
- Use Poetry for dependency management
- Integrate Google Agent Development Kit (google-adk) for agent logic
- Use FastAPI for serving the agent via HTTP
- Use Typer for the CLI (gen-bootstrap)
- Deploy on Google Cloud Platform (GCP), specifically Cloud Run
- Integrate with GCP services like Vertex AI and Secret Manager

## Scope:
- Project structure for google-adk based applications
- Core agent logic implementation
- Example custom tool
- Functional CLI for init, run, deploy, setup-gcp, tools list/describe, prompts list/get/create, secrets list/get/create/add-version
- FastAPI server integrated with google-adk and ADK Web UI
- Basic structured logging and configuration management
- Example Gradio test client
- Documentation (ADRs, guides, tutorials, plan)

## Non-Goals:
(Based on the provided README, specific non-goals are not explicitly stated. I will leave this section open for now.)
