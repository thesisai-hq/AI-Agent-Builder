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
	
	// Prompt editing
	let isEditingPrompt = $state(false);
	let editedSystemPrompt = $state('');
	let isSavingPrompt = $state(false);
	let showPromptPreview = $state(false);
	
	// Data inspection
	let showDataDetails = $state(false);
	
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
			
			if (agent?.llm_config) {
				editedSystemPrompt = agent.llm_config.system_prompt || '';
			}
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
			showDataDetails = false; // Reset
		} catch (err) {
			analysisError = err instanceof Error ? err.message : 'Analysis failed';
		} finally {
			isAnalyzing = false;
		}
	}
	
	async function saveSystemPrompt() {
		if (!agent) return;
		
		isSavingPrompt = true;
		try {
			const updated = await api.updateAgent(agent.id, {
				llm_config: {
					...agent.llm_config!,
					system_prompt: editedSystemPrompt
				}
			});
			
			agent = updated;
			isEditingPrompt = false;
		} catch (err) {
			alert(err instanceof Error ? err.message : 'Failed to save prompt');
		} finally {
			isSavingPrompt = false;
		}
	}
	
	function cancelEditPrompt() {
		editedSystemPrompt = agent?.llm_config?.system_prompt || '';
		isEditingPrompt = false;
	}
	
	function generatePromptPreview(): string {
		if (!agent || !testTicker) return '';
		
		const lines = [
			'=== FUNDAMENTAL DATA ===',
			`Company: ${testTicker.toUpperCase()}`,
			'Sector: [From yfinance]',
			'Industry: [From yfinance]',
			'',
			'Valuation:',
			'  Price: $[From yfinance]',
			'  P/E Ratio: [From yfinance]',
			'  ...(all available metrics)',
			''
		];
		
		if (agent.llm_config?.tools?.includes('web_search')) {
			lines.push('=== RECENT NEWS ===', '- News headline 1', '- News headline 2', '...', '');
		}
		
		if (agent.llm_config?.tools?.includes('financial_data')) {
			lines.push('=== ADDITIONAL METRICS ===', 'Analyst Target: $XXX', 'Volume: XXX,XXX', '...', '');
		}
		
		lines.push(
			'Based on the above data, provide your recommendation.',
			'',
			'Respond in this EXACT format:',
			'SIGNAL: [bullish/bearish/neutral]',
			'CONFIDENCE: [0.0-1.0]',
			'REASONING: [your analysis]'
		);
		
		return lines.join('\n');
	}
	
	function formatFieldName(field: string): string {
		return field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
	}
	
	function formatValue(value: any): string {
		if (typeof value === 'number') {
			if (value > 1000000000) {
				return `$${(value / 1000000000).toFixed(2)}B`;
			} else if (value > 1000000) {
				return `$${(value / 1000000).toFixed(2)}M`;
			} else if (value > 1000) {
				return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
			}
			return value.toFixed(2);
		}
		return String(value);
	}
	
	async function exportCode() {
		if (!agent) return;
		
		isExporting = true;
		try {
			const response = await api.exportAgentCode(agent.id);
			
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
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
		</div>
		
	{:else if errorMessage}
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
					aria-label="Back to agents list"
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
			<!-- Left Column -->
			<div class="lg:col-span-1 space-y-6">
				<!-- Agent Info Card -->
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4">Agent Information</h2>
					
					<div class="space-y-3">
						<div>
							<div class="text-sm font-medium text-gray-600">Type</div>
							<div class="mt-1">
								{#if agent.type === 'rule_based'}
									<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
										Rule-Based
									</span>
								{:else}
									<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
										AI-Powered
									</span>
								{/if}
							</div>
						</div>
						
						{#if agent.description}
							<div>
								<div class="text-sm font-medium text-gray-600">Description</div>
								<p class="mt-1 text-sm text-gray-900">{agent.description}</p>
							</div>
						{/if}
						
						<div>
							<div class="text-sm font-medium text-gray-600">Created</div>
							<p class="mt-1 text-sm text-gray-900">{formatDate(agent.created_at)}</p>
						</div>
					</div>
				</div>
				
				<!-- Configuration Card -->
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4">Configuration</h2>
					
					{#if agent.type === 'rule_based'}
						<div>
							<div class="text-sm font-medium text-gray-600">Rules</div>
							<p class="mt-1 text-2xl font-bold text-gray-900">{agent.rules.length}</p>
						</div>
						
						<div class="mt-4 space-y-2">
							{#each agent.rules as rule, index}
								<div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
									<div class="text-xs font-medium text-gray-900">Rule {index + 1}</div>
									<div class="text-xs text-gray-600 mt-1">
										{rule.conditions.length} condition{rule.conditions.length !== 1 ? 's' : ''} → 
										{rule.action.action} {rule.action.size}%
									</div>
								</div>
							{/each}
						</div>
					{:else if agent.llm_config}
						<div class="space-y-3">
							<div>
								<div class="text-sm font-medium text-gray-600">Provider</div>
								<p class="mt-1 text-sm text-gray-900 capitalize">{agent.llm_config.provider}</p>
							</div>
							<div>
								<div class="text-sm font-medium text-gray-600">Model</div>
								<p class="mt-1 text-sm text-gray-900">{agent.llm_config.model}</p>
							</div>
							{#if agent.llm_config.tools && agent.llm_config.tools.length > 0}
								<div>
									<div class="text-sm font-medium text-gray-600">Tools Enabled</div>
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
				
				<!-- System Prompt Card (AI Only) -->
				{#if agent.type === 'llm_based' && agent.llm_config}
					<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
						<div class="flex items-center justify-between mb-4">
							<h2 class="text-lg font-semibold text-gray-900">System Prompt</h2>
							{#if !isEditingPrompt}
								<button
									onclick={() => { isEditingPrompt = true; editedSystemPrompt = agent.llm_config?.system_prompt || ''; }}
									class="text-sm text-primary-600 hover:text-primary-700 font-medium"
								>
									Edit
								</button>
							{/if}
						</div>
						
						{#if isEditingPrompt}
							<div class="space-y-3">
								<textarea
									bind:value={editedSystemPrompt}
									rows="12"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm font-mono"
									placeholder="You are a professional financial analyst..."
								></textarea>
								
								<div class="flex space-x-2">
									<button
										onclick={saveSystemPrompt}
										disabled={isSavingPrompt}
										class="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
									>
										{isSavingPrompt ? 'Saving...' : 'Save Changes'}
									</button>
									<button
										onclick={cancelEditPrompt}
										disabled={isSavingPrompt}
										class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
									>
										Cancel
									</button>
								</div>
							</div>
						{:else}
							<div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
								<pre class="text-xs text-gray-700 whitespace-pre-wrap font-mono">{agent.llm_config.system_prompt || 'No system prompt set (using default)'}</pre>
							</div>
						{/if}
						
						<button
							onclick={() => showPromptPreview = !showPromptPreview}
							class="mt-4 w-full text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center justify-center space-x-1"
						>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={showPromptPreview ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'} />
							</svg>
							<span>{showPromptPreview ? 'Hide' : 'Show'} Full Prompt Preview</span>
						</button>
						
						{#if showPromptPreview}
							<div class="mt-4 bg-blue-50 rounded-lg p-4 border border-blue-200">
								<div class="text-xs font-semibold text-blue-900 mb-2">
									📋 This is what will be sent to the LLM:
								</div>
								<pre class="text-xs text-blue-900 whitespace-pre-wrap font-mono max-h-96 overflow-y-auto">{generatePromptPreview()}</pre>
							</div>
						{/if}
					</div>
				{/if}
			</div>
			
			<!-- Right Column: Test Interface -->
			<div class="lg:col-span-2">
				<div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
					<h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
						<svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
						</svg>
						Test Agent Analysis
					</h2>
					
					<p class="text-sm text-gray-600 mb-6">
						Enter a stock ticker to analyze using live Yahoo Finance data
					</p>
					
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
								Popular: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, KO, T
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
								<span>Analyze</span>
							{/if}
						</button>
					</div>
					
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
					
					{#if analysisResult}
						<div class="border-t border-gray-200 pt-6 space-y-6">
							<!-- Signal & Confidence -->
							<div>
								<div class="flex items-center justify-between mb-4">
									<h3 class="text-lg font-semibold text-gray-900">Analysis Result</h3>
									<span class="text-xs text-gray-500">{formatDate(analysisResult.timestamp)}</span>
								</div>
								
								<div class="flex items-center space-x-4 mb-6">
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
										<div class="text-sm font-medium text-gray-600">Confidence</div>
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
								<div class="text-sm font-semibold text-gray-900 mb-2">Analysis Reasoning</div>
								<p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{analysisResult.reasoning}</p>
							</div>
							
							<!-- Data Quality Info -->
							{#if analysisResult.data_quality}
								<div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
									<div class="text-sm font-semibold text-blue-900 mb-3 flex items-center">
										<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
										</svg>
										Data Quality
									</div>
									<div class="grid grid-cols-2 gap-3 text-sm mb-3">
										<div>
											<span class="text-blue-700">Fields Retrieved:</span>
											<span class="font-semibold text-blue-900 ml-2">
												{analysisResult.data_quality.populated_fields}/{analysisResult.data_quality.total_fields}
											</span>
										</div>
										<div>
											<span class="text-blue-700">Source:</span>
											<span class="font-semibold text-blue-900 ml-2">{analysisResult.data_quality.data_source}</span>
										</div>
									</div>
									
									{#if analysisResult.data_quality.missing_fields.length > 0}
										<div class="bg-yellow-50 border border-yellow-200 rounded p-3 mt-3">
											<div class="text-xs font-semibold text-yellow-900 mb-1">
												⚠️ Missing Data ({analysisResult.data_quality.missing_fields.length} fields)
											</div>
											<div class="text-xs text-yellow-800">
												{analysisResult.data_quality.missing_fields.map(f => formatFieldName(f)).join(', ')}
											</div>
										</div>
									{/if}
									
									{#if analysisResult.data_quality.zero_value_fields.length > 0}
										<div class="bg-gray-50 border border-gray-200 rounded p-3 mt-2">
											<div class="text-xs font-semibold text-gray-700 mb-1">
												ℹ️ Zero/Not Applicable ({analysisResult.data_quality.zero_value_fields.length} fields)
											</div>
											<div class="text-xs text-gray-600">
												{analysisResult.data_quality.zero_value_fields.map(f => formatFieldName(f)).join(', ')}
											</div>
										</div>
									{/if}
								</div>
							{/if}
							
							<!-- Actual Data Used -->
							<div>
								<button
									onclick={() => showDataDetails = !showDataDetails}
									class="w-full text-left p-4 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 transition-colors"
								>
									<div class="flex items-center justify-between">
										<span class="text-sm font-semibold text-gray-900 flex items-center">
											<svg class="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
											</svg>
											Actual Metrics Used in Analysis
										</span>
										<svg class="w-5 h-5 text-gray-400 transition-transform {showDataDetails ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
										</svg>
									</div>
								</button>
								
								{#if showDataDetails && analysisResult.data_used}
									<div class="mt-3 bg-white rounded-lg border border-gray-200 p-4 max-h-96 overflow-y-auto">
										<div class="grid grid-cols-2 gap-3">
											{#each Object.entries(analysisResult.data_used) as [key, value]}
												{#if !['ticker', 'data_source', 'currency'].includes(key)}
													<div class="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
														<span class="text-xs font-medium text-gray-600">{formatFieldName(key)}:</span>
														<span class="text-xs font-mono {
															value === 0 || value === null ? 'text-gray-400' : 'text-gray-900 font-semibold'
														}">
															{value !== null && value !== undefined ? formatValue(value) : 'N/A'}
														</span>
													</div>
												{/if}
											{/each}
										</div>
									</div>
								{/if}
							</div>
						</div>
					{:else}
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
