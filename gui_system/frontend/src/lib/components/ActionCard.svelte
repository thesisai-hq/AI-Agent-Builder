<script lang="ts">
	/**
	 * Reusable action card component
	 * Interactive card for navigation or actions
	 */
	interface Props {
		href?: string;
		title: string;
		description: string;
		gradient?: 'primary' | 'gray' | 'green' | 'purple';
		onclick?: () => void;
	}

	let { href, title, description, gradient = 'primary', onclick }: Props = $props();

	// Gradient mappings
	const gradients = {
		primary: 'from-primary-500 to-primary-600',
		gray: 'from-gray-700 to-gray-800',
		green: 'from-green-500 to-green-600',
		purple: 'from-purple-500 to-purple-600'
	};

	const textColors = {
		primary: 'text-primary-100',
		gray: 'text-gray-300',
		green: 'text-green-100',
		purple: 'text-purple-100'
	};
</script>

{#if href}
	<a
		{href}
		class="bg-gradient-to-br {gradients[gradient]} rounded-xl p-8 text-white hover:shadow-xl transition-all duration-200 group block"
		onclick={onclick}
	>
		<div class="flex items-center justify-between mb-4">
			<h2 class="text-2xl font-bold">{title}</h2>
			<svg
				class="w-8 h-8 group-hover:translate-x-1 transition-transform"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</div>
		<p class="{textColors[gradient]}">{description}</p>
	</a>
{:else}
	<button
		type="button"
		class="w-full bg-gradient-to-br {gradients[gradient]} rounded-xl p-8 text-white hover:shadow-xl transition-all duration-200 group text-left"
		onclick={onclick}
	>
		<div class="flex items-center justify-between mb-4">
			<h2 class="text-2xl font-bold">{title}</h2>
			<svg
				class="w-8 h-8 group-hover:translate-x-1 transition-transform"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</div>
		<p class="{textColors[gradient]}">{description}</p>
	</button>
{/if}
