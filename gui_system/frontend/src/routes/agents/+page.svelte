<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api, type Agent } from '$lib/api';
	
	let agents = $state<Agent[]>([]);
	let isLoading = $state(true);
	let errorMessage = $state<string | null>(null);
	let deletingId = $state<string | null>(null);
	
	onMount(async () => {
		await loadAgents();
	});
	
	async function loadAgents() {
		try {
			isLoading = true;
			errorMessage = null;
			const response = await api.listAgents();
			agents = response.agents;
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to load agents';
		} finally {
			isLoading = false;
		}
	}
	
	async function deleteAgent(agentId: string) {
		if (!confirm('Are you sure you want to delete this agent?')) {
			return;
		}
		
		try {
			deletingId = agentId;
			await api.deleteAgent(agentId);
			await loadAgents();
		} catch (err) {
			alert(err instanceof Error ? err.message : 'Failed to delete agent');
		} finally {
			deletingId = null;
		}
	}
	
	async function exportAgent(agentId: string, agentName: string) {
		try {
			const response = await api.exportAgentCode(agentId);
			
			// Create download link
			const blob = new Blob([response.code], { type: 'text/plain' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = response.filename;
			a.click();
			URL.revokeObjectURL(url);
		} catch (err) {
			alert(err instanceof Error ? err.message : 'Failed to export agent');
		}
	}
	
	function getTypeColor(type: string): string {
		return type === 'rule_based' ? 'bg-green-100 text-green-800' : 'bg-purple-100 text-purple-800';
	}
	
	function getTypeIcon(type: string): string {
		return type === 'rule_based' ? 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' : 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z';
	}
	
	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-US', { 
			month: 'short', 
			day: 'numeric', 
			year: 'numeric' 
		});
	}
</script>

<svelte:head>
	<title>My Agents - AI Agent Builder</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<!-- Header -->
	<div class="flex items-center justify-between mb-8">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">My Agents</h1>
			<p class="text-gray-600 mt-1">Manage your investment agents</p>
		</div>
		<a
			href="/create"
			class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
		>
			<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
			</svg>
			Create Agent
		</a>
	</div>
	
	{#if isLoading}
		<!-- Loading State -->
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
		</div>
		
	{:else if errorMessage}
		<!-- Error State -->
		<div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
			<svg class="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
			<h3 class="text-lg font-medium text-red-900 mb-2">Failed to Load Agents</h3>
			<p class="text-red-700 mb-4">{errorMessage}</p>
			<button
				onclick={loadAgents}
				class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
			>
				Retry
			</button>
		</div>
		
	{:else if agents.length === 0}
		<!-- Empty State -->
		<div class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
			<svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
			</svg>
			<h3 class="text-lg font-medium text-gray-900 mb-2">No Agents Yet</h3>
			<p class="text-gray-600 mb-6">Create your first investment agent to get started</p>
			<a
				href="/create"
				class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
			>
				<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
				</svg>
				Create Your First Agent
			</a>
		</div>
		
	{:else}
		<!-- Agents Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each agents as agent}
				<div class="agent-card">
					<!-- Card Header -->
					<div class="flex items-start justify-between mb-4">
						<div class="flex items-center space-x-3">
							<div class="icon-wrapper" class:rule-based={agent.type === 'rule_based'} class:llm-based={agent.type === 'llm_based'}>
								<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={getTypeIcon(agent.type)} />
								</svg>
							</div>
							<div>
								<h3 class="font-semibold text-gray-900 line-clamp-1">{agent.name}</h3>
								<span class="badge {getTypeColor(agent.type)}">
									{agent.type === 'rule_based' ? 'Rule-Based' : 'AI-Powered'}
								</span>
							</div>
						</div>
					</div>
					
					<!-- Goal -->
					<p class="text-sm text-gray-600 mb-4 line-clamp-3">{agent.goal}</p>
					
					<!-- Meta Info -->
					<div class="flex items-center justify-between text-xs text-gray-500 mb-4 pt-4 border-t border-gray-200">
						<div class="flex items-center">
							<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
							</svg>
							{agent.rules.length} rule{agent.rules.length !== 1 ? 's' : ''}
						</div>
						<div class="flex items-center">
							<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
							</svg>
							{formatDate(agent.created_at)}
						</div>
					</div>
					
					<!-- Actions -->
					<div class="flex space-x-2">
						<button
							type="button"
							class="action-btn primary"
							onclick={() => goto(`/agents/${agent.id}`)}
							title="View details"
						>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
							</svg>
							View
						</button>
						
						<button
							type="button"
							class="action-btn"
							onclick={() => exportAgent(agent.id, agent.name)}
							title="Export as Python code"
						>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
							</svg>
							Export
						</button>
						
						<button
							type="button"
							class="action-btn danger"
							onclick={() => deleteAgent(agent.id)}
							disabled={deletingId === agent.id}
							title="Delete agent"
						>
							{#if deletingId === agent.id}
								<svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
							{:else}
								<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
								</svg>
							{/if}
						</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.agent-card {
		@apply bg-white border border-gray-200 rounded-xl p-6;
		@apply hover:shadow-lg hover:border-primary-300 transition-all;
	}
	
	.icon-wrapper {
		@apply w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0;
	}
	
	.icon-wrapper.rule-based {
		@apply bg-green-600;
	}
	
	.icon-wrapper.llm-based {
		@apply bg-purple-600;
	}
	
	.badge {
		@apply inline-block px-2 py-1 text-xs font-medium rounded-full;
	}
	
	.action-btn {
		@apply flex-1 px-3 py-2 border border-gray-300 rounded-lg;
		@apply hover:bg-gray-50 transition-colors;
		@apply flex items-center justify-center space-x-1;
		@apply text-sm font-medium text-gray-700;
		@apply disabled:opacity-50 disabled:cursor-not-allowed;
	}
	
	.action-btn.primary {
		@apply border-primary-500 text-primary-700 hover:bg-primary-50;
	}
	
	.action-btn.danger {
		@apply border-red-300 text-red-700 hover:bg-red-50;
	}
	
	.line-clamp-1 {
		display: -webkit-box;
		-webkit-line-clamp: 1;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
	
	.line-clamp-3 {
		display: -webkit-box;
		-webkit-line-clamp: 3;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
