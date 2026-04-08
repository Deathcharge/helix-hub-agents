"""
Enhanced Agent Communication Module
====================================

Advanced messaging, routing, and coordination protocols for agent communication.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set
from enum import Enum
from datetime import datetime
import asyncio
import uuid


class MessageType(str, Enum):
    """Types of messages agents can send"""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    CONSENSUS = "consensus"
    HEARTBEAT = "heartbeat"
    ERROR = "error"
    NOTIFICATION = "notification"
    COMMAND = "command"


class MessagePriority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Message:
    """Agent communication message"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_ids: List[str] = field(default_factory=list)
    message_type: MessageType = MessageType.REQUEST
    priority: MessagePriority = MessagePriority.NORMAL
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    timeout: int = 30  # seconds
    retry_count: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed > self.timeout


@dataclass
class MessageResponse:
    """Response to a message"""
    message_id: str
    responder_id: str
    status: str  # "success", "failure", "timeout"
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class MessageRouter:
    """Routes messages between agents"""
    
    def __init__(self):
        """Initialize message router"""
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.agent_routes: Dict[str, List[str]] = {}
        self.message_history: List[Message] = []
        self.max_history_size = 10000
    
    async def route_message(self, message: Message) -> None:
        """Route a message to its recipients"""
        await self.message_queue.put(message)
        self.message_history.append(message)
        
        # Maintain history size
        if len(self.message_history) > self.max_history_size:
            self.message_history = self.message_history[-self.max_history_size:]
    
    async def get_message(self, timeout: int = 5) -> Optional[Message]:
        """Get next message from queue"""
        try:
            message = await asyncio.wait_for(
                self.message_queue.get(),
                timeout=timeout
            )
            return message
        except asyncio.TimeoutError:
            return None
    
    def register_route(self, agent_id: str, target_agents: List[str]) -> None:
        """Register routing for an agent"""
        self.agent_routes[agent_id] = target_agents
    
    def get_routes_for_agent(self, agent_id: str) -> List[str]:
        """Get routing targets for an agent"""
        return self.agent_routes.get(agent_id, [])
    
    def get_message_history(
        self,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        message_type: Optional[MessageType] = None,
        limit: int = 100
    ) -> List[Message]:
        """Get message history with optional filters"""
        filtered = self.message_history
        
        if sender_id:
            filtered = [m for m in filtered if m.sender_id == sender_id]
        
        if recipient_id:
            filtered = [m for m in filtered if recipient_id in m.recipient_ids]
        
        if message_type:
            filtered = [m for m in filtered if m.message_type == message_type]
        
        return filtered[-limit:]


class ConsensusProtocol:
    """Protocol for reaching consensus among agents"""
    
    def __init__(self, timeout: int = 30):
        """Initialize consensus protocol"""
        self.timeout = timeout
        self.votes: Dict[str, Dict[str, Any]] = {}
        self.consensus_threshold = 0.8
    
    async def initiate_consensus(
        self,
        proposer_id: str,
        participants: List[str],
        proposal: Dict[str, Any],
        router: MessageRouter
    ) -> Dict[str, Any]:
        """Initiate a consensus round"""
        consensus_id = str(uuid.uuid4())
        
        # Send proposal to all participants
        proposal_message = Message(
            sender_id=proposer_id,
            recipient_ids=participants,
            message_type=MessageType.CONSENSUS,
            content={
                "consensus_id": consensus_id,
                "proposal": proposal,
                "action": "vote"
            }
        )
        
        await router.route_message(proposal_message)
        
        # Collect votes
        votes = {}
        start_time = datetime.now()
        
        while len(votes) < len(participants):
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > self.timeout:
                break
            
            # In real implementation, would receive vote messages
            await asyncio.sleep(0.1)
        
        # Calculate consensus
        agreement_count = sum(1 for v in votes.values() if v.get("agree", False))
        agreement_ratio = agreement_count / len(participants) if participants else 0
        
        return {
            "consensus_id": consensus_id,
            "consensus_reached": agreement_ratio >= self.consensus_threshold,
            "agreement_ratio": agreement_ratio,
            "votes": votes,
            "participants": len(participants),
            "agreements": agreement_count,
        }
    
    def add_vote(self, voter_id: str, vote: Dict[str, Any]) -> None:
        """Add a vote to the consensus"""
        self.votes[voter_id] = vote


