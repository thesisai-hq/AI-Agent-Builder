"""Pydantic models for GUI system API."""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# Agent Type
AgentTypeEnum = Literal["rule_based", "llm_based"]
SignalDirection = Literal["bullish", "bearish", "neutral"]


# Rule condition types
ConditionType = Literal["simple", "formula"]


# Simple condition (existing)
class RuleCondition(BaseModel):
    """Single condition in a rule."""
    type: ConditionType = Field(default="simple", description="Condition type")
    indicator: Optional[str] = Field(None, description="Indicator name (e.g., 'pe_ratio')")
    operator: Optional[str] = Field(None, description="Comparison operator (<, >, =, <=, >=)")
    value: Optional[float] = Field(None, description="Threshold value")
    
    # Formula-based condition (NEW)
    formula: Optional[str] = Field(None, description="Mathematical formula (e.g., 'PE_RATIO / GROWTH_RATE')")
    variables: Optional[Dict[str, str]] = Field(None, description="Variable mappings (e.g., {'PE_RATIO': 'pe_ratio'})")
    formula_operator: Optional[str] = Field(None, description="Operator for formula result")
    formula_threshold: Optional[float] = Field(None, description="Threshold for formula result")
    formula_description: Optional[str] = Field(None, description="Human-readable formula description")


class RuleAction(BaseModel):
    """Action to take when rule fires."""
    action: str = Field(..., description="Action type (buy, sell, hold)")
    size: float = Field(..., description="Position size as percentage (0-100)")
    parameters: Dict[str, Any] = Field(default_factory=dict)


class Rule(BaseModel):
    """Complete trading rule."""
    id: Optional[str] = None
    conditions: List[RuleCondition] = Field(default_factory=list)
    action: RuleAction
    description: Optional[str] = None


# LLM Configuration
class LLMConfigModel(BaseModel):
    """LLM configuration for AI-powered agents."""
    provider: str = Field(default="openai", description="LLM provider")
    model: str = Field(default="gpt-4", description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, gt=0)
    system_prompt: Optional[str] = None
    tools: List[str] = Field(default_factory=list)


# Agent models
class AgentBase(BaseModel):
    """Base agent fields."""
    name: str = Field(..., min_length=1, max_length=100)
    type: AgentTypeEnum
    description: Optional[str] = None
    goal: str = Field(..., min_length=1)


class AgentCreate(AgentBase):
    """Request to create an agent."""
    template_id: Optional[str] = None
    rules: List[Rule] = Field(default_factory=list)
    llm_config: Optional[LLMConfigModel] = None


class AgentUpdate(BaseModel):
    """Request to update an agent."""
    name: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    rules: Optional[List[Rule]] = None
    llm_config: Optional[LLMConfigModel] = None


class AgentResponse(AgentBase):
    """Agent response with metadata."""
    id: str
    template_id: Optional[str] = None
    rules: List[Rule] = Field(default_factory=list)
    llm_config: Optional[LLMConfigModel] = None
    created_at: datetime
    updated_at: datetime


class AgentListResponse(BaseModel):
    """List of agents."""
    agents: List[AgentResponse]
    total: int


# Template models
class TemplateResponse(BaseModel):
    """Pre-built agent template."""
    id: str
    name: str
    description: str
    type: AgentTypeEnum
    icon: str = Field(default="chart")
    color: str = Field(default="#3B82F6")
    goal: str
    rules: List[Rule] = Field(default_factory=list)
    llm_config: Optional[LLMConfigModel] = None
    category: str = Field(default="general")


class TemplateListResponse(BaseModel):
    """List of templates."""
    templates: List[TemplateResponse]
    total: int


# Analysis models
class AnalysisRequest(BaseModel):
    """Request to analyze a stock."""
    ticker: str = Field(..., min_length=1, max_length=10)
    agent_id: str


class AnalysisResponse(BaseModel):
    """Analysis result from an agent."""
    ticker: str
    agent_id: str
    agent_name: str
    direction: SignalDirection
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    timestamp: datetime


# Formula validation
class FormulaValidateRequest(BaseModel):
    """Request to validate a formula."""
    formula: str
    variables: Dict[str, str] = Field(default_factory=dict)
    sample_data: Optional[Dict[str, float]] = None


class FormulaValidateResponse(BaseModel):
    """Formula validation result."""
    valid: bool
    result: Optional[float] = None
    error: Optional[str] = None
    parsed_formula: Optional[str] = None


# Export models
class ExportCodeResponse(BaseModel):
    """Python code export."""
    code: str
    filename: str


# Health check
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime
