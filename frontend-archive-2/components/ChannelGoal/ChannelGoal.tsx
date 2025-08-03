import React from 'react';
import styles from './ChannelGoal.module.css';

interface GoalData {
  id: string;
  title: string;
  icon: string;
  progress: number;
  current: string;
  remaining: string;
  total: string;
  gradient: 'views' | 'subscribers';
}

export interface ChannelGoalProps {
  className?: string;
  goals?: GoalData[];
  onAddGoal?: () => void;
}

const defaultGoals: GoalData[] = [
  {
    id: 'views',
    title: 'Views',
    icon: '👁️',
    progress: 75,
    current: '7.5k',
    remaining: '2.5k',
    total: '10k',
    gradient: 'views'
  },
  {
    id: 'subscribers',
    title: 'Subscribers',
    icon: '👤',
    progress: 75,
    current: '7.5k',
    remaining: '2.5k',
    total: '10k',
    gradient: 'subscribers'
  }
];

const CircularProgress: React.FC<{ progress: number }> = ({ progress }) => {
  const radius = 45;
  const strokeWidth = 8;
  const normalizedRadius = radius - strokeWidth * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDasharray = `${circumference} ${circumference}`;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className={styles.progressWrapper}>
      <svg
        height={radius * 2}
        width={radius * 2}
        className={styles.progressSvg}
      >
        <circle
          stroke="rgba(255, 255, 255, 0.2)"
          fill="transparent"
          strokeWidth={strokeWidth}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke="rgba(255, 255, 255, 0.9)"
          fill="transparent"
          strokeWidth={strokeWidth}
          strokeDasharray={strokeDasharray}
          style={{ strokeDashoffset }}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          className={styles.progressCircle}
        />
      </svg>
      <div className={styles.progressText}>
        {progress}%
      </div>
    </div>
  );
};

const GoalCard: React.FC<{ goal: GoalData }> = ({ goal }) => {
  return (
    <div className={`${styles.goalCard} ${styles[`gradient${goal.gradient.charAt(0).toUpperCase() + goal.gradient.slice(1)}`]}`}>
      <div className={styles.cardHeader}>
        <div className={styles.iconContainer}>
          <span className={styles.icon}>{goal.icon}</span>
        </div>
        <h3 className={styles.goalTitle}>{goal.title}</h3>
        <button className={styles.moreButton}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="3" cy="8" r="1.5" fill="currentColor"/>
            <circle cx="8" cy="8" r="1.5" fill="currentColor"/>
            <circle cx="13" cy="8" r="1.5" fill="currentColor"/>
          </svg>
        </button>
      </div>
      
      <div className={styles.progressSection}>
        <CircularProgress progress={goal.progress} />
      </div>
      
      <div className={styles.metricsSection}>
        <div className={styles.metric}>
          <div className={styles.metricValue}>{goal.current}</div>
          <div className={styles.metricLabel}>Current</div>
        </div>
        <div className={styles.metric}>
          <div className={styles.metricValue}>{goal.remaining}</div>
          <div className={styles.metricLabel}>Remaining</div>
        </div>
        <div className={styles.metric}>
          <div className={styles.metricValue}>{goal.total}</div>
          <div className={styles.metricLabel}>Total</div>
        </div>
      </div>
    </div>
  );
};

export const ChannelGoal: React.FC<ChannelGoalProps> = ({ 
  className, 
  goals = defaultGoals, 
  onAddGoal 
}) => {
  return (
    <div className={`${styles.container} ${className || ''}`}>
      <div className={styles.header}>
        <h2 className={styles.title}>Channel Goals</h2>
        <button className={styles.addButton} onClick={onAddGoal}>
          <span className={styles.plusIcon}>+</span>
          Add New Goal
        </button>
      </div>
      
      <div className={styles.goalsGrid}>
        {goals.map((goal) => (
          <GoalCard key={goal.id} goal={goal} />
        ))}
      </div>
    </div>
  );
};

export default ChannelGoal;