#!/usr/bin/env python3
"""
NUAA CLI A2A (Agent-to-Agent) Module
=====================================

Provides Agent-to-Agent communication protocol implementation for NUAA CLI,
enabling coordinated multi-agent workflows and collaborative task execution.

This module implements a lightweight message bus that allows agents to:
- Discover other agents and their capabilities
- Send messages and requests to other agents
- Subscribe to events and notifications
- Coordinate complex workflows across multiple agents

Public API:
    - A2ACoordinator: Main coordinator for agent communication
    - A2AMessage: Message format for agent communication
    - A2AAgent: Agent representation with capabilities
    - register_agent: Register an agent with the coordinator
    - send_message: Send a message to another agent

Author: NUAA Project
License: MIT
"""

from .coordinator import A2ACoordinator, A2AAgent, A2AMessage
from .exceptions import A2AError, AgentNotFoundError, MessageDeliveryError

__all__ = [
    "A2ACoordinator",
    "A2AAgent",
    "A2AMessage",
    "A2AError",
    "AgentNotFoundError",
    "MessageDeliveryError",
]
