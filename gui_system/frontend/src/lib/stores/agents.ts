/**
 * Svelte stores for agent and template management
 */

import { writable } from 'svelte/store';
import type { Agent, Template } from '$lib/api';

// Agent store
export const agents = writable<Agent[]>([]);

// Template store
export const templates = writable<Template[]>([]);

// Loading state
export const loading = writable(false);

// Error state
export const error = writable<string | null>(null);

// Selected agent for editing
export const selectedAgent = writable<Agent | null>(null);
