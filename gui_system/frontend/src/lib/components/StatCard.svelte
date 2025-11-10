<script lang="ts">
	/**
	 * Reusable stat card component
	 * Shows a metric with an icon and optional styling
	 */
	interface Props {
		title: string;
		value: number | string;
		icon?: 'users' | 'chart' | 'sparkles' | 'check';
		color?: 'primary' | 'green' | 'purple' | 'blue' | 'red';
	}

	let { title, value, icon = 'chart', color = 'primary' }: Props = $props();

	// Color mappings
	const colorClasses = {
		primary: 'bg-primary-100 text-primary-600',
		green: 'bg-green-100 text-green-600',
		purple: 'bg-purple-100 text-purple-600',
		blue: 'bg-blue-100 text-blue-600',
		red: 'bg-red-100 text-red-600'
	};

	// Icon paths
	const icons = {
		users: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
		chart: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
		sparkles: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z',
		check: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
	};
</script>

<div class="bg-white rounded-lg shadow p-6 border border-gray-200">
	<div class="flex items-center justify-between">
		<div>
			<p class="text-sm font-medium text-gray-600">{title}</p>
			<p class="text-3xl font-bold text-gray-900 mt-1">{value}</p>
		</div>
		<div class="w-12 h-12 {colorClasses[color]} rounded-lg flex items-center justify-center">
			<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={icons[icon]} />
			</svg>
		</div>
	</div>
</div>
