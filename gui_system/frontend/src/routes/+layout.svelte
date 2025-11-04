<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	
	let { children } = $props();
</script>

<div class="min-h-screen flex flex-col">
	<!-- Header -->
	<header class="bg-white border-b border-gray-200">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center h-16">
				<!-- Logo -->
				<div class="flex items-center">
					<a href="/" class="flex items-center space-x-2">
						<div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
							<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
							</svg>
						</div>
						<span class="text-xl font-bold text-gray-900">AI Agent Builder</span>
					</a>
				</div>

				<!-- Navigation -->
				<nav class="hidden md:flex space-x-8">
					<a 
						href="/" 
						class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors"
						class:text-primary-600={$page.url.pathname === '/'}
						class:font-semibold={$page.url.pathname === '/'}
					>
						Home
					</a>
					<a 
						href="/agents" 
						class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors"
						class:text-primary-600={$page.url.pathname.startsWith('/agents')}
						class:font-semibold={$page.url.pathname.startsWith('/agents')}
					>
						My Agents
					</a>
					<a 
						href="/create" 
						class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors"
						class:text-primary-600={$page.url.pathname === '/create'}
						class:font-semibold={$page.url.pathname === '/create'}
					>
						Create
					</a>
				</nav>

				<!-- Actions -->
				<div class="flex items-center space-x-4">
					<a
						href="/create"
						class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
					>
						<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
						</svg>
						New Agent
					</a>
				</div>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="flex-1">
		{@render children()}
	</main>

	<!-- Footer -->
	<footer class="bg-white border-t border-gray-200 mt-auto">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
			<div class="text-center text-sm text-gray-500">
				<p>AI Agent Builder - Build intelligent investment agents with ease</p>
				<p class="mt-1">
					<a href="http://localhost:8000/docs" target="_blank" class="text-primary-600 hover:text-primary-700">
						API Documentation
					</a>
				</p>
			</div>
		</div>
	</footer>
</div>
