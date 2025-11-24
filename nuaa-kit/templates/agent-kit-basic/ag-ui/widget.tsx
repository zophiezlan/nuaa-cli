/**
 * AG-UI Widget Template for {{PROJECT_NAME}}
 *
 * This is a basic agentic UI widget that can respond to agent events
 * and update its state dynamically.
 */

import React, { useState, useEffect } from 'react';

interface AgentEvent {
  type: string;
  payload: any;
  timestamp: string;
}

interface WidgetProps {
  agentId?: string;
  onAction?: (action: string, params: any) => void;
}

export const NUAAWidget: React.FC<WidgetProps> = ({
  agentId = 'nuaa-agent',
  onAction
}) => {
  const [status, setStatus] = useState<string>('idle');
  const [events, setEvents] = useState<AgentEvent[]>([]);

  useEffect(() => {
    // Subscribe to agent events
    const handleAgentEvent = (event: AgentEvent) => {
      setEvents(prev => [...prev, event]);

      // Update status based on event type
      switch(event.type) {
        case 'program_design_started':
          setStatus('Designing program...');
          break;
        case 'proposal_generated':
          setStatus('Proposal ready');
          break;
        default:
          setStatus('idle');
      }
    };

    // Setup event listener (pseudo-code, depends on your framework)
    // agentEventBus.subscribe(agentId, handleAgentEvent);

    return () => {
      // Cleanup
      // agentEventBus.unsubscribe(agentId, handleAgentEvent);
    };
  }, [agentId]);

  const handleDesignProgram = () => {
    onAction?.('design_program', {
      program_name: 'New Program',
      target_population: 'Target audience',
      duration: '6 months'
    });
  };

  const handleCreateProposal = () => {
    onAction?.('create_proposal', {
      program_name: 'Program Name',
      funder: 'Funder Name',
      amount: '$50000'
    });
  };

  return (
    <div className="nuaa-widget">
      <div className="widget-header">
        <h3>NUAA Project Assistant</h3>
        <span className="status">{status}</span>
      </div>

      <div className="widget-actions">
        <button onClick={handleDesignProgram}>
          Design Program
        </button>
        <button onClick={handleCreateProposal}>
          Create Proposal
        </button>
      </div>

      <div className="widget-events">
        <h4>Recent Events</h4>
        <ul>
          {events.slice(-5).map((event, idx) => (
            <li key={idx}>
              <span className="event-type">{event.type}</span>
              <span className="event-time">
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default NUAAWidget;
