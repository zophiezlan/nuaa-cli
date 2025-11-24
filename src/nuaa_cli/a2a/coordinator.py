#!/usr/bin/env python3
"""
A2A Coordinator - Agent-to-Agent Communication Coordinator
===========================================================

Provides a message bus for agent-to-agent communication, enabling
collaborative workflows and coordinated task execution across multiple agents.

Key Features:
- Agent registration and discovery
- Message routing and delivery
- Event subscription and notification
- Capability-based agent matching
- Message queuing and history

Example Usage:
    >>> from nuaa_cli.a2a import A2ACoordinator, A2AAgent, A2AMessage
    >>>
    >>> # Create coordinator
    >>> coordinator = A2ACoordinator()
    >>>
    >>> # Register agents
    >>> agent1 = A2AAgent(
    ...     id="design-agent",
    ...     name="Design Agent",
    ...     capabilities=["design_program", "create_logic_model"],
    ...     message_handler=lambda msg: f"Handled: {msg.content}"
    ... )
    >>> coordinator.register(agent1)
    >>>
    >>> # Send message
    >>> message = A2AMessage(
    ...     from_agent="user",
    ...     to_agent="design-agent",
    ...     content={"action": "design_program", "params": {...}}
    ... )
    >>> result = coordinator.send(message)

Author: NUAA Project
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Optional
from uuid import uuid4

from .exceptions import (
    AgentNotFoundError,
    AgentRegistrationError,
    InvalidMessageError,
    MessageDeliveryError,
)


@dataclass
class A2AMessage:
    """
    Message format for agent-to-agent communication.

    Attributes:
        from_agent: Sender agent ID
        to_agent: Recipient agent ID
        content: Message payload (any JSON-serializable data)
        message_type: Type of message ("request", "response", "notification", "event")
        message_id: Unique message identifier (auto-generated)
        timestamp: Message creation timestamp (auto-generated)
        reply_to: Optional message ID this is replying to
        metadata: Optional additional metadata
    """

    from_agent: str
    to_agent: str
    content: Any
    message_type: str = "request"
    message_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reply_to: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate message after initialization."""
        valid_types = ["request", "response", "notification", "event"]
        if self.message_type not in valid_types:
            raise InvalidMessageError(
                f"Invalid message_type '{self.message_type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )


@dataclass
class A2AAgent:
    """
    Agent representation for A2A communication.

    Attributes:
        id: Unique agent identifier
        name: Human-readable agent name
        capabilities: List of capabilities/actions the agent can perform
        message_handler: Callable that processes incoming messages
        description: Optional agent description
        metadata: Optional additional metadata
    """

    id: str
    name: str
    capabilities: list[str]
    message_handler: Callable[[A2AMessage], Any]
    description: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class A2ACoordinator:
    """
    Coordinator for agent-to-agent communication.

    Manages agent registration, message routing, and event delivery.
    Provides a central message bus for multi-agent coordination.

    Attributes:
        _agents: Dictionary mapping agent IDs to agent instances
        _message_history: List of recent messages (configurable max size)
        _max_history: Maximum number of messages to keep in history
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize the A2A coordinator.

        Args:
            max_history: Maximum number of messages to keep in history
        """
        self._agents: dict[str, A2AAgent] = {}
        self._message_history: list[A2AMessage] = []
        self._max_history = max_history

    def register(self, agent: A2AAgent) -> None:
        """
        Register an agent with the coordinator.

        Args:
            agent: Agent instance to register

        Raises:
            AgentRegistrationError: If agent ID is invalid or already registered
        """
        if not agent.id or not agent.id.strip():
            raise AgentRegistrationError("Agent ID cannot be empty")

        if agent.id in self._agents:
            raise AgentRegistrationError(f"Agent '{agent.id}' is already registered")

        self._agents[agent.id] = agent

    def unregister(self, agent_id: str) -> None:
        """
        Unregister an agent from the coordinator.

        Args:
            agent_id: ID of agent to unregister

        Raises:
            AgentNotFoundError: If agent is not registered
        """
        if agent_id not in self._agents:
            raise AgentNotFoundError(f"Agent '{agent_id}' is not registered")

        del self._agents[agent_id]

    def send(self, message: A2AMessage) -> Any:
        """
        Send a message to an agent and return the response.

        Args:
            message: Message to send

        Returns:
            Response from the recipient agent's message handler

        Raises:
            AgentNotFoundError: If recipient agent is not registered
            MessageDeliveryError: If message delivery fails
        """
        # Validate recipient exists
        if message.to_agent not in self._agents:
            raise AgentNotFoundError(
                f"Recipient agent '{message.to_agent}' not found. "
                f"Available agents: {', '.join(self._agents.keys())}"
            )

        # Add to history
        self._add_to_history(message)

        # Deliver message
        recipient = self._agents[message.to_agent]

        try:
            return recipient.message_handler(message)
        except Exception as e:
            raise MessageDeliveryError(
                f"Failed to deliver message to '{message.to_agent}': {str(e)}"
            ) from e

    def broadcast(
        self, message: A2AMessage, capability: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Broadcast a message to all agents (or those with specific capability).

        Args:
            message: Message to broadcast
            capability: Optional capability filter

        Returns:
            Dictionary mapping agent IDs to their responses
        """
        responses = {}

        for agent_id, agent in self._agents.items():
            # Skip sender
            if agent_id == message.from_agent:
                continue

            # Filter by capability if specified
            if capability and capability not in agent.capabilities:
                continue

            # Create copy of message for this recipient
            agent_message = A2AMessage(
                from_agent=message.from_agent,
                to_agent=agent_id,
                content=message.content,
                message_type=message.message_type,
                message_id=str(uuid4()),  # New ID for each recipient
                reply_to=message.message_id,
                metadata=message.metadata,
            )

            try:
                responses[agent_id] = agent.message_handler(agent_message)
            except Exception as e:
                responses[agent_id] = {"error": str(e)}

        return responses

    def find_agents(
        self, capability: str, exclude: Optional[list[str]] = None
    ) -> list[A2AAgent]:
        """
        Find agents with a specific capability.

        Args:
            capability: Capability to search for
            exclude: Optional list of agent IDs to exclude

        Returns:
            List of matching agents
        """
        exclude = exclude or []
        matching = []

        for agent_id, agent in self._agents.items():
            if agent_id in exclude:
                continue

            if capability in agent.capabilities:
                matching.append(agent)

        return matching

    def list_agents(self) -> list[A2AAgent]:
        """
        List all registered agents.

        Returns:
            List of all registered agents
        """
        return list(self._agents.values())

    def has_agent(self, agent_id: str) -> bool:
        """
        Check if an agent is registered.

        Args:
            agent_id: Agent ID to check

        Returns:
            True if agent is registered, False otherwise
        """
        return agent_id in self._agents

    def get_agent(self, agent_id: str) -> A2AAgent:
        """
        Get an agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent instance

        Raises:
            AgentNotFoundError: If agent is not registered
        """
        if agent_id not in self._agents:
            raise AgentNotFoundError(f"Agent '{agent_id}' is not registered")

        return self._agents[agent_id]

    def get_history(self, limit: Optional[int] = None) -> list[A2AMessage]:
        """
        Get message history.

        Args:
            limit: Optional limit on number of messages to return

        Returns:
            List of recent messages (newest first)
        """
        history = list(reversed(self._message_history))
        if limit:
            return history[:limit]
        return history

    def clear_history(self) -> None:
        """Clear message history."""
        self._message_history.clear()

    def count_agents(self) -> int:
        """Return the number of registered agents."""
        return len(self._agents)

    def clear(self) -> None:
        """Clear all agents and message history."""
        self._agents.clear()
        self._message_history.clear()

    def _add_to_history(self, message: A2AMessage) -> None:
        """Add message to history, maintaining max size."""
        self._message_history.append(message)

        # Trim history if needed
        if len(self._message_history) > self._max_history:
            self._message_history = self._message_history[-self._max_history :]
