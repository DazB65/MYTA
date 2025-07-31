import type { Meta, StoryObj } from '@storybook/react';
import { ChannelGoal } from './ChannelGoal';

const meta = {
  title: 'Dashboard/ChannelGoal',
  component: ChannelGoal,
  parameters: {
    layout: 'fullscreen',
    backgrounds: {
      default: 'dark',
      values: [
        {
          name: 'dark',
          value: '#1a1a2e',
        },
        {
          name: 'light',
          value: '#ffffff',
        },
      ],
    },
  },
  tags: ['autodocs'],
  argTypes: {
    className: {
      control: 'text',
      description: 'Additional CSS classes to apply to the component',
    },
    goals: {
      control: 'object',
      description: 'Array of goal data to display',
    },
    onAddGoal: {
      action: 'onAddGoal',
      description: 'Callback function when Add New Goal button is clicked',
    },
  },
} satisfies Meta<typeof ChannelGoal>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default story with both goals
export const Default: Story = {
  args: {
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};

// Story with only Views goal
export const ViewsOnly: Story = {
  args: {
    goals: [
      {
        id: 'views',
        title: 'Views',
        icon: '👁️',
        progress: 75,
        current: '7.5k',
        remaining: '2.5k',
        total: '10k',
        gradient: 'views' as const,
      },
    ],
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};

// Story with only Subscribers goal
export const SubscribersOnly: Story = {
  args: {
    goals: [
      {
        id: 'subscribers',
        title: 'Subscribers',
        icon: '👤',
        progress: 75,
        current: '7.5k',
        remaining: '2.5k',
        total: '10k',
        gradient: 'subscribers' as const,
      },
    ],
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};

// Story with different progress values
export const DifferentProgress: Story = {
  args: {
    goals: [
      {
        id: 'views',
        title: 'Views',
        icon: '👁️',
        progress: 45,
        current: '4.5k',
        remaining: '5.5k',
        total: '10k',
        gradient: 'views' as const,
      },
      {
        id: 'subscribers',
        title: 'Subscribers',
        icon: '👤',
        progress: 90,
        current: '9k',
        remaining: '1k',
        total: '10k',
        gradient: 'subscribers' as const,
      },
    ],
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};

// Story with no goals (empty state)
export const EmptyState: Story = {
  args: {
    goals: [],
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};

// Story with custom class
export const WithCustomClass: Story = {
  args: {
    className: 'custom-spacing',
    onAddGoal: () => console.log('Add new goal clicked'),
  },
};