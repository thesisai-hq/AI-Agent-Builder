<script lang="ts">
	import type { Template } from '$lib/api';
	
	export let template: Template;
	export let onclick: () => void;
</script>

<button
	type="button"
	class="template-card"
	{onclick}
>
	<div class="flex items-start space-x-4">
		<!-- Icon -->
		<div class="icon-circle" style="background-color: {template.color}">
			<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
			</svg>
		</div>
		
		<!-- Content -->
		<div class="flex-1 text-left min-w-0">
			<div class="flex items-center space-x-2 mb-2">
				<h3 class="font-semibold text-gray-900 text-lg">{template.name}</h3>
				{#if template.type === 'rule_based'}
					<span class="badge bg-green-100 text-green-800">Rule-Based</span>
				{:else}
					<span class="badge bg-purple-100 text-purple-800">AI-Powered</span>
				{/if}
			</div>
			<p class="text-sm text-gray-600 mb-3">{template.description}</p>
			
			<!-- Quick Stats -->
			<div class="flex items-center space-x-4 text-xs text-gray-500">
				<div class="flex items-center">
					<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
					</svg>
					{template.rules.length} {template.rules.length === 1 ? 'rule' : 'rules'}
				</div>
				{#if template.category}
					<div class="flex items-center">
						<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
						</svg>
						{template.category}
					</div>
				{/if}
			</div>
		</div>
		
		<!-- Arrow -->
		<div class="flex-shrink-0">
			<svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</div>
	</div>
</button>

<style>
	.template-card {
		@apply w-full p-6 bg-white border-2 border-gray-200 rounded-lg;
		@apply hover:border-primary-300 hover:shadow-lg transition-all;
		@apply text-left;
	}
	
	.icon-circle {
		@apply w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0;
	}
	
	.badge {
		@apply px-2 py-1 text-xs font-medium rounded-full;
	}
</style>
