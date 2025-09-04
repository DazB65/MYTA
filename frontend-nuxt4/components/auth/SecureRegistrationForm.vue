<template>
  <div class="registration-form">
    <h2>Create Your Account</h2>
    <p class="subtitle">Join Vidalytics to optimize your YouTube channel</p>
    
    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <VInput
          v-model="form.name"
          label="Full Name"
          type="text"
          placeholder="Enter your full name"
          required
          :error="errors.name"
        />
      </div>
      
      <div class="form-group">
        <VInput
          v-model="form.email"
          label="Email Address"
          type="email"
          placeholder="Enter your email"
          required
          :error="errors.email"
        />
      </div>
      
      <div class="form-group">
        <VInput
          v-model="form.password"
          label="Password"
          type="password"
          placeholder="Create a strong password"
          required
          :error="errors.password"
          :hint="passwordHint"
        />
      </div>
      
      <div class="form-group">
        <VInput
          v-model="form.confirmPassword"
          label="Confirm Password"
          type="password"
          placeholder="Confirm your password"
          required
          :error="errors.confirmPassword"
        />
      </div>
      
      <div class="password-strength">
        <div class="strength-meter">
          <div 
            class="strength-bar" 
            :class="passwordStrength.class"
            :style="{ width: passwordStrength.width }"
          ></div>
        </div>
        <span class="strength-text">{{ passwordStrength.text }}</span>
      </div>
      
      <VButton
        type="submit"
        :loading="loading"
        :disabled="!isFormValid"
        class="submit-button"
      >
        Create Account
      </VButton>
      
      <p class="login-link">
        Already have an account? 
        <NuxtLink to="/login" class="link">Sign in</NuxtLink>
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface RegistrationForm {
  name: string
  email: string
  password: string
  confirmPassword: string
}

const form = ref<RegistrationForm>({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = ref<Partial<RegistrationForm>>({})
const loading = ref(false)

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.value.password
  if (!password) return { width: '0%', class: '', text: '' }
  
  let score = 0
  let feedback = []
  
  // Length check
  if (password.length >= 8) score += 1
  else feedback.push('at least 8 characters')
  
  // Uppercase check
  if (/[A-Z]/.test(password)) score += 1
  else feedback.push('uppercase letter')
  
  // Lowercase check
  if (/[a-z]/.test(password)) score += 1
  else feedback.push('lowercase letter')
  
  // Number check
  if (/\d/.test(password)) score += 1
  else feedback.push('number')
  
  // Special character check
  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) score += 1
  else feedback.push('special character')
  
  const strength = {
    0: { width: '0%', class: '', text: '' },
    1: { width: '20%', class: 'very-weak', text: 'Very Weak' },
    2: { width: '40%', class: 'weak', text: 'Weak' },
    3: { width: '60%', class: 'fair', text: 'Fair' },
    4: { width: '80%', class: 'good', text: 'Good' },
    5: { width: '100%', class: 'strong', text: 'Strong' }
  }
  
  return strength[score as keyof typeof strength]
})

const passwordHint = computed(() => {
  if (!form.value.password) return 'Password must contain uppercase, lowercase, number, and special character'
  if (passwordStrength.value.class === 'strong') return 'Strong password!'
  return 'Password could be stronger'
})

// Form validation
const isFormValid = computed(() => {
  return form.value.name.length >= 2 &&
         form.value.email.includes('@') &&
         form.value.password.length >= 8 &&
         form.value.password === form.value.confirmPassword &&
         passwordStrength.value.class !== 'very-weak'
})

// Real-time validation
watch(() => form.value.email, (email) => {
  if (email && !email.includes('@')) {
    errors.value.email = 'Please enter a valid email address'
  } else {
    delete errors.value.email
  }
})

watch(() => form.value.confirmPassword, (confirmPassword) => {
  if (confirmPassword && confirmPassword !== form.value.password) {
    errors.value.confirmPassword = 'Passwords do not match'
  } else {
    delete errors.value.confirmPassword
  }
})

watch(() => form.value.password, (password) => {
  if (password && password.length < 8) {
    errors.value.password = 'Password must be at least 8 characters long'
  } else {
    delete errors.value.password
  }
  
  // Revalidate confirm password
  if (form.value.confirmPassword && form.value.confirmPassword !== password) {
    errors.value.confirmPassword = 'Passwords do not match'
  } else {
    delete errors.value.confirmPassword
  }
})

const handleSubmit = async () => {
  loading.value = true
  errors.value = {}
  
  try {
    const { $api } = useNuxtApp()
    
    const response = await $api('/api/auth/register', {
      method: 'POST',
      body: {
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        confirm_password: form.value.confirmPassword
      }
    })
    
    if (response.status === 'success') {
      // Registration successful, redirect to dashboard
      await navigateTo('/dashboard')
    } else {
      // Handle registration errors
      if (response.error) {
        errors.value.email = response.error
      }
    }
  } catch (error: any) {
    console.error('Registration failed:', error)
    errors.value.email = error.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.registration-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}

.registration-form h2 {
  text-align: center;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
}

.subtitle {
  text-align: center;
  color: var(--color-text-muted);
  margin-bottom: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.password-strength {
  margin-top: -1rem;
  margin-bottom: 0.5rem;
}

.strength-meter {
  width: 100%;
  height: 4px;
  background: var(--color-border);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.strength-bar {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.strength-bar.very-weak { background-color: #ef4444; }
.strength-bar.weak { background-color: #f97316; }
.strength-bar.fair { background-color: #eab308; }
.strength-bar.good { background-color: #22c55e; }
.strength-bar.strong { background-color: #16a34a; }

.strength-text {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.submit-button {
  width: 100%;
  margin-top: 1rem;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: var(--color-text-muted);
}

.link {
  color: var(--color-brand-primary);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
