/**
 * API client for AI Agent Builder backend
 */

const API_BASE = 'http://localhost:8000/api';

// Type definitions
export type AgentType = 'rule_based' | 'llm_based';
export type SignalDirection = 'bullish' | 'bearish' | 'neutral';
export type ConditionType = 'simple' | 'formula';

export interface RuleCondition {
	type: ConditionType;
	indicator?: string;
	operator?: string;
	value?: number;
	formula?: string;
	variables?: Record<string, string>;
	formula_operator?: string;
	formula_threshold?: number;
	formula_description?: string;
}

export interface RuleAction {
	action: SignalDirection;
	size: number;
	parameters: Record<string, any>;
}

export interface Rule {
	id?: string;
	conditions: RuleCondition[];
	action: RuleAction;
	description?: string;
}

export interface LLMConfig {
	provider: string;
	model: string;
	temperature: number;
	max_tokens: number;
	system_prompt?: string;
	tools: string[];
	ollama_base_url?: string;  // For local Ollama
}

export interface Agent {
	id: string;
	name: string;
	type: AgentType;
	description?: string;
	goal: string;
	template_id?: string;
	rules: Rule[];
	llm_config?: LLMConfig;
	created_at: string;
	updated_at: string;
}

export interface AgentCreate {
	name: string;
	type: AgentType;
	description?: string;
	goal: string;
	template_id?: string;
	rules: Rule[];
	llm_config?: LLMConfig;
}

export interface AgentUpdate {
	name?: string;
	description?: string;
	goal?: string;
	rules?: Rule[];
	llm_config?: LLMConfig;
}

export interface Template {
	id: string;
	name: string;
	description: string;
	type: AgentType;
	icon: string;
	color: string;
	goal: string;
	rules: Rule[];
	llm_config?: LLMConfig;
	category: string;
}

export interface AnalysisRequest {
	ticker: string;
	agent_id: string;
}

export interface AnalysisResponse {
	ticker: string;
	agent_id: string;
	agent_name: string;
	direction: SignalDirection;
	confidence: number;
	reasoning: string;
	timestamp: string;
	data_used: Record<string, any>;
	data_quality?: any;
}

export interface Document {
	filename: string;
	size: number;
	size_mb: number;
	modified: string;
}

// API client
class APIClient {
	private baseUrl: string;

	constructor(baseUrl: string = API_BASE) {
		this.baseUrl = baseUrl;
	}

	private async request<T>(
		endpoint: string,
		options: RequestInit = {},
		expectJson: boolean = true
	): Promise<T> {
		const url = `${this.baseUrl}${endpoint}`;
		const response = await fetch(url, {
			...options,
			headers: {
				'Content-Type': 'application/json',
				...options.headers,
			},
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ message: 'Request failed' }));
			throw new Error(error.detail?.message || error.message || 'Request failed');
		}

		// Handle 204 No Content responses
		if (response.status === 204 || !expectJson) {
			return undefined as T;
		}

		return response.json();
	}

	// Agent endpoints
	async createAgent(agent: AgentCreate): Promise<Agent> {
		return this.request<Agent>('/agents', {
			method: 'POST',
			body: JSON.stringify(agent),
		});
	}

	async listAgents(): Promise<{ agents: Agent[]; total: number }> {
		return this.request('/agents');
	}

	async getAgent(id: string): Promise<Agent> {
		return this.request(`/agents/${id}`);
	}

	async updateAgent(id: string, update: AgentUpdate): Promise<Agent> {
		return this.request(`/agents/${id}`, {
			method: 'PATCH',
			body: JSON.stringify(update),
		});
	}

	async deleteAgent(id: string): Promise<void> {
		// 204 No Content - don't expect JSON
		await this.request(`/agents/${id}`, { method: 'DELETE' }, false);
	}

	async exportAgent(id: string): Promise<{ code: string; filename: string }> {
		return this.request(`/agents/${id}/export`);
	}

	// Alias for backward compatibility
	async exportAgentCode(id: string): Promise<{ code: string; filename: string }> {
		return this.exportAgent(id);
	}

	// Template endpoints
	async listTemplates(): Promise<{ templates: Template[]; total: number }> {
		return this.request('/templates');
	}

	async getTemplate(id: string): Promise<Template> {
		return this.request(`/templates/${id}`);
	}

	// Analysis endpoints
	async analyzeStock(request: AnalysisRequest): Promise<AnalysisResponse> {
		return this.request('/analysis', {
			method: 'POST',
			body: JSON.stringify(request),
		});
	}

	// Document endpoints (RAG)
	async uploadDocument(agentId: string, file: File): Promise<any> {
		const formData = new FormData();
		formData.append('file', file);

		const response = await fetch(`${this.baseUrl}/agents/${agentId}/documents`, {
			method: 'POST',
			body: formData,
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ message: 'Upload failed' }));
			throw new Error(error.detail?.message || 'Upload failed');
		}

		return response.json();
	}

	async listDocuments(agentId: string): Promise<{ documents: Document[]; total: number }> {
		return this.request(`/agents/${agentId}/documents`);
	}

	async deleteDocument(agentId: string, filename: string): Promise<void> {
		// 204 No Content - don't expect JSON
		await fetch(`${this.baseUrl}/agents/${agentId}/documents/${filename}`, {
			method: 'DELETE',
		});
	}

	async queryDocuments(agentId: string, query: string, n_results: number = 5): Promise<any> {
		return this.request(`/agents/${agentId}/documents/query`, {
			method: 'POST',
			body: JSON.stringify({ query, n_results }),
		});
	}

	// Formula endpoints
	async validateFormula(formula: string, variables: Record<string, string>, sampleData?: Record<string, number>): Promise<any> {
		return this.request('/formulas/validate', {
			method: 'POST',
			body: JSON.stringify({ formula, variables, sample_data: sampleData }),
		});
	}

	async listFormulaTemplates(): Promise<any> {
		return this.request('/formulas/templates');
	}

	// Cache endpoints
	async getCacheStats(): Promise<any> {
		return this.request('/cache/stats');
	}

	async clearCache(ticker?: string): Promise<any> {
		const url = ticker ? `/cache/clear?ticker=${ticker}` : '/cache/clear';
		return this.request(url, { method: 'POST' });
	}

	// Health check
	async healthCheck(): Promise<any> {
		return this.request('/health');
	}
}

export const api = new APIClient();
