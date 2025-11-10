<script lang="ts">
	import { onMount } from 'svelte';
	import type { LLMConfig } from '$lib/api';
	
	// Svelte 5 runes mode - use $props() instead of export let
	let { 
		config,
		agentId = '',
		onchange
	}: {
		config: LLMConfig;
		agentId?: string;
		onchange: (config: LLMConfig) => void;
	} = $props();
	
	const availableTools = [
		{ 
			id: 'web_search', 
			name: 'Web Search', 
			description: 'Search for recent company news and developments', 
			icon: '🔍',
			color: 'blue'
		},
		{ 
			id: 'financial_data', 
			name: 'Financial Data', 
			description: 'Access detailed financial statements and metrics', 
			icon: '📊',
			color: 'green'
		},
		{ 
			id: 'document_analysis', 
			name: 'Document Analysis (RAG)', 
			description: 'Analyze your uploaded research documents', 
			icon: '📄',
			color: 'purple'
		},
		{ 
			id: 'calculator', 
			name: 'Financial Calculator', 
			description: 'Perform DCF, Graham Number, and other calculations', 
			icon: '🧮',
			color: 'orange'
		}
	];
	
	// Model options per provider
	const providerModels = {
		openai: [
			{ value: 'gpt-4', label: 'GPT-4' },
			{ value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
			{ value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' }
		],
		anthropic: [
			{ value: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
			{ value: 'claude-3-sonnet-20240229', label: 'Claude 3 Sonnet' },
			{ value: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku' }
		],
		cohere: [
			{ value: 'command', label: 'Command' },
			{ value: 'command-light', label: 'Command Light' }
		],
		ollama: [
			{ value: 'llama2', label: 'Llama 2' },
			{ value: 'llama2:13b', label: 'Llama 2 13B' },
			{ value: 'llama2:70b', label: 'Llama 2 70B' },
			{ value: 'mistral', label: 'Mistral 7B' },
			{ value: 'mixtral', label: 'Mixtral 8x7B' },
			{ value: 'codellama', label: 'Code Llama' },
			{ value: 'phi', label: 'Phi-2' },
			{ value: 'neural-chat', label: 'Neural Chat' }
		]
	};
	
	let uploadedDocs = $state<any[]>([]);
	let isUploading = $state(false);
	let uploadError = $state<string | null>(null);
	
	// Initialize ollama_base_url if not set
	$effect(() => {
		if (config.provider === 'ollama' && !config.ollama_base_url) {
			config.ollama_base_url = 'http://localhost:11434';
			onchange(config);
		}
	});
	
	function toggleTool(toolId: string) {
		const tools = config.tools || [];
		const index = tools.indexOf(toolId);
		
		if (index > -1) {
			tools.splice(index, 1);
		} else {
			tools.push(toolId);
		}
		
		config.tools = [...tools];
		onchange(config);
	}
	
	async function uploadDocument(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files || !input.files[0]) return;
		
		if (!agentId) {
			uploadError = "Agent must be created first before uploading documents";
			return;
		}
		
		isUploading = true;
		uploadError = null;
		
		const formData = new FormData();
		formData.append('file', input.files[0]);
		
		try {
			const response = await fetch(`http://localhost:8000/api/agents/${agentId}/documents`, {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				const error = await response.json();
				throw new Error(error.detail?.message || 'Upload failed');
			}
			
			const result = await response.json();
			console.log('Upload result:', result);
			
			// Reload documents list
			await loadDocuments();
			
			// Reset file input
			input.value = '';
			
		} catch (err) {
			console.error('Upload failed:', err);
			uploadError = err instanceof Error ? err.message : 'Upload failed';
		} finally {
			isUploading = false;
		}
	}
	
	async function loadDocuments() {
		if (!agentId) return;
		
		try {
			const response = await fetch(`http://localhost:8000/api/agents/${agentId}/documents`);
			if (response.ok) {
				const data = await response.json();
				uploadedDocs = data.documents || [];
			}
		} catch (err) {
			console.error('Failed to load documents:', err);
		}
	}
	
	async function deleteDoc(filename: string) {
		if (!confirm(`Delete ${filename}?`)) return;
		
		try {
			const response = await fetch(
				`http://localhost:8000/api/agents/${agentId}/documents/${filename}`,
				{ method: 'DELETE' }
			);
			
			if (response.ok) {
				await loadDocuments();
			}
		} catch (err) {
			console.error('Delete failed:', err);
		}
	}
	
	onMount(() => {
		if (agentId) {
			loadDocuments();
		}
	});
	
	// Get current provider's models
	$: currentModels = providerModels[config.provider as keyof typeof providerModels] || providerModels.openai;
</script>

<div class="space-y-6">
	<!-- Provider & Model -->
	<div class="grid grid-cols-2 gap-4">
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-2">LLM Provider</label>
			<select bind:value={config.provider} onchange={() => onchange(config)} class="input-field">
				<option value="openai">OpenAI</option>
				<option value="anthropic">Anthropic (Claude)</option>
				<option value="cohere">Cohere</option>
				<option value="ollama">Ollama (Local) 🏠</option>
			</select>
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-2">Model</label>
			<select bind:value={config.model} onchange={() => onchange(config)} class="input-field">
				{#each currentModels as modelOption}
					<option value={modelOption.value}>{modelOption.label}</option>
				{/each}
			</select>
		</div>
	</div>
	
	<!-- Ollama Base URL (only show for Ollama provider) -->
	{#if config.provider === 'ollama'}
		<div class="ollama-config">
			<div class="flex items-center mb-3">
				<span class="text-xl mr-2">🏠</span>
				<h3 class="font-semibold text-gray-900">Ollama Configuration</h3>
			</div>
			
			<div class="mb-3">
				<label class="block text-sm font-medium text-gray-700 mb-2">
					Ollama API URL
					<span class="text-xs font-normal text-gray-500 ml-2">(Default: http://localhost:11434)</span>
				</label>
				<input 
					type="text" 
					bind:value={config.ollama_base_url}
					oninput={() => onchange(config)}
					class="input-field font-mono text-sm"
					placeholder="http://localhost:11434"
				/>
			</div>
			
			<div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
				<p class="text-sm text-blue-800">
					<strong>💡 Using Ollama?</strong> Make sure Ollama is running locally:
				</p>
				<code class="text-xs bg-blue-100 px-2 py-1 rounded mt-2 inline-block">ollama serve</code>
				<p class="text-xs text-blue-700 mt-2">
					Install models: <code class="bg-blue-100 px-1 rounded">ollama pull llama2</code>
				</p>
			</div>
		</div>
	{/if}
	
	<!-- API Key Notice -->
	{#if config.provider !== 'ollama'}
		<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
			<p class="text-sm text-yellow-800">
				⚠️ <strong>API Key Required:</strong> Make sure to set your {config.provider.toUpperCase()} API key in the environment:
			</p>
			<code class="text-xs bg-yellow-100 px-2 py-1 rounded mt-1 inline-block">
				{config.provider === 'openai' ? 'OPENAI_API_KEY' : 
				 config.provider === 'anthropic' ? 'ANTHROPIC_API_KEY' : 
				 'COHERE_API_KEY'}=your_key_here
			</code>
		</div>
	{:else}
		<div class="bg-green-50 border border-green-200 rounded-lg p-3">
			<p class="text-sm text-green-800">
				✅ <strong>No API Key Needed:</strong> Ollama runs locally on your machine. Free and private!
			</p>
		</div>
	{/if}
	
	<!-- Temperature & Tokens -->
	<div class="grid grid-cols-2 gap-4">
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-2">
				Temperature: {config.temperature.toFixed(1)}
			</label>
			<input 
				type="range" 
				min="0" 
				max="2" 
				step="0.1" 
				bind:value={config.temperature}
				oninput={() => onchange(config)}
				class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
			/>
			<div class="flex justify-between text-xs text-gray-500 mt-1">
				<span>Focused</span>
				<span>Balanced</span>
				<span>Creative</span>
			</div>
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-2">Max Tokens</label>
			<input 
				type="number" 
				bind:value={config.max_tokens}
				oninput={() => onchange(config)}
				min="100"
				max="8000"
				class="input-field"
			/>
		</div>
	</div>
	
	<!-- Tools Selection -->
	<div>
		<label class="block text-sm font-medium text-gray-700 mb-3">
			Enable Tools
			<span class="text-xs font-normal text-gray-500 ml-2">(Select tools the AI can use)</span>
		</label>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
			{#each availableTools as tool}
				<button
					type="button"
					class="tool-card"
					class:selected={config.tools?.includes(tool.id)}
					onclick={() => toggleTool(tool.id)}
				>
					<div class="flex items-start space-x-3">
						<span class="text-2xl flex-shrink-0">{tool.icon}</span>
						<div class="flex-1 text-left min-w-0">
							<div class="font-semibold text-gray-900 truncate">{tool.name}</div>
							<div class="text-xs text-gray-600 mt-0.5">{tool.description}</div>
						</div>
						{#if config.tools?.includes(tool.id)}
							<svg class="w-5 h-5 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						{/if}
					</div>
				</button>
			{/each}
		</div>
	</div>
	
	<!-- Document Upload (RAG) - Only show if document_analysis tool is enabled -->
	{#if config.tools?.includes('document_analysis')}
		<div class="rag-section">
			<div class="flex items-center mb-3">
				<span class="text-xl mr-2">📚</span>
				<h3 class="font-semibold text-gray-900">Knowledge Base (RAG)</h3>
			</div>
			
			{#if !agentId}
				<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
					<p class="text-sm text-yellow-800">
						💡 Documents can be uploaded after creating the agent. 
						Save this agent first, then edit it to add documents.
					</p>
				</div>
			{:else}
				<p class="text-sm text-gray-600 mb-4">
					Upload PDFs or text files that the AI should reference during analysis.
					Documents will be embedded and searchable.
				</p>
				
				<!-- Upload Error -->
				{#if uploadError}
					<div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
						<p class="text-sm text-red-800">{uploadError}</p>
					</div>
				{/if}
				
				<!-- Upload Area -->
				<div class="upload-area">
					<input 
						type="file" 
						id="doc-upload" 
						accept=".pdf,.txt"
						onchange={uploadDocument}
						disabled={isUploading}
						class="hidden"
					/>
					<label for="doc-upload" class="upload-label">
						{#if isUploading}
							<div class="flex flex-col items-center">
								<svg class="animate-spin h-8 w-8 text-blue-600 mb-2" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
								<span class="text-sm text-gray-600">Processing document...</span>
							</div>
						{:else}
							<svg class="w-10 h-10 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
							</svg>
							<span class="text-sm font-medium text-gray-700">Click to upload or drag files here</span>
							<span class="text-xs text-gray-500 mt-1">PDF, TXT (max 10MB)</span>
						{/if}
					</label>
				</div>
				
				<!-- Uploaded Documents List -->
				{#if uploadedDocs.length > 0}
					<div class="mt-4 space-y-2">
						<p class="text-sm font-medium text-gray-700">Uploaded Documents ({uploadedDocs.length})</p>
						{#each uploadedDocs as doc}
							<div class="doc-item">
								<div class="flex items-center space-x-2 flex-1 min-w-0">
									<span>📄</span>
									<span class="text-sm text-gray-900 truncate">{doc.filename}</span>
									<span class="text-xs text-gray-500">({doc.size_mb.toFixed(2)} MB)</span>
								</div>
								<button 
									class="text-red-600 hover:text-red-800 text-sm font-medium transition-colors"
									onclick={() => deleteDoc(doc.filename)}
								>
									Delete
								</button>
							</div>
						{/each}
					</div>
				{/if}
			{/if}
		</div>
	{/if}
	
	<!-- System Prompt -->
	<div>
		<label class="block text-sm font-medium text-gray-700 mb-2">
			System Prompt (Optional)
			<span class="text-xs font-normal text-gray-500 ml-2">Custom instructions for the AI</span>
		</label>
		<textarea 
			bind:value={config.system_prompt}
			oninput={() => onchange(config)}
			class="input-field"
			rows="5"
			placeholder="You are a conservative value investor focusing on companies with strong fundamentals..."
		></textarea>
		<p class="text-xs text-gray-500 mt-1">
			Leave empty to use default prompt based on your investment goal
		</p>
	</div>
	
	<!-- Tool Descriptions Help -->
	<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
		<div class="flex">
			<svg class="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
			<div class="text-sm text-blue-800">
				<p class="font-medium mb-1">About Tools</p>
				<p>
					Tools give your AI agent additional capabilities. Enable only the tools you need.
					The AI will automatically use them when analyzing stocks.
				</p>
			</div>
		</div>
	</div>
</div>

<style>
	.input-field {
		@apply w-full px-4 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
		@apply transition-all;
	}
	
	.tool-card {
		@apply p-4 border-2 border-gray-200 rounded-lg transition-all;
		@apply hover:border-blue-300 hover:shadow-sm;
		@apply text-left w-full;
	}
	
	.tool-card.selected {
		@apply border-blue-500 bg-blue-50 shadow-sm;
	}
	
	.rag-section {
		@apply p-6 bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg border-2 border-purple-200;
	}
	
	.ollama-config {
		@apply p-6 bg-gradient-to-br from-green-50 to-teal-50 rounded-lg border-2 border-green-200;
	}
	
	.upload-area {
		@apply border-2 border-dashed border-gray-300 rounded-lg p-8;
		@apply hover:border-blue-400 hover:bg-blue-50 transition-all;
		@apply cursor-pointer;
	}
	
	.upload-label {
		@apply flex flex-col items-center justify-center cursor-pointer;
	}
	
	.doc-item {
		@apply flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200;
		@apply hover:border-gray-300 transition-colors;
	}
</style>
