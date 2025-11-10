<script lang="ts">
	import type { Rule, RuleCondition, RuleAction } from '$lib/api';
	
	// Svelte 5 runes mode - use $props() instead of export let
	let {
		rules,
		onchange
	}: {
		rules: Rule[];
		onchange: (rules: Rule[]) => void;
	} = $props();
	
	const indicators = [
		{ value: 'pe_ratio', label: 'P/E Ratio' },
		{ value: 'pb_ratio', label: 'P/B Ratio' },
		{ value: 'peg_ratio', label: 'PEG Ratio' },
		{ value: 'dividend_yield', label: 'Dividend Yield (%)' },
		{ value: 'roe', label: 'ROE (%)' },
		{ value: 'roa', label: 'ROA (%)' },
		{ value: 'profit_margin', label: 'Profit Margin (%)' },
		{ value: 'revenue_growth', label: 'Revenue Growth (%)' },
		{ value: 'earnings_growth', label: 'Earnings Growth (%)' },
		{ value: 'debt_to_equity', label: 'Debt to Equity' },
		{ value: 'current_ratio', label: 'Current Ratio' },
		{ value: 'quick_ratio', label: 'Quick Ratio' },
	];
	
	const operators = [
		{ value: '<', label: 'Less than (<)' },
		{ value: '<=', label: 'Less than or equal (≤)' },
		{ value: '>', label: 'Greater than (>)' },
		{ value: '>=', label: 'Greater than or equal (≥)' },
		{ value: '=', label: 'Equal to (=)' },
	];
	
	const actions = [
		{ value: 'bullish', label: 'Bullish (Buy Signal)', color: 'green' },
		{ value: 'bearish', label: 'Bearish (Sell Signal)', color: 'red' },
		{ value: 'neutral', label: 'Neutral (Hold)', color: 'gray' },
	];
	
	function addRule() {
		const newRule: Rule = {
			conditions: [{
				type: 'simple',
				indicator: 'pe_ratio',
				operator: '<',
				value: 15
			}],
			action: {
				action: 'bullish',
				size: 10,
				parameters: {}
			},
			description: ''
		};
		
		rules = [...rules, newRule];
		onchange(rules);
	}
	
	function removeRule(index: number) {
		rules = rules.filter((_, i) => i !== index);
		onchange(rules);
	}
	
	function addCondition(ruleIndex: number) {
		const condition: RuleCondition = {
			type: 'simple',
			indicator: 'pe_ratio',
			operator: '<',
			value: 15
		};
		
		rules[ruleIndex].conditions = [...rules[ruleIndex].conditions, condition];
		onchange(rules);
	}
	
	function removeCondition(ruleIndex: number, condIndex: number) {
		rules[ruleIndex].conditions = rules[ruleIndex].conditions.filter((_, i) => i !== condIndex);
		onchange(rules);
	}
	
	function updateRule(index: number, updates: Partial<Rule>) {
		rules[index] = { ...rules[index], ...updates };
		onchange(rules);
	}
	
	function updateCondition(ruleIndex: number, condIndex: number, updates: Partial<RuleCondition>) {
		rules[ruleIndex].conditions[condIndex] = {
			...rules[ruleIndex].conditions[condIndex],
			...updates
		};
		onchange(rules);
	}
	
	function updateAction(ruleIndex: number, updates: Partial<RuleAction>) {
		rules[ruleIndex].action = {
			...rules[ruleIndex].action,
			...updates
		};
		onchange(rules);
	}
</script>

