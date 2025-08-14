import { TaskPriority, ContentStatus, PillarCategory } from '../enums';

// Props types (data passed to components)
export interface TaskProps {
  id: number;
  title: string;
  description: string;
  priority: TaskPriority;
  tags: string[];
  dueDate: string;
  completed: boolean;
}

export interface ContentItemProps {
  id: number;
  title: string;
  description: string;
  status: ContentStatus;
  priority: TaskPriority;
  assignee: string;
  progress?: number;
  metrics?: {
    views: string;
    engagement: number;
    likes: string;
    shares: string;
  };
  createdAt: string;
}

export interface PillarProps {
  id: number;
  name: string;
  category: PillarCategory;
  videoCount: number;
  createdMonthsAgo: number;
  revenue: number;
  revenueChange: number;
  watchTime: number;
  watchTimeChange: number;
  subscribers: number;
  subscriberChange: number;
  color: string;
}

export interface UserProfileProps {
  name: string;
  initial: string;
  greeting: string;
  currentDate: string;
}

export interface ChannelGoalsProps {
  views: {
    completed: number;
    remaining: number;
    total: number;
    percentage: number;
  };
  subscribers: {
    completed: number;
    remaining: number;
    total: number;
    percentage: number;
  };
}

export interface CreateProfileFormProps {
  motivation: string;
  niche: string;
  contentType: string;
  uploadFrequency: string;
  targetGoal: string;
  additionalNotes: string;
}