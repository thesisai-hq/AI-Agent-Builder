"""
Agent Orchestration System
Coordinates multiple agents with communication, memory, and advanced consensus
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# AGENT COMMUNICATION
# ============================================================================


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AgentMessage:
    """Message passed between agents"""

    sender: str
    receiver: Optional[str]  # None = broadcast
    content: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MessageBus:
    """
    Message passing system for agent communication

    Usage:
        bus = MessageBus()
        bus.subscribe("risk_agent", callback_function)
        bus.publish(AgentMessage(sender="fundamental_agent", ...))
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._history: List[AgentMessage] = []

    def subscribe(self, agent_id: str, callback: Callable):
        """Subscribe agent to messages"""
        if agent_id not in self._subscribers:
            self._subscribers[agent_id] = []
        self._subscribers[agent_id].append(callback)

    def publish(self, message: AgentMessage):
        """Publish message to subscribers"""
        self._history.append(message)

        # Broadcast or targeted
        if message.receiver:
            # Send to specific agent
            if message.receiver in self._subscribers:
                for callback in self._subscribers[message.receiver]:
                    callback(message)
        else:
            # Broadcast to all except sender
            for agent_id, callbacks in self._subscribers.items():
                if agent_id != message.sender:
                    for callback in callbacks:
                        callback(message)

    def get_history(self, agent_id: Optional[str] = None) -> List[AgentMessage]:
        """Get message history"""
        if agent_id:
            return [
                m
                for m in self._history
                if m.sender == agent_id or m.receiver == agent_id
            ]
        return self._history


# ============================================================================
# AGENT MEMORY
# ============================================================================


@dataclass
class AgentMemory:
    """
    Memory system for agents to learn from past analyses

    Stores:
    - Past signals and outcomes
    - Performance metrics
    - Learned patterns
    """

    agent_id: str
    signals: List[Dict[str, Any]] = field(default_factory=list)
    accuracy_history: List[float] = field(default_factory=list)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)

    def remember(
        self,
        ticker: str,
        signal: str,
        confidence: float,
        reasoning: str,
        metadata: Optional[Dict] = None,
    ):
        """Store a signal in memory"""
        self.signals.append(
            {
                "ticker": ticker,
                "signal": signal,
                "confidence": confidence,
                "reasoning": reasoning,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            }
        )

    def recall(self, ticker: str, limit: int = 10) -> List[Dict]:
        """Recall past signals for ticker"""
        return [s for s in self.signals if s["ticker"] == ticker][-limit:]

    def update_accuracy(self, accuracy: float):
        """Update performance tracking"""
        self.accuracy_history.append(accuracy)

    def get_avg_accuracy(self, window: int = 10) -> float:
        """Get recent average accuracy"""
        if not self.accuracy_history:
            return 0.5
        recent = self.accuracy_history[-window:]
        return sum(recent) / len(recent)

    def learn_pattern(self, pattern_name: str, pattern_data: Any):
        """Store learned pattern"""
        self.learned_patterns[pattern_name] = pattern_data


class MemoryManager:
    """Manages memory for all agents"""

    def __init__(self):
        self._memories: Dict[str, AgentMemory] = {}

    def get_memory(self, agent_id: str) -> AgentMemory:
        """Get or create memory for agent"""
        if agent_id not in self._memories:
            self._memories[agent_id] = AgentMemory(agent_id)
        return self._memories[agent_id]

    def get_all_memories(self) -> Dict[str, AgentMemory]:
        """Get all agent memories"""
        return self._memories


# ============================================================================
# AGENT ORCHESTRATOR
# ============================================================================


