<script setup>
import { ref } from 'vue'

const goals = ref([
  { id: 1, type: 'pink', percentage: 75, value: '7.5K', target: 'from 10k' },
  { id: 2, type: 'blue', percentage: 75, value: '7.5K', target: 'from 10k' },
])
</script>

<template>
  <div class="goals-container">
    <div class="card-header">
      <h2 class="card-title">Channel Goals</h2>
      <button class="options-btn">
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="10" cy="5" r="1.5" fill="#6E6E6E" />
          <circle cx="10" cy="10" r="1.5" fill="#6E6E6E" />
          <circle cx="10" cy="15" r="1.5" fill="#6E6E6E" />
        </svg>
      </button>
    </div>

    <div v-for="goal in goals" :key="goal.id" class="goal-card" :class="`goal-card-${goal.type}`">
      <div class="donut-chart-wrapper">
        <IconDonut :percentage="goal.percentage" :type="goal.type" />
        <span>{{ goal.percentage }}%</span>
      </div>
      <div class="goal-info">
        <div class="goal-value">{{ goal.value }}</div>
        <div class="goal-target">{{ goal.target }}</div>
      </div>
    </div>

    <button class="quick-statistic">Quick Statistic</button>
  </div>
</template>

<style scoped>
.goals-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-24);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 8px; /* Added padding to align with cards */
}
.card-title {
  font-size: 18px;
  font-weight: 600;
}
.options-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.goal-card {
  border-radius: 12px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.goal-card-pink {
  background: var(--gradient-pink);
}
.goal-card-blue {
  background: var(--gradient-blue);
}

.donut-chart-wrapper {
  position: relative;
  display: grid;
  place-items: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
}
/* This assumes your IconDonut component creates the visual chart */
.donut-chart-wrapper > span {
  position: absolute; /* Puts the text on top of the icon */
}

.goal-info {
  text-align: right;
}
.goal-value {
  font-size: 18px;
  font-weight: 700;
}
.goal-target {
  font-size: 12px;
  font-weight: 500;
  opacity: 0.8;
}

.quick-statistic {
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  text-decoration: underline;
  display: block;
  margin: 0 auto;
  font-size: 14px;
  cursor: pointer;
}
</style>
