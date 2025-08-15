// Utility types for better type safety and developer experience

// Make all properties optional recursively
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Make specific properties required
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>

// Make specific properties optional
export type OptionalFields<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

// Extract function return type
export type ReturnTypeOf<T> = T extends (...args: any[]) => infer R ? R : never

// Extract array element type
export type ArrayElement<T> = T extends (infer U)[] ? U : never

// Create a union of all values in an object
export type ValueOf<T> = T[keyof T]

// Create a union of all keys in an object as strings
export type KeysOf<T> = Extract<keyof T, string>

// Exclude null and undefined
export type NonNullable<T> = T extends null | undefined ? never : T

// Create a type that requires at least one property
export type AtLeastOne<T, U = { [K in keyof T]: Pick<T, K> }> = Partial<T> & U[keyof U]

// Create a type for async function states
export type AsyncState<T, E = Error> = {
  data: T | null
  loading: boolean
  error: E | null
}

// Create a type for form validation
export type ValidationResult = {
  valid: boolean
  errors: string[]
}

// Create a type for API endpoints
export type ApiEndpoint<TRequest = any, TResponse = any> = {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  url: string
  request?: TRequest
  response: TResponse
}

// Create a type for component events
export type ComponentEvents<T> = {
  [K in keyof T]: T[K] extends (...args: any[]) => any ? Parameters<T[K]> : never
}

// Create a type for store getters
export type StoreGetters<T> = {
  readonly [K in keyof T]: T[K] extends (...args: any[]) => any ? ReturnType<T[K]> : T[K]
}

// Create a type for reactive refs
export type ReactiveRefs<T> = {
  [K in keyof T]: Ref<T[K]>
}

// Create a type for computed properties
export type ComputedRefs<T> = {
  readonly [K in keyof T]: ComputedRef<T[K]>
}

// Create a type for Pinia store composition
export type StoreComposition<TState, TGetters, TActions> = {
  // State (reactive refs)
  [K in keyof TState]: Ref<TState[K]>
} & {
  // Getters (computed refs)
  readonly [K in keyof TGetters]: ComputedRef<TGetters[K]>
} & {
  // Actions (functions)
  [K in keyof TActions]: TActions[K]
}

// Create a type for component props with defaults
export type PropsWithDefaults<T, D> = T & {
  [K in keyof D]: K extends keyof T ? NonNullable<T[K]> : D[K]
}

// Create a type for event handlers
export type EventHandler<T = Event> = (event: T) => void | Promise<void>

// Create a type for async data fetching
export type AsyncData<T> = {
  data: Ref<T | null>
  pending: Ref<boolean>
  error: Ref<Error | null>
  refresh: () => Promise<void>
}

// Create a type for form field validation
export type FieldValidator<T = any> = (value: T) => ValidationResult | Promise<ValidationResult>

// Create a type for route parameters
export type RouteParams<T extends string> = T extends `${infer _Start}:${infer Param}/${infer Rest}`
  ? { [K in Param]: string } & RouteParams<Rest>
  : T extends `${infer _Start}:${infer Param}`
    ? { [K in Param]: string }
    : {}

// Create a type for theme configuration
export type ThemeConfig<T> = {
  [K in keyof T]: T[K] extends object ? ThemeConfig<T[K]> : string | number
}

// Create a type for responsive values
export type ResponsiveValue<T> =
  | T
  | {
      xs?: T
      sm?: T
      md?: T
      lg?: T
      xl?: T
    }

// Create a type for animation configuration
export type AnimationConfig = {
  duration?: number
  easing?: string
  delay?: number
  iterations?: number | 'infinite'
  direction?: 'normal' | 'reverse' | 'alternate' | 'alternate-reverse'
  fillMode?: 'none' | 'forwards' | 'backwards' | 'both'
}

// Create a type for color variants
export type ColorVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info'

// Create a type for size variants
export type SizeVariant = 'xs' | 'sm' | 'md' | 'lg' | 'xl'

// Create a type for component variants
export type ComponentVariant = 'filled' | 'outlined' | 'text' | 'ghost'