class AgentOrchestrator:
    """
    Advanced orchestration with:
    - Sequential execution (agents run in order)
    - Parallel execution (agents run simultaneously)
    - Hierarchical execution (supervisor → workers)
    - Debate/refinement phases
    - Adaptive consensus
    """

    def __init__(self, registry, db):
        self.registry = registry
        self.db = db
        self.message_bus = MessageBus()
        self.memory_manager = MemoryManager()

    # ========================================================================
    # EXECUTION MODES
    # ========================================================================

    def execute_sequential(self, ticker: str, context, agent_ids: List[str]) -> Dict:
        """
        Sequential execution - Each agent sees previous agents' outputs

        Use case: Pipeline where later agents refine earlier analysis
        Example: Fundamental → Technical → Risk → Final
        """
        signals = []
        previous_signals = []

        for agent_id in agent_ids:
            agent = self.registry.get(agent_id)
            if not agent:
                continue

            try:
                # Agent can access previous signals via context
                context.previous_signals = previous_signals

                signal = agent.analyze(ticker, context)
                signal_dict = signal.to_dict()
                signals.append(signal_dict)
                previous_signals.append(signal_dict)

                # Store in memory
                memory = self.memory_manager.get_memory(agent_id)
                memory.remember(
                    ticker, signal.signal_type, signal.confidence, signal.reasoning
                )

                logger.info(
                    f"✅ {agent.name}: {signal.signal_type} ({signal.confidence:.2f})"
                )

            except Exception as e:
                logger.error(f"❌ {agent.name} failed: {e}")

        return {
            "mode": "sequential",
            "signals": signals,
            "consensus": self.calculate_advanced_consensus(signals),
        }

    def execute_parallel(self, ticker: str, context, agent_ids: List[str]) -> Dict:
        """
        Parallel execution - Agents run independently

        Use case: Diverse perspectives, no dependencies
        Example: Multiple analysts giving independent opinions
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        signals = []

        # Check if we have agents
        if not agent_ids:
            return {
                "mode": "parallel",
                "signals": [],
                "consensus": {"signal": "neutral", "confidence": 0.0},
            }

        def run_agent(agent_id):
            agent = self.registry.get(agent_id)
            if not agent:
                return None

            try:
                signal = agent.analyze(ticker, context)

                # Store in memory
                memory = self.memory_manager.get_memory(agent_id)
                memory.remember(
                    ticker, signal.signal_type, signal.confidence, signal.reasoning
                )

                return signal.to_dict()
            except Exception as e:
                logger.error(
                    f"❌ {agent.name if hasattr(agent, 'name') else agent_id} failed: {e}"
                )
                return None

        # Run in parallel
        max_workers = min(len(agent_ids), 10)  # Cap at 10 workers
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(run_agent, aid): aid for aid in agent_ids}

            for future in as_completed(futures):
                result = future.result()
                if result:
                    signals.append(result)

        return {
            "mode": "parallel",
            "signals": signals,
            "consensus": self.calculate_advanced_consensus(signals),
        }

    def execute_hierarchical(
        self, ticker: str, context, supervisor_id: str, worker_ids: List[str]
    ) -> Dict:
        """
        Hierarchical execution - Supervisor coordinates workers

        Use case: Complex analysis with specialized agents
        Example: Lead analyst → [Fundamental, Technical, Sentiment] workers
        """
        # Phase 1: Workers analyze
        worker_signals = []
        for worker_id in worker_ids:
            agent = self.registry.get(worker_id)
            if agent:
                try:
                    signal = agent.analyze(ticker, context)
                    worker_signals.append(signal.to_dict())
                except Exception as e:
                    logger.error(f"Worker {agent.name} failed: {e}")

        # Phase 2: Supervisor reviews and makes final call
        supervisor = self.registry.get(supervisor_id)
        if supervisor:
            try:
                # Pass worker signals to supervisor
                context.worker_signals = worker_signals
                supervisor_signal = supervisor.analyze(ticker, context)

                return {
                    "mode": "hierarchical",
                    "supervisor": supervisor_signal.to_dict(),
                    "workers": worker_signals,
                    "final_signal": supervisor_signal.to_dict(),
                }
            except Exception as e:
                logger.error(f"Supervisor failed: {e}")

        # Fallback to consensus
        return {
            "mode": "hierarchical",
            "workers": worker_signals,
            "consensus": self.calculate_advanced_consensus(worker_signals),
        }

    def execute_debate(
        self, ticker: str, context, agent_ids: List[str], rounds: int = 2
    ) -> Dict:
        """
        Debate mode - Agents refine opinions through multiple rounds

        Use case: Critical decisions requiring deliberation
        Example: Investment committee debate
        """
        all_rounds = []

        for round_num in range(rounds):
            logger.info(f"🗣️ Debate Round {round_num + 1}/{rounds}")

            round_signals = []

            for agent_id in agent_ids:
                agent = self.registry.get(agent_id)
                if not agent:
                    continue

                try:
                    # Agents see previous round results
                    if all_rounds:
                        context.previous_round = all_rounds[-1]

                    signal = agent.analyze(ticker, context)
                    round_signals.append(signal.to_dict())

                    # Broadcast signal to other agents
                    message = AgentMessage(
                        sender=agent_id,
                        receiver=None,  # Broadcast
                        content={
                            "signal": signal.signal_type,
                            "confidence": signal.confidence,
                            "reasoning": signal.reasoning,
                        },
                        priority=MessagePriority.NORMAL,
                    )
                    self.message_bus.publish(message)

                except Exception as e:
                    logger.error(f"Agent {agent_id} failed in debate: {e}")

            all_rounds.append(round_signals)

        # Final consensus from last round
        final_signals = all_rounds[-1] if all_rounds else []

        return {
            "mode": "debate",
            "rounds": all_rounds,
            "final_signals": final_signals,
            "consensus": self.calculate_advanced_consensus(final_signals),
        }

    # ========================================================================
    # ADVANCED CONSENSUS
    # ========================================================================

    def calculate_advanced_consensus(self, signals: List[Dict]) -> Dict:
        """
        Advanced consensus with:
        - Weighted voting (by agent weight and confidence)
        - Confidence-adjusted signals
        - Dissent tracking
        - Uncertainty quantification
        """
        if not signals:
            return {
                "signal": "neutral",
                "confidence": 0.0,
                "agreement": 0.0,
                "method": "none",
            }

        # Get agent weights
        weighted_votes = {}
        total_weight = 0
        total_weighted_confidence = 0

        for s in signals:
            agent_id = s.get("agent_name", "unknown")
            meta = self.registry.get_metadata(agent_id.lower().replace(" ", "_"))
            weight = meta.weight if meta else 1.0

            signal_type = s["signal_type"]
            confidence = s["confidence"]

            # Weighted vote
            weighted_vote = weight * confidence
            weighted_votes[signal_type] = (
                weighted_votes.get(signal_type, 0) + weighted_vote
            )
            total_weight += weight
            total_weighted_confidence += weight * confidence

        # Determine winner
        if weighted_votes:
            winner = max(weighted_votes.items(), key=lambda x: x[1])
            signal = winner[0]
            signal_weight = winner[1]
        else:
            signal = "neutral"
            signal_weight = 0

        # Calculate metrics
        avg_confidence = (
            total_weighted_confidence / total_weight if total_weight > 0 else 0
        )
        agreement = (
            signal_weight / sum(weighted_votes.values()) if weighted_votes else 0
        )

        # Detect strong dissent
        dissent = []
        for s in signals:
            if s["signal_type"] != signal and s["confidence"] > 0.7:
                dissent.append(
                    {
                        "agent": s["agent_name"],
                        "signal": s["signal_type"],
                        "confidence": s["confidence"],
                    }
                )

        return {
            "signal": signal,
            "confidence": round(avg_confidence, 3),
            "agreement": round(agreement, 3),
            "distribution": weighted_votes,
            "dissent": dissent,
            "method": "weighted_confidence",
            "uncertainty": round(1 - agreement, 3),
        }

    # ========================================================================
    # ADAPTIVE EXECUTION
    # ========================================================================

    def execute_adaptive(self, ticker: str, context, agent_ids: List[str]) -> Dict:
        """
        Adaptive execution - Choose best strategy based on situation

        Logic:
        - High volatility → Use parallel (diverse opinions)
        - Strong trend → Use sequential (build on analysis)
        - Unclear market → Use debate (thorough deliberation)
        """
        # Analyze market conditions
        volatility = self._calculate_volatility(ticker, context)
        trend_strength = self._calculate_trend_strength(ticker, context)

        if volatility > 0.5:
            logger.info("📊 High volatility → Parallel execution")
            return self.execute_parallel(ticker, context, agent_ids)
        elif trend_strength > 0.7:
            logger.info("📈 Strong trend → Sequential execution")
            return self.execute_sequential(ticker, context, agent_ids)
        else:
            logger.info("🤔 Unclear market → Debate mode")
            return self.execute_debate(ticker, context, agent_ids, rounds=2)

    def _calculate_volatility(self, ticker: str, context) -> float:
        """Calculate recent volatility"""
        try:
            prices = context.get_price_data(days=30)
            if not prices or len(prices) < 2:
                return 0.5

            returns = []
            for i in range(len(prices) - 1):
                r = (prices[i]["close"] - prices[i + 1]["close"]) / prices[i + 1][
                    "close"
                ]
                returns.append(abs(r))

            return min(1.0, sum(returns) / len(returns) * 10) if returns else 0.5
        except:
            return 0.5

    def _calculate_trend_strength(self, ticker: str, context) -> float:
        """Calculate trend strength"""
        try:
            prices = context.get_price_data(days=20)
            if not prices or len(prices) < 2:
                return 0.5

            latest = prices[0]
            current = latest["close"]
            sma_20 = latest.get("sma_20", current)

            # Distance from SMA as trend strength
            diff = abs(current - sma_20) / sma_20
            return min(1.0, diff * 10)
        except:
            return 0.5


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of orchestrator
    """
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext
    from agent_builder.agents.registry import get_registry

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)
    registry = get_registry()

    # Create orchestrator
    orchestrator = AgentOrchestrator(registry, db)

    # Test ticker
    ticker = "AAPL"
    context = AgentContext(ticker, db)
    agent_ids = registry.list_enabled()

    print("\n" + "=" * 70)
    print("TESTING ORCHESTRATION MODES")
    print("=" * 70)

    # Test 1: Sequential
    print("\n1️⃣ Sequential Execution:")
    result = orchestrator.execute_sequential(ticker, context, agent_ids)
    print(f"   Signal: {result['consensus']['signal']}")
    print(f"   Confidence: {result['consensus']['confidence']:.2f}")

    # Test 2: Parallel
    print("\n2️⃣ Parallel Execution:")
    result = orchestrator.execute_parallel(ticker, context, agent_ids)
    print(f"   Signal: {result['consensus']['signal']}")
    print(f"   Confidence: {result['consensus']['confidence']:.2f}")

    # Test 3: Debate
    print("\n3️⃣ Debate Mode (2 rounds):")
    result = orchestrator.execute_debate(ticker, context, agent_ids, rounds=2)
    print(f"   Signal: {result['consensus']['signal']}")
    print(f"   Confidence: {result['consensus']['confidence']:.2f}")
    print(f"   Agreement: {result['consensus']['agreement']:.2f}")

    # Test 4: Adaptive
    print("\n4️⃣ Adaptive Execution:")
    result = orchestrator.execute_adaptive(ticker, context, agent_ids)
    print(f"   Mode: {result['mode']}")
    print(f"   Signal: {result['consensus']['signal']}")
    print(f"   Confidence: {result['consensus']['confidence']:.2f}")

    pool.close()
    print("\n" + "=" * 70)
    print("✅ Orchestration tests complete")
    print("=" * 70 + "\n")