<div class="space-y-6">
	<!-- Add Rule Button -->
	<button
		type="button"
		class="btn-add-rule"
		onclick={addRule}
	>
		<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
		</svg>
		Add Rule
	</button>
	
	<!-- Rules List -->
	{#if rules.length === 0}
		<div class="empty-state">
			<svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
			</svg>
			<p class="text-gray-600">No rules yet. Click "Add Rule" to get started.</p>
		</div>
	{:else}
		<div class="space-y-4">
			{#each rules as rule, ruleIndex}
				<div class="rule-card">
					<!-- Rule Header -->
					<div class="rule-header">
						<h4 class="rule-title">Rule {ruleIndex + 1}</h4>
						<button
							type="button"
							class="btn-remove"
							onclick={() => removeRule(ruleIndex)}
						>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
							</svg>
						</button>
					</div>
					
					<!-- Rule Description -->
					<div class="mb-4">
						<label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
						<input
							type="text"
							class="input-field"
							bind:value={rule.description}
							oninput={() => onchange(rules)}
							placeholder="e.g., Buy undervalued stocks with low P/E"
						/>
					</div>
					
					<!-- Conditions -->
					<div class="mb-4">
						<div class="flex items-center justify-between mb-3">
							<label class="text-sm font-medium text-gray-700">
								Conditions (ALL must be met)
							</label>
							<button
								type="button"
								class="btn-add-condition"
								onclick={() => addCondition(ruleIndex)}
							>
								<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
								</svg>
								Add Condition
							</button>
						</div>
						
						<div class="space-y-2">
							{#each rule.conditions as condition, condIndex}
								<div class="condition-row">
									<select
										class="condition-select"
										bind:value={condition.indicator}
										onchange={() => onchange(rules)}
									>
										{#each indicators as indicator}
											<option value={indicator.value}>{indicator.label}</option>
										{/each}
									</select>
									
									<select
										class="condition-select"
										bind:value={condition.operator}
										onchange={() => onchange(rules)}
									>
										{#each operators as operator}
											<option value={operator.value}>{operator.label}</option>
										{/each}
									</select>
									
									<input
										type="number"
										class="condition-input"
										bind:value={condition.value}
										oninput={() => onchange(rules)}
										step="0.01"
										placeholder="Value"
									/>
									
									<button
										type="button"
										class="btn-remove-small"
										onclick={() => removeCondition(ruleIndex, condIndex)}
									>
										<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
										</svg>
									</button>
								</div>
							{/each}
						</div>
					</div>
					
					<!-- Action -->
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-3">Then take action:</label>
						<div class="grid grid-cols-2 gap-4">
							<div>
								<label class="block text-xs text-gray-600 mb-1">Signal</label>
								<select
									class="input-field"
									bind:value={rule.action.action}
									onchange={() => onchange(rules)}
								>
									{#each actions as action}
										<option value={action.value}>{action.label}</option>
									{/each}
								</select>
							</div>
							<div>
								<label class="block text-xs text-gray-600 mb-1">
									Position Size (% of portfolio)
								</label>
								<input
									type="number"
									class="input-field"
									bind:value={rule.action.size}
									oninput={() => onchange(rules)}
									min="0"
									max="100"
									step="1"
								/>
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
	
	<!-- Help Text -->
	{#if rules.length > 0}
		<div class="bg-green-50 border border-green-200 rounded-lg p-4">
			<p class="text-sm text-green-800">
				💡 <strong>Tip:</strong> Rules are evaluated in order. The first matching rule will be used.
				Make sure to order your rules from most specific to most general.
			</p>
		</div>
	{/if}
</div>

<style>
	.btn-add-rule {
		@apply w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg;
		@apply text-gray-700 font-medium;
		@apply hover:border-primary-400 hover:bg-primary-50 hover:text-primary-700;
		@apply transition-all flex items-center justify-center;
	}
	
	.empty-state {
		@apply flex flex-col items-center justify-center py-12 text-center;
	}
	
	.rule-card {
		@apply p-6 bg-white border-2 border-gray-200 rounded-lg;
		@apply hover:border-gray-300 transition-colors;
	}
	
	.rule-header {
		@apply flex items-center justify-between mb-4;
	}
	
	.rule-title {
		@apply text-lg font-semibold text-gray-900;
	}
	
	.btn-remove {
		@apply text-red-600 hover:text-red-800 hover:bg-red-50 p-2 rounded transition-colors;
	}
	
	.btn-add-condition {
		@apply text-sm text-primary-600 hover:text-primary-800 font-medium;
		@apply flex items-center;
	}
	
	.condition-row {
		@apply flex items-center space-x-2;
	}
	
	.condition-select {
		@apply flex-1 px-3 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
		@apply text-sm;
	}
	
	.condition-input {
		@apply w-24 px-3 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
		@apply text-sm;
	}
	
	.btn-remove-small {
		@apply text-gray-400 hover:text-red-600 hover:bg-red-50 p-2 rounded transition-colors;
	}
	
	.input-field {
		@apply w-full px-4 py-2 border border-gray-300 rounded-lg;
		@apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
		@apply transition-all;
	}
</style>
