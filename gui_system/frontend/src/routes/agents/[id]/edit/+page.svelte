<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { api, type Agent, type AgentUpdate, type Rule, type LLMConfig } from '$lib/api';
	import RuleBuilder from '$lib/components/RuleBuilder.svelte';
	import LLMConfigComponent from '$lib/components/LLMConfig.svelte';
	
	let agent = $state<Agent | null>(null);
	let isLoading = $state(true);
	let isSaving = $state(false);
	let errorMessage = $state<string | null>(null);
	
	// Form data
	let agentName = $state('');
	let agentGoal = $state('');
	let agentDescription = $state('');
	let rules = $state<Rule[]>([]);
	let llmConfig = $state<LLMConfig>({
		provider: 'openai',
		model: 'gpt-4',
		temperature: 0.7,
		max_tokens: 2000,
		system_prompt: '',
		tools: []
	});
	
	onMount(async () => {
		const agentId = $page.params.id;
		await loadAgent(agentId);
	});
	
	async function loadAgent(agentId: string) {
		try {
			isLoading = true;
			errorMessage = null;
			agent = await api.getAgent(agentId);
			
			// Populate form
			agentName = agent.name;
			agentGoal = agent.goal;
			agentDescription = agent.description || '';
			rules = agent.rules || [];
			if (agent.llm_config) {
				llmConfig = { ...agent.llm_config };
			}
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to load agent';
		} finally {
			isLoading = false;
		}
	}
	
	async function saveAgent() {
		if (!agent) return;
		
		if (!agentName.trim()) {
			errorMessage = 'Agent name is required';
			return;
		}
		
		if (!agentGoal.trim()) {
			errorMessage = 'Investment goal is required';
			return;
		}
		
		isSaving = true;
		errorMessage = null;
		
		try {
			const update: AgentUpdate = {
				name: agentName,
				goal: agentGoal,
				description: agentDescription || undefined,
			};
			
			if (agent.type === 'rule_based') {
				update.rules = rules;
			} else {
				update.llm_config = llmConfig;
			}
			
			await api.updateAgent(agent.id, update);
			
			// Success! Navigate back to agent details
			goto(`/agents/${agent.id}`);
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to save agent';
			isSaving = false;
		}
	}
	
	function cancel() {
		if (agent) {
			goto(`/agents/${agent.id}`);
		} else {
			goto('/agents');
		}
	}
</script>

<svelte:head>
	<title>Edit {agent?.name || 'Agent'} - AI Agent Builder</title>
</svelte:head>

<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	{#if isLoading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
		</div>
		
	{:else if errorMessage && !agent}
		<div class="bg-red-50 border border-red-200 rounded-lg p-6">
			<h3 class="text-lg font-medium text-red-900 mb-2">Error Loading Agent</h3>
			<p class="text-red-700 mb-4">{errorMessage}</p>
			<button
				onclick={() => goto('/agents')}
				class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
			>
				Back to Agents
			</button>
		</div>
		
	{:else if agent}
		<!-- Header -->
		<div class="mb-8">
			<div class="flex items-center space-x-4 mb-4">
				<button
					onclick={cancel}
					class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
					</svg>
				</button>
				
				<div>
					<h1 class="text-3xl font-bold text-gray-900">Edit Agent</h1>
					<p class="text-gray-600 mt-1">Update your agent's configuration</p>
				</div>
			</div>
		</div>
		
		<!-- Error Message -->
		{#if errorMessage}
			<div class="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
				<svg class="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<p class="text-sm text-red-800">{errorMessage}</p>
			</div>
		{/if}
		
		<!-- Edit Form -->
		<div class="bg-white rounded-xl shadow-lg p-8 mb-6">
			<div class="space-y-6">
				<!-- Basic Info -->
				<div>
					<h2 class="text-xl font-semibold text-gray-900 mb-4">Basic Information</h2>
					
					<div class="space-y-4">
						<div>
							<label for="name" class="block text-sm font-medium text-gray-700 mb-2">
								Agent Name *
							</label>
							<input
								id="name"
								type="text"
								class="input-field"
								bind:value={agentName}
								placeholder="e.g., Value Stock Finder"
							/>
						</div>
						
						<div>
							<label for="goal" class="block text-sm font-medium text-gray-700 mb-2">
								Investment Goal *
							</label>
							<textarea
								id="goal"
								class="input-field"
								bind:value={agentGoal}
								rows="3"
								placeholder="Describe what this agent should accomplish..."
							></textarea>
						</div>
						
						<div>
							<label for="description" class="block text-sm font-medium text-gray-700 mb-2">
								Description (Optional)
							</label>
							<textarea
								id="description"
								class="input-field"
								bind:value={agentDescription}
								rows="2"
								placeholder="Additional details about this agent..."
							></textarea>
						</div>
					</div>
				</div>
				
				<!-- Configuration -->
				<div>
					<h2 class="text-xl font-semibold text-gray-900 mb-4">
						{agent.type === 'rule_based' ? 'Rules Configuration' : 'AI Configuration'}
					</h2>
					
					{#if agent.type === 'rule_based'}
						<RuleBuilder bind:rules onchange={(newRules) => rules = newRules} />
					{:else}
						<LLMConfigComponent 
							bind:config={llmConfig} 
							agentId={agent.id}
							onchange={(newConfig) => llmConfig = newConfig} 
						/>
					{/if}
				</div>
			</div>
		</div>
		
		<!-- Action Buttons -->
		<div class="flex items-center justify-between">
			<button
				type="button"
				class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
				onclick={cancel}
				disabled={isSaving}
			>
				Cancel
			</button>
			
			<button
				type="button"
				class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium flex items-center space-x-2 disabled:opacity-50"
				onclick={saveAgent}
				disabled={isSaving}
			>
				{#if isSaving}
					<svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					<span>Saving...</span>
				{:else}
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>Save Changes</span>
				{/if}
			</button>
		</div>
	{/if}
</div>

<style>
	.input-field {
		@apply w-full px-4 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
	}
</style>
