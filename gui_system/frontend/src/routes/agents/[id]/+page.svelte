<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { api, type Agent, type AnalysisResult } from '$lib/api';
	
	let agent = $state<Agent | null>(null);
	let isLoading = $state(true);
	let errorMessage = $state<string | null>(null);
	
	// Test interface
	let testTicker = $state('');
	let isAnalyzing = $state(false);
	let analysisResult = $state<AnalysisResult | null>(null);
	let analysisError = $state<string | null>(null);
	
	// Export
	let isExporting = $state(false);
	
	onMount(async () => {
		const agentId = $page.params.id;
		await loadAgent(agentId);
	});
	
	async function loadAgent(agentId: string) {
		try {
			isLoading = true;
			errorMessage = null;
			agent = await api.getAgent(agentId);
		} catch (err) {
			errorMessage = err instanceof Error ? err.message : 'Failed to load agent';
		} finally {
			isLoading = false;
		}
	}
	
	async function analyzeStock() {
		if (!testTicker.trim() || !agent) return;
		
		isAnalyzing = true;
		analysisError = null;
		analysisResult = null;
		
		try {
			const result = await api.analyzeStock(testTicker.toUpperCase(), agent.id);
			analysisResult = result;
		} catch (err) {
			analysisError = err instanceof Error ? err.message : 'Analysis failed';
		} finally {
			isAnalyzing = false;
		}
	}
	
	async function exportCode() {
		if (!agent) return;
		
		isExporting = true;
		try {
			const response = await api.exportAgentCode(agent.id);
			
			// Create download
			const blob = new Blob([response.code], { type: 'text/plain' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = response.filename;
			a.click();
			URL.revokeObjectURL(url);
		} catch (err) {
			alert(err instanceof Error ? err.message : 'Export failed');
		} finally {
			isExporting = false;
		}
	}
	
	async function deleteAgent() {
		if (!agent) return;
		
		if (!confirm(`Are you sure you want to delete "${agent.name}"?`)) {
			return;
		}
		
		try {
			await api.deleteAgent(agent.id);
			goto('/agents');
		} catch (err) {
			alert(err instanceof Error ? err.message : 'Failed to delete agent');
		}
	}
	
	function getSignalColor(direction: string): string {
		if (direction === 'bullish') return 'bg-green-100 text-green-800 border-green-300';
		if (direction === 'bearish') return 'bg-red-100 text-red-800 border-red-300';
		return 'bg-gray-100 text-gray-800 border-gray-300';
	}
	
	function getSignalIcon(direction: string): string {
		if (direction === 'bullish') return 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6';
		if (direction === 'bearish') return 'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6';
		return 'M5 13l4 4L19 7';
	}
	
	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleString('en-US', { 
			month: 'short', 
			day: 'numeric', 
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>{agent?.name || 'Agent Details'} - AI Agent Builder</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	{#if isLoading}
		<!-- Loading State -->
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
		</div>
		
	{:else if errorMessage}
		<!-- Error State -->
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
		<div class="flex items-center justify-between mb-8">
			<div class="flex items-center space-x-4">
				<button
					onclick={() => goto('/agents')}
					class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
					</svg>
				</button>
				
				<div>
					<h1 class="text-3xl font-bold text-gray-900">{agent.name}</h1>
					<p class="text-gray-600 mt-1">{agent.goal}</p>
				</div>
			</div>
			
			<div class="flex space-x-3">
				<button
					onclick={exportCode}
					disabled={isExporting}
					class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center space-x-2"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
					</svg>
					<span>{isExporting ? 'Exporting...' : 'Export Code'}</span>
				</button>
				
				<button
					onclick={deleteAgent}
					class="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors flex items-center space-x-2"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
					</svg>
					<span>Delete</span>
				</button>
			</div>
		</div>
		
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Left Column: Agent Details -->
			<div class="lg:col-span-1 space-y-6">
				<!-- Agent Info Card -->
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4">Agent Information</h2>
					
					<div class="space-y-3">
						<div>
							<label class="text-sm font-medium text-gray-600">Type</label>
							<div class="mt-1">
								{#if agent.type === 'rule_based'}
									<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
										</svg>
										Rule-Based
									</span>
								{:else}
									<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
										</svg>
										AI-Powered
									</span>
								{/if}
							</div>
						</div>
						
						{#if agent.description}
							<div>
								<label class="text-sm font-medium text-gray-600">Description</label>
								<p class="mt-1 text-sm text-gray-900">{agent.description}</p>
							</div>
						{/if}
						
						<div>
							<label class="text-sm font-medium text-gray-600">Created</label>
							<p class="mt-1 text-sm text-gray-900">{formatDate(agent.created_at)}</p>
						</div>
						
						<div>
							<label class="text-sm font-medium text-gray-600">Last Updated</label>
							<p class="mt-1 text-sm text-gray-900">{formatDate(agent.updated_at)}</p>
						</div>
					</div>
				</div>
				
				<!-- Configuration Card -->
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4">Configuration</h2>
					
					{#if agent.type === 'rule_based'}
						<div>
							<label class="text-sm font-medium text-gray-600">Rules</label>
							<p class="mt-1 text-2xl font-bold text-gray-900">{agent.rules.length}</p>
							<p class="text-xs text-gray-500 mt-1">
								{agent.rules.reduce((sum, rule) => sum + rule.conditions.length, 0)} total conditions
							</p>
						</div>
						
						<div class="mt-4 space-y-2">
							{#each agent.rules as rule, index}
								<div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
									<div class="text-xs font-medium text-gray-900">Rule {index + 1}</div>
									<div class="text-xs text-gray-600 mt-1">
										{rule.conditions.length} condition{rule.conditions.length !== 1 ? 's' : ''} → 
										{rule.action.action} {rule.action.size}%
									</div>
									{#if rule.description}
										<div class="text-xs text-gray-500 mt-1 italic">{rule.description}</div>
									{/if}
								</div>
							{/each}
						</div>
					{:else if agent.llm_config}
						<div class="space-y-3">
							<div>
								<label class="text-sm font-medium text-gray-600">Provider</label>
								<p class="mt-1 text-sm text-gray-900 capitalize">{agent.llm_config.provider}</p>
							</div>
							<div>
								<label class="text-sm font-medium text-gray-600">Model</label>
								<p class="mt-1 text-sm text-gray-900">{agent.llm_config.model}</p>
							</div>
							<div>
								<label class="text-sm font-medium text-gray-600">Temperature</label>
								<p class="mt-1 text-sm text-gray-900">{agent.llm_config.temperature}</p>
							</div>
							{#if agent.llm_config.tools && agent.llm_config.tools.length > 0}
								<div>
									<label class="text-sm font-medium text-gray-600">Tools</label>
									<div class="mt-1 flex flex-wrap gap-1">
										{#each agent.llm_config.tools as tool}
											<span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">{tool}</span>
										{/each}
									</div>
								</div>
							{/if}
						</div>
					{/if}
				</div>
			</div>
			
			<!-- Right Column: Test Interface -->
			<div class="lg:col-span-2">
				<!-- Test Stock Analysis Card -->
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
						<svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
						</svg>
						Test Agent Analysis
					</h2>
					
					<p class="text-sm text-gray-600 mb-6">
						Enter a stock ticker to see how this agent would analyze it using live data from Yahoo Finance.
					</p>
					
					<!-- Ticker Input -->
					<div class="flex space-x-3 mb-6">
						<div class="flex-1">
							<input
								type="text"
								class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg uppercase"
								bind:value={testTicker}
								placeholder="Enter ticker (e.g., AAPL, TSLA, MSFT)"
								onkeypress={(e) => e.key === 'Enter' && analyzeStock()}
							/>
							<p class="text-xs text-gray-500 mt-1">
								Popular tickers: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META
							</p>
						</div>
						
						<button
							onclick={analyzeStock}
							disabled={!testTicker.trim() || isAnalyzing}
							class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center space-x-2"
						>
							{#if isAnalyzing}
								<svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
								<span>Analyzing...</span>
							{:else}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
								</svg>
								<span>Analyze</span>
							{/if}
						</button>
					</div>
					
					<!-- Analysis Error -->
					{#if analysisError}
						<div class="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
							<svg class="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<div>
								<p class="text-sm font-medium text-red-900">Analysis Failed</p>
								<p class="text-sm text-red-700 mt-1">{analysisError}</p>
							</div>
						</div>
					{/if}
					
					<!-- Analysis Result -->
					{#if analysisResult}
						<div class="border-t border-gray-200 pt-6">
							<div class="flex items-center justify-between mb-4">
								<h3 class="text-lg font-semibold text-gray-900">Analysis Result</h3>
								<span class="text-xs text-gray-500">{formatDate(analysisResult.timestamp)}</span>
							</div>
							
							<!-- Signal Badge -->
							<div class="mb-6">
								<div class="flex items-center space-x-4">
									<div class="signal-badge {getSignalColor(analysisResult.direction)}">
										<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={getSignalIcon(analysisResult.direction)} />
										</svg>
										<div>
											<div class="text-sm font-medium uppercase">{analysisResult.direction}</div>
											<div class="text-xs opacity-75">Signal</div>
										</div>
									</div>
									
									<div class="flex-1">
										<label class="text-sm font-medium text-gray-600">Confidence</label>
										<div class="mt-1">
											<div class="flex items-center space-x-2">
												<div class="flex-1 bg-gray-200 rounded-full h-3">
													<div 
														class="h-3 rounded-full transition-all duration-500 {
															analysisResult.confidence > 0.7 ? 'bg-green-500' :
															analysisResult.confidence > 0.4 ? 'bg-yellow-500' :
															'bg-red-500'
														}"
														style="width: {analysisResult.confidence * 100}%"
													></div>
												</div>
												<span class="text-sm font-semibold text-gray-900 w-12">
													{(analysisResult.confidence * 100).toFixed(0)}%
												</span>
											</div>
										</div>
									</div>
								</div>
							</div>
							
							<!-- Reasoning -->
							<div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
								<label class="text-sm font-semibold text-gray-900 mb-2 block">Analysis Reasoning</label>
								<p class="text-sm text-gray-700 leading-relaxed">{analysisResult.reasoning}</p>
							</div>
							
							<!-- Metadata -->
							<div class="mt-4 grid grid-cols-2 gap-4 text-sm">
								<div class="bg-blue-50 rounded-lg p-3">
									<label class="text-xs font-medium text-blue-900">Ticker</label>
									<p class="text-lg font-bold text-blue-900 mt-1">{analysisResult.ticker}</p>
								</div>
								<div class="bg-blue-50 rounded-lg p-3">
									<label class="text-xs font-medium text-blue-900">Data Source</label>
									<p class="text-sm font-semibold text-blue-900 mt-1">Yahoo Finance (yfinance)</p>
								</div>
							</div>
						</div>
					{:else}
						<!-- Placeholder -->
						<div class="border-t border-gray-200 pt-6">
							<div class="text-center py-12">
								<svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
								</svg>
								<p class="text-gray-500">Enter a ticker and click Analyze to test this agent</p>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.signal-badge {
		@apply flex items-center space-x-3 px-4 py-3 rounded-lg border-2;
	}
</style>
