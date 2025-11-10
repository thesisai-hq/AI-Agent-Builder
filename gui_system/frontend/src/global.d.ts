// Global runes helper declarations to satisfy TypeScript and Svelte in runes mode
// These helpers are provided by the runes compilation/runtime. Declaring them
// here prevents per-file duplication and avoids ordering/visibility issues.

declare function $props<T = any>(): T;
// `$state` is used in some components as a runes helper to create reactive
// stateful values. We declare it as any to keep the type checks happy.
declare function $state<T = any>(initial?: T): any;
