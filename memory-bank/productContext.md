# Product Context

This document explains the purpose of the project, the problems it solves, how it should work, and the user experience goals.

## Purpose:
To provide a scaffold for building generative AI projects on GCP using the Google Agent Development Kit (ADK).

## Problems Solved:
- Accelerates the setup of generative AI projects.
- Provides a structured project foundation.
- Integrates google-adk for agent logic.
- Automates common development lifecycle tasks (local run, deployment).

## How it Works:
The project uses Python with Poetry for dependency management. It integrates the google-adk for defining agent logic and tools. A FastAPI application serves the agent via HTTP, including the ADK Web UI. A Typer-based CLI provides commands for project setup, running, deployment, and interacting with GCP services like Vertex AI Prompt Registry and Secret Manager.

## User Experience Goals:
- Provide a quick and easy way to start new generative AI projects on GCP.
- Offer a clear and well-structured project layout.
- Simplify the process of running agents locally and deploying them to Cloud Run.
- Provide helpful CLI tools for managing prompts and secrets on GCP.
