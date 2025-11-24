#!/usr/bin/env python3
"""
A2A Exception Classes
======================

Custom exceptions for Agent-to-Agent communication operations.
"""


class A2AError(Exception):
    """Base exception for all A2A-related errors."""

    pass


class AgentNotFoundError(A2AError):
    """Raised when attempting to communicate with an unregistered agent."""

    pass


class MessageDeliveryError(A2AError):
    """Raised when message delivery fails."""

    pass


class AgentRegistrationError(A2AError):
    """Raised when agent registration fails."""

    pass


class InvalidMessageError(A2AError):
    """Raised when message format is invalid."""

    pass
