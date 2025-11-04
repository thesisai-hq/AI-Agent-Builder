<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api, type Template } from '$lib/api';
	import { templates, loading, error } from '$lib/stores/agents';
	import TemplateCard from '$lib/components/TemplateCard.svelte';

	let templatesData = $state<Template[]>([]);
	let isLoading = $state(true);
	let errorMessage = $state<string | null>(null);
	let stats = $state({
		totalAgents: 0,
		ruleBasedAgents: 0,
		llmAgents: 0
	});

	// Load templates on mount
	onMount(async () => {
		try {
			isLoading = true;
			const response = await api.listTemplates();
			templatesData = response.templates;
			templates.set(response.templates);
			
			// Load agent stats
			const agentsResponse = await api.listAgents();
			stats.totalAgents = agentsResponse.total;
			stats.ruleBasedAgents = agentsResponse.agents.filter(a => a.type === 'rule_based').length;
			stats.llmAgents = agentsResponse.agents.filter(a => a.type === 'llm_based').length;
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to load templates';
			error.set(errorMessage);
		} finally {
			isLoading = false;
		}
	});

	function handleTemplateClick(template: Template) {
		// Navigate to create page with template pre-selected
		goto(`/create?template=${template.id}`);
	}
</script>

<svelte:head>
	<title>AI Agent Builder - Home</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<!-- Hero Section -->
	<div class="text-center mb-12">
		<h1 class="text-4xl font-bold text-gray-900 mb-4">
			Build Your Investment Team
		</h1>
		<p class="text-xl text-gray-600 max-w-3xl mx-auto">
			Create AI-powered agents to automate your investment strategy. Choose from proven templates or build your own custom agent.
		</p>
	</div>

	<!-- Stats -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
		<div class="bg-white rounded-lg shadow p-6 border border-gray-200">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm font-medium text-gray-600">Total Agents</p>
					<p class="text-3xl font-bold text-gray-900 mt-1">{stats.totalAgents}</p>
				</div>
				<div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
					<svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
					</svg>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg shadow p-6 border border-gray-200">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm font-medium text-gray-600">Rule-Based</p>
					<p class="text-3xl font-bold text-gray-900 mt-1">{stats.ruleBasedAgents}</p>
				</div>
				<div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
					<svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
					</svg>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg shadow p-6 border border-gray-200">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm font-medium text-gray-600">AI-Powered</p>
					<p class="text-3xl font-bold text-gray-900 mt-1">{stats.llmAgents}</p>
				</div>
				<div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
					<svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
					</svg>
				</div>
			</div>
		</div>
	</div>

	<!-- Quick Actions -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
		<a
			href="/create"
			class="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl p-8 text-white hover:shadow-xl transition-all duration-200 group"
		>
			<div class="flex items-center justify-between mb-4">
				<h2 class="text-2xl font-bold">Create New Agent</h2>
				<svg class="w-8 h-8 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
				</svg>
			</div>
			<p class="text-primary-100">Build a custom agent from scratch with your own rules and strategies</p>
		</a>

		<a
			href="/agents"
			class="bg-gradient-to-br from-gray-700 to-gray-800 rounded-xl p-8 text-white hover:shadow-xl transition-all duration-200 group"
		>
			<div class="flex items-center justify-between mb-4">
				<h2 class="text-2xl font-bold">View My Agents</h2>
				<svg class="w-8 h-8 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</div>
			<p class="text-gray-300">Manage, test, and deploy your existing investment agents</p>
		</a>
	</div>

	<!-- Templates Section -->
	<div class="mb-8">
		<div class="flex items-center justify-between mb-6">
			<div>
				<h2 class="text-2xl font-bold text-gray-900">Popular Templates</h2>
				<p class="text-gray-600 mt-1">Start with a proven strategy</p>
			</div>
		</div>

		{#if isLoading}
			<!-- Loading state -->
			<div class="flex items-center justify-center py-12">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
			</div>
		{:else if errorMessage}
			<!-- Error state -->
			<div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
				<svg class="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<h3 class="text-lg font-medium text-red-900 mb-2">Failed to Load Templates</h3>
				<p class="text-red-700">{errorMessage}</p>
				<button
					onclick={() => window.location.reload()}
					class="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
				>
					Retry
				</button>
			</div>
		{:else if templatesData.length === 0}
			<!-- Empty state -->
			<div class="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
				<svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
				</svg>
				<h3 class="text-lg font-medium text-gray-900 mb-2">No Templates Available</h3>
				<p class="text-gray-600">Check your backend configuration</p>
			</div>
		{:else}
			<!-- Templates grid -->
			<div class="grid grid-cols-1 gap-6">
				{#each templatesData as template}
					<TemplateCard 
						{template} 
						onclick={() => handleTemplateClick(template)}
					/>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Info Banner -->
	<div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-12">
		<div class="flex">
			<div class="flex-shrink-0">
				<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			</div>
			<div class="ml-3">
				<h3 class="text-sm font-medium text-blue-900">Getting Started</h3>
				<div class="mt-2 text-sm text-blue-700">
					<p>
						Select a template above to create an agent with pre-configured rules, or 
						<a href="/create" class="font-medium underline hover:text-blue-800">build from scratch</a>
						to customize every aspect of your strategy.
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
