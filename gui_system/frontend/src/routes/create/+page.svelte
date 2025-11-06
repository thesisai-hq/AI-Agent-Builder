<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { api, type Template, type Rule, type AgentCreate, type LLMConfig } from '$lib/api';
	import { loading } from '$lib/stores/agents';
	import RuleBuilder from '$lib/components/RuleBuilder.svelte';
	import LLMConfigComponent from '$lib/components/LLMConfig.svelte';
	
	// Steps
	const steps = [
		{ id: 'template', name: 'Choose Template', icon: 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01' },
		{ id: 'info', name: 'Basic Info', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
		{ id: 'type', name: 'Agent Type', icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' },
		{ id: 'config', name: 'Configuration', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' },
		{ id: 'review', name: 'Review & Create', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' }
	];
	
	let currentStep = $state(0);
	let templates = $state<Template[]>([]);
	let selectedTemplate = $state<Template | null>(null);
	let isCreating = $state(false);
	let errorMessage = $state<string | null>(null);
	
	// Form data
	let agentName = $state('');
	let agentGoal = $state('');
	let agentDescription = $state('');
	let agentType = $state<'rule_based' | 'llm_based'>('rule_based');
	let rules = $state<Rule[]>([]);
	let llmConfig = $state<LLMConfig>({
		provider: 'openai',
		model: 'gpt-4',
		temperature: 0.7,
		max_tokens: 2000,
		system_prompt: '',
		tools: []
	});
	
	// Load templates on mount
	onMount(async () => {
		try {
			const response = await api.listTemplates();
			templates = response.templates;
			
			// Check if template is pre-selected from URL
			const templateId = $page.url.searchParams.get('template');
			if (templateId) {
				const template = templates.find(t => t.id === templateId);
				if (template) {
					selectTemplate(template);
					currentStep = 1; // Skip to info step
				}
			}
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to load templates';
		}
	});
	
	function selectTemplate(template: Template) {
		selectedTemplate = template;
		agentName = template.name;
		agentGoal = template.goal;
		agentDescription = template.description;
		agentType = template.type;
		rules = template.rules;
		if (template.llm_config) {
			llmConfig = template.llm_config;
		}
	}
	
	function skipTemplate() {
		selectedTemplate = null;
		agentName = '';
		agentGoal = '';
		agentDescription = '';
		rules = [];
		currentStep = 1;
	}
	
	function nextStep() {
		if (validateCurrentStep()) {
			currentStep++;
		}
	}
	
	function previousStep() {
		currentStep--;
		errorMessage = null;
	}
	
	function validateCurrentStep(): boolean {
		errorMessage = null;
		
		switch (currentStep) {
			case 0: // Template
				if (!selectedTemplate) {
					errorMessage = 'Please select a template or skip to create from scratch';
					return false;
				}
				return true;
			
			case 1: // Info
				if (!agentName.trim()) {
					errorMessage = 'Please enter an agent name';
					return false;
				}
				if (!agentGoal.trim()) {
					errorMessage = 'Please enter an investment goal';
					return false;
				}
				return true;
			
			case 2: // Type selection
				return true;
			
			case 3: // Configuration
				if (agentType === 'rule_based') {
					if (rules.length === 0) {
						errorMessage = 'Please add at least one rule';
						return false;
					}
					// Validate each rule has conditions
					for (const rule of rules) {
						if (rule.conditions.length === 0) {
							errorMessage = 'Each rule must have at least one condition';
							return false;
						}
					}
				}
				return true;
			
			default:
				return true;
		}
	}
	
	async function createAgent() {
		if (!validateCurrentStep()) return;
		
		isCreating = true;
		errorMessage = null;
		
		try {
			const agentData: AgentCreate = {
				name: agentName,
				type: agentType,
				goal: agentGoal,
				description: agentDescription || undefined,
				template_id: selectedTemplate?.id,
				rules: agentType === 'rule_based' ? rules : [],
				llm_config: agentType === 'llm_based' ? llmConfig : undefined
			};
			
			const newAgent = await api.createAgent(agentData);
			
			// Success! Navigate to agents list
			goto('/agents');
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to create agent';
			isCreating = false;
		}
	}
</script>

<svelte:head>
	<title>Create Agent - AI Agent Builder</title>
</svelte:head>

<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<!-- Progress Steps -->
	<div class="mb-12">
		<div class="flex items-center justify-between">
			{#each steps as step, index}
				<div class="flex items-center {index < steps.length - 1 ? 'flex-1' : ''}">
					<!-- Step Circle -->
					<div class="flex items-center">
						<div 
							class="step-circle"
							class:active={index === currentStep}
							class:completed={index < currentStep}
						>
							{#if index < currentStep}
								<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
								</svg>
							{:else}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={step.icon} />
								</svg>
							{/if}
						</div>
						<div class="ml-3 hidden md:block">
							<p class="text-sm font-medium" class:text-primary-600={index <= currentStep} class:text-gray-500={index > currentStep}>
								{step.name}
							</p>
						</div>
					</div>
					
					<!-- Connector Line -->
					{#if index < steps.length - 1}
						<div class="flex-1 h-0.5 mx-4 {index < currentStep ? 'bg-primary-600' : 'bg-gray-300'}"></div>
					{/if}
				</div>
			{/each}
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
	
	<!-- Step Content -->
	<div class="bg-white rounded-xl shadow-lg p-8 mb-6">
		{#if currentStep === 0}
			<!-- Step 1: Template Selection -->
			<div class="space-y-6">
				<div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">Choose a Starting Point</h2>
					<p class="text-gray-600">Select a pre-built template or start from scratch</p>
				</div>
				
				<div class="grid grid-cols-1 gap-4">
					{#each templates as template}
						<button
							type="button"
							class="template-option"
							class:selected={selectedTemplate?.id === template.id}
							onclick={() => selectTemplate(template)}
						>
							<div class="flex items-center space-x-4">
								<div class="icon-circle" style="background-color: {template.color}">
									<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
									</svg>
								</div>
								<div class="flex-1 text-left">
									<h3 class="font-semibold text-gray-900">{template.name}</h3>
									<p class="text-sm text-gray-600">{template.description}</p>
								</div>
								{#if selectedTemplate?.id === template.id}
									<svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
								{/if}
							</div>
						</button>
					{/each}
					
					<!-- Skip option -->
					<button
						type="button"
						class="template-option border-dashed"
						onclick={skipTemplate}
					>
						<div class="flex items-center space-x-4">
							<div class="icon-circle bg-gray-200">
								<svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
								</svg>
							</div>
							<div class="flex-1 text-left">
								<h3 class="font-semibold text-gray-900">Start from Scratch</h3>
								<p class="text-sm text-gray-600">Create a custom agent with your own rules</p>
							</div>
						</div>
					</button>
				</div>
			</div>
			
		{:else if currentStep === 1}
			<!-- Step 2: Basic Info -->
			<div class="space-y-6">
				<div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">Basic Information</h2>
					<p class="text-gray-600">Tell us about your investment agent</p>
				</div>
				
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
			
		{:else if currentStep === 2}
			<!-- Step 3: Agent Type Selection -->
			<div class="space-y-6">
				<div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">Choose Agent Type</h2>
					<p class="text-gray-600">Select how your agent will make decisions</p>
				</div>
				
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<!-- Rule-Based Option -->
					<button
						type="button"
						class="type-card"
						class:selected={agentType === 'rule_based'}
						onclick={() => { agentType = 'rule_based'; }}
					>
						<div class="type-icon rule-based">
							<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
							</svg>
						</div>
						<h3 class="text-xl font-bold text-gray-900 mb-2">Rule-Based</h3>
						<p class="text-sm text-gray-600 mb-4">Traditional systematic approach</p>
						
						<div class="features-list">
							<div class="feature">
								<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Precise, predictable rules</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Easy to backtest</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Lower cost (no LLM)</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Full transparency</span>
							</div>
						</div>
					</button>
					
					<!-- LLM-Based Option -->
					<button
						type="button"
						class="type-card"
						class:selected={agentType === 'llm_based'}
						onclick={() => { agentType = 'llm_based'; }}
					>
						<div class="type-icon llm-based">
							<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
							</svg>
						</div>
						<h3 class="text-xl font-bold text-gray-900 mb-2">AI-Powered (LLM)</h3>
						<p class="text-sm text-gray-600 mb-4">Intelligent decision making</p>
						
						<div class="features-list">
							<div class="feature">
								<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Adapts to market conditions</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Processes complex data</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Natural language reasoning</span>
							</div>
							<div class="feature">
								<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
								<span>Continuous learning</span>
							</div>
						</div>
					</button>
				</div>
			</div>
			
		{:else if currentStep === 3}
			<!-- Step 4: Configuration -->
			<div class="space-y-6">
				<div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">
						{agentType === 'rule_based' ? 'Configure Rules' : 'Configure AI Model'}
					</h2>
					<p class="text-gray-600">
						{agentType === 'rule_based' 
							? 'Define the conditions and actions for your agent' 
							: 'Set up the AI model that will power your agent'}
					</p>
				</div>
				
				{#if agentType === 'rule_based'}
					<RuleBuilder bind:rules onchange={(newRules) => rules = newRules} />
				{:else}
					<LLMConfigComponent bind:config={llmConfig} onchange={(newConfig) => llmConfig = newConfig} />
				{/if}
			</div>
			
		{:else}
			<!-- Step 5: Review -->
			<div class="space-y-6">
				<div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">Review & Create</h2>
					<p class="text-gray-600">Review your agent configuration before creating</p>
				</div>
				
				<div class="space-y-4">
					<!-- Agent Info -->
					<div class="review-section">
						<h3 class="review-title">Agent Information</h3>
						<div class="review-grid">
							<div>
								<span class="review-label">Name:</span>
								<span class="review-value">{agentName}</span>
							</div>
							<div>
								<span class="review-label">Type:</span>
								<span class="review-value">
									{#if agentType === 'rule_based'}
										<span class="badge bg-green-100 text-green-800">Rule-Based</span>
									{:else}
										<span class="badge bg-purple-100 text-purple-800">AI-Powered</span>
									{/if}
								</span>
							</div>
							<div class="col-span-2">
								<span class="review-label">Goal:</span>
								<span class="review-value">{agentGoal}</span>
							</div>
							{#if agentDescription}
								<div class="col-span-2">
									<span class="review-label">Description:</span>
									<span class="review-value">{agentDescription}</span>
								</div>
							{/if}
							{#if selectedTemplate}
								<div class="col-span-2">
									<span class="review-label">Template:</span>
									<span class="review-value">{selectedTemplate.name}</span>
								</div>
							{/if}
						</div>
					</div>
					
					<!-- Rules or LLM Config Summary -->
					{#if agentType === 'rule_based'}
						<div class="review-section">
							<h3 class="review-title">Rules ({rules.length})</h3>
							<div class="space-y-2">
								{#each rules as rule, index}
									<div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
										<div class="text-sm font-medium text-gray-900 mb-1">Rule {index + 1}</div>
										<div class="text-sm text-gray-600">
											{rule.conditions.length} condition{rule.conditions.length !== 1 ? 's' : ''} → 
											{rule.action.action} {rule.action.size}% of portfolio
										</div>
										{#if rule.description}
											<div class="text-xs text-gray-500 mt-1">{rule.description}</div>
										{/if}
									</div>
								{/each}
							</div>
						</div>
					{:else}
						<div class="review-section">
							<h3 class="review-title">AI Configuration</h3>
							<div class="review-grid">
								<div>
									<span class="review-label">Provider:</span>
									<span class="review-value">{llmConfig.provider}</span>
								</div>
								<div>
									<span class="review-label">Model:</span>
									<span class="review-value">{llmConfig.model}</span>
								</div>
								<div>
									<span class="review-label">Temperature:</span>
									<span class="review-value">{llmConfig.temperature}</span>
								</div>
								<div>
									<span class="review-label">Max Tokens:</span>
									<span class="review-value">{llmConfig.max_tokens}</span>
								</div>
								<div class="col-span-2">
									<span class="review-label">Tools Enabled:</span>
									<span class="review-value">
										{llmConfig.tools?.length || 0} 
										{#if llmConfig.tools && llmConfig.tools.length > 0}
											({llmConfig.tools.join(', ')})
										{/if}
									</span>
								</div>
							</div>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</div>
	
	<!-- Navigation Buttons -->
	<div class="flex items-center justify-between">
		<button
			type="button"
			class="btn-secondary"
			onclick={previousStep}
			disabled={currentStep === 0}
		>
			<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			Back
		</button>
		
		{#if currentStep < steps.length - 1}
			<button
				type="button"
				class="btn-primary"
				onclick={nextStep}
			>
				Next
				<svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</button>
		{:else}
			<button
				type="button"
				class="btn-primary"
				onclick={createAgent}
				disabled={isCreating}
			>
				{#if isCreating}
					<svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					Creating...
				{:else}
					<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					Create Agent
				{/if}
			</button>
		{/if}
	</div>
</div>

<style>
	.step-circle {
		@apply w-12 h-12 rounded-full border-2 border-gray-300;
		@apply flex items-center justify-center;
		@apply text-gray-400 bg-white transition-all;
	}
	
	.step-circle.active {
		@apply border-primary-600 bg-primary-600 text-white;
	}
	
	.step-circle.completed {
		@apply border-primary-600 bg-primary-600 text-white;
	}
	
	.template-option {
		@apply w-full p-4 border-2 border-gray-200 rounded-lg;
		@apply hover:border-primary-300 hover:shadow-md transition-all;
		@apply text-left;
	}
	
	.template-option.selected {
		@apply border-primary-500 bg-primary-50;
	}
	
	.icon-circle {
		@apply w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0;
	}
	
	.input-field {
		@apply w-full px-4 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
	}
	
	.type-card {
		@apply p-6 border-2 border-gray-200 rounded-xl;
		@apply hover:border-primary-300 hover:shadow-lg transition-all;
		@apply text-left w-full;
	}
	
	.type-card.selected {
		@apply border-primary-500 bg-primary-50 ring-2 ring-primary-200;
	}
	
	.type-icon {
		@apply w-16 h-16 rounded-xl flex items-center justify-center mb-4;
	}
	
	.type-icon.rule-based {
		@apply bg-green-600;
	}
	
	.type-icon.llm-based {
		@apply bg-purple-600;
	}
	
	.features-list {
		@apply space-y-2;
	}
	
	.feature {
		@apply flex items-center space-x-2 text-sm text-gray-700;
	}
	
	.review-section {
		@apply p-6 bg-gray-50 rounded-lg border border-gray-200;
	}
	
	.review-title {
		@apply text-lg font-semibold text-gray-900 mb-4;
	}
	
	.review-grid {
		@apply grid grid-cols-2 gap-4;
	}
	
	.review-label {
		@apply text-sm font-medium text-gray-600;
	}
	
	.review-value {
		@apply text-sm text-gray-900 ml-2;
	}
	
	.badge {
		@apply inline-block px-2 py-1 text-xs font-medium rounded-full;
	}
	
	.btn-primary {
		@apply px-6 py-3 bg-primary-600 text-white rounded-lg;
		@apply hover:bg-primary-700 transition-colors;
		@apply flex items-center font-medium;
		@apply disabled:opacity-50 disabled:cursor-not-allowed;
	}
	
	.btn-secondary {
		@apply px-6 py-3 border border-gray-300 text-gray-700 rounded-lg;
		@apply hover:bg-gray-50 transition-colors;
		@apply flex items-center font-medium;
		@apply disabled:opacity-50 disabled:cursor-not-allowed;
	}
</style>