class ConflictResolution:
    """Handles conflicts between agents"""
    
    @staticmethod
    async def resolve_conflict(
        agent_ids: List[str],
        conflict_data: Dict[str, Any],
        mediator_id: str,
        router: MessageRouter
    ) -> Dict[str, Any]:
        """Resolve a conflict between agents"""
        resolution_id = str(uuid.uuid4())
        
        # Request positions from all agents
        position_message = Message(
            sender_id=mediator_id,
            recipient_ids=agent_ids,
            message_type=MessageType.REQUEST,
            content={
                "resolution_id": resolution_id,
                "conflict_data": conflict_data,
                "action": "provide_position"
            }
        )
        
        await router.route_message(position_message)
        
        # Collect positions
        positions = {}
        for agent_id in agent_ids:
            # In real implementation, would receive position responses
            positions[agent_id] = {"position": "neutral"}
        
        # Analyze positions and find resolution
        resolution = ConflictResolution._analyze_positions(positions)
        
        # Broadcast resolution
        resolution_message = Message(
            sender_id=mediator_id,
            recipient_ids=agent_ids,
            message_type=MessageType.NOTIFICATION,
            content={
                "resolution_id": resolution_id,
                "resolution": resolution,
                "action": "accept_resolution"
            }
        )
        
        await router.route_message(resolution_message)
        
        return {
            "resolution_id": resolution_id,
            "resolution": resolution,
            "positions": positions,
        }
    
    @staticmethod
    def _analyze_positions(positions: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze agent positions and find resolution"""
        # Simple majority-based resolution
        return {
            "strategy": "majority",
            "recommended_action": "proceed_with_consensus",
            "confidence": 0.85,
        }


class CommunicationMiddleware:
    """Middleware for agent communication"""
    
    def __init__(self):
        """Initialize middleware"""
        self.interceptors: List[Callable] = []
        self.rate_limiters: Dict[str, int] = {}
        self.message_filters: List[Callable] = []
    
    def add_interceptor(self, interceptor: Callable) -> None:
        """Add a message interceptor"""
        self.interceptors.append(interceptor)
    
    def add_message_filter(self, filter_func: Callable) -> None:
        """Add a message filter"""
        self.message_filters.append(filter_func)
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process a message through middleware"""
        # Check filters
        for filter_func in self.message_filters:
            if not filter_func(message):
                return None
        
        # Check rate limiting
        if self._is_rate_limited(message.sender_id):
            return None
        
        # Run interceptors
        for interceptor in self.interceptors:
            message = await interceptor(message)
            if message is None:
                return None
        
        return message
    
    def _is_rate_limited(self, agent_id: str) -> bool:
        """Check if agent is rate limited"""
        limit = self.rate_limiters.get(agent_id, 0)
        return limit > 100  # Simple threshold
    
    def set_rate_limit(self, agent_id: str, limit: int) -> None:
        """Set rate limit for an agent"""
        self.rate_limiters[agent_id] = limit


class MessageQueue:
    """Priority-based message queue"""
    
    def __init__(self):
        """Initialize message queue"""
        self.queues: Dict[MessagePriority, asyncio.Queue] = {
            priority: asyncio.Queue() for priority in MessagePriority
        }
        self.priority_order = [
            MessagePriority.CRITICAL,
            MessagePriority.HIGH,
            MessagePriority.NORMAL,
            MessagePriority.LOW,
        ]
    
    async def put(self, message: Message) -> None:
        """Add message to queue"""
        await self.queues[message.priority].put(message)
    
    async def get(self, timeout: int = 5) -> Optional[Message]:
        """Get next message from queue (respecting priority)"""
        for priority in self.priority_order:
            try:
                message = self.queues[priority].get_nowait()
                return message
            except asyncio.QueueEmpty:
                continue
        
        # If no messages in any queue, wait for any
        try:
            for priority in self.priority_order:
                return await asyncio.wait_for(
                    self.queues[priority].get(),
                    timeout=timeout / len(self.priority_order)
                )
        except asyncio.TimeoutError:
            return None
    
    def size(self) -> int:
        """Get total queue size"""
        return sum(q.qsize() for q in self.queues.values())


class AgentCommunicationHub:
    """Central hub for agent communication"""
    
    def __init__(self):
        """Initialize communication hub"""
        self.router = MessageRouter()
        self.consensus = ConsensusProtocol()
        self.middleware = CommunicationMiddleware()
        self.message_queue = MessageQueue()
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
    
    async def send_message(self, message: Message) -> bool:
        """Send a message through the hub"""
        # Process through middleware
        processed_message = await self.middleware.process_message(message)
        if processed_message is None:
            return False
        
        # Route message
        await self.router.route_message(processed_message)
        
        # Add to priority queue
        await self.message_queue.put(processed_message)
        
        return True
    
    async def receive_message(self, timeout: int = 5) -> Optional[Message]:
        """Receive next message from hub"""
        return await self.message_queue.get(timeout)
    
    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> None:
        """Register an agent with the hub"""
        self.agent_registry[agent_id] = agent_info
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an agent"""
        return self.agent_registry.get(agent_id)
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agent_registry.keys())
