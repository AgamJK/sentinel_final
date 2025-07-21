import { useState, useEffect } from "react";
import {
  ReactFlow,
  Background,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    data: { label: '📧 Email Support' },
    position: { x: 50, y: 50 },
    style: { 
      background: 'hsl(195 100% 42%)', 
      color: 'white', 
      border: '2px solid hsl(195 100% 50%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(195 100% 42% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '2', 
    type: 'input',
    data: { label: '💬 Chat Messages' },
    position: { x: 50, y: 150 },
    style: { 
      background: 'hsl(195 100% 42%)', 
      color: 'white', 
      border: '2px solid hsl(195 100% 50%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(195 100% 42% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '3',
    type: 'input', 
    data: { label: '🎫 Support Tickets' },
    position: { x: 50, y: 250 },
    style: { 
      background: 'hsl(195 100% 42%)', 
      color: 'white', 
      border: '2px solid hsl(195 100% 50%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(195 100% 42% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '4',
    data: { label: '🧠 AI Sentiment Analysis' },
    position: { x: 300, y: 150 },
    style: { 
      background: 'hsl(258 100% 55%)', 
      color: 'white', 
      border: '2px solid hsl(258 100% 65%)',
      borderRadius: '16px',
      padding: '16px 28px',
      fontSize: '15px',
      fontWeight: '700',
      boxShadow: '0 6px 20px hsl(258 100% 55% / 0.4)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '5',
    data: { label: '😊 Positive Emotions' },
    position: { x: 550, y: 50 },
    style: { 
      background: 'hsl(120 60% 45%)', 
      color: 'white', 
      border: '2px solid hsl(120 60% 55%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(120 60% 45% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '6',
    data: { label: '😡 Negative Emotions' },
    position: { x: 550, y: 150 },
    style: { 
      background: 'hsl(0 70% 50%)', 
      color: 'white', 
      border: '2px solid hsl(0 70% 60%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(0 70% 50% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '7',
    data: { label: '😐 Neutral Emotions' },
    position: { x: 550, y: 250 },
    style: { 
      background: 'hsl(45 30% 45%)', 
      color: 'white', 
      border: '2px solid hsl(45 30% 55%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(45 30% 45% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '8',
    type: 'output',
    data: { label: '🚨 Alert System' },
    position: { x: 800, y: 100 },
    style: { 
      background: 'hsl(0 70% 50%)', 
      color: 'white', 
      border: '2px solid hsl(0 70% 60%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(0 70% 50% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
  {
    id: '9',
    type: 'output',
    data: { label: '📊 Dashboard' },
    position: { x: 800, y: 200 },
    style: { 
      background: 'hsl(210 20% 35%)', 
      color: 'white', 
      border: '2px solid hsl(210 20% 45%)',
      borderRadius: '12px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 12px hsl(210 20% 35% / 0.3)'
    },
    draggable: false,
    selectable: false,
  },
];

const AnimatedFlow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [animationStep, setAnimationStep] = useState(0);

  // Animated edges that appear in sequence
  const edgeSequence = [
    { id: 'e1-4', source: '1', target: '4', animated: true, style: { stroke: 'hsl(195 100% 50%)', strokeWidth: 3 } },
    { id: 'e2-4', source: '2', target: '4', animated: true, style: { stroke: 'hsl(195 100% 50%)', strokeWidth: 3 } },
    { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: 'hsl(195 100% 50%)', strokeWidth: 3 } },
    { id: 'e4-5', source: '4', target: '5', style: { stroke: 'hsl(120 60% 55%)', strokeWidth: 3 } },
    { id: 'e4-6', source: '4', target: '6', animated: true, style: { stroke: 'hsl(0 70% 60%)', strokeWidth: 4 } },
    { id: 'e4-7', source: '4', target: '7', style: { stroke: 'hsl(45 30% 55%)', strokeWidth: 3 } },
    { id: 'e6-8', source: '6', target: '8', animated: true, style: { stroke: 'hsl(0 70% 60%)', strokeWidth: 4, strokeDasharray: '8,8' } },
    { id: 'e5-9', source: '5', target: '9', style: { stroke: 'hsl(120 60% 55%)', strokeWidth: 3 } },
    { id: 'e6-9', source: '6', target: '9', style: { stroke: 'hsl(0 70% 60%)', strokeWidth: 3 } },
    { id: 'e7-9', source: '7', target: '9', style: { stroke: 'hsl(45 30% 55%)', strokeWidth: 3 } },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationStep(prev => {
        const nextStep = (prev + 1) % (edgeSequence.length + 2);
        
        if (nextStep === 0) {
          // Reset - show all edges
          setEdges(edgeSequence);
        } else if (nextStep <= edgeSequence.length) {
          // Show edges progressively
          setEdges(edgeSequence.slice(0, nextStep));
        } else {
          // Brief pause with all edges visible
          setEdges(edgeSequence);
        }
        
        return nextStep;
      });
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-96 bg-gradient-to-br from-background to-muted/10 rounded-lg overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        panOnDrag={false}
        zoomOnScroll={false}
        zoomOnPinch={false}
        zoomOnDoubleClick={false}
        fitView
        style={{ backgroundColor: "transparent" }}
        proOptions={{ hideAttribution: true }}
      >
      </ReactFlow>
      
      {/* Status indicator */}
      <div className="absolute bottom-4 right-4 flex items-center space-x-2 bg-card/80 backdrop-blur-sm px-3 py-2 rounded-lg border border-border">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span className="text-xs text-muted-foreground">Live Data Flow</span>
      </div>
    </div>
  );
};

export default AnimatedFlow;