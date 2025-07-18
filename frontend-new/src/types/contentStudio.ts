// Content Studio Type Definitions

export interface Tag {
    text: string;
    color: 'blue' | 'green' | 'purple' | 'yellow' | 'red' | 'orange' | 'gray';
    icon?: React.ReactNode;
}

export interface Pillar {
    id: string;
    name: string;
    icon: string;
    color: string;
}

export interface Progress {
    label: string;
    value: number;
    check?: boolean;
}

export type CardStatus = 'ideas' | 'planning' | 'inProgress' | 'ready';

export interface ContentCard {
    id: string;
    user_id?: string;
    title: string;
    description: string;
    pillars: Pillar[];
    status: CardStatus;
    dueDate?: string;
    due_date?: string; // Supabase field name
    progress?: Progress;
    order?: number; // Legacy field
    order_index?: number; // Supabase field name
    templateId?: string;
    createdAt?: any;
    updatedAt?: any;
    created_at?: string; // Supabase field name
    updated_at?: string; // Supabase field name
    lastModified?: any;
    modifiedBy?: string;
    archived?: boolean;
}

export interface Suggestion {
    id: string;
    type: string;
    title: string;
    metric: string;
    description: string;
    tags: Tag[];
    icon: React.ReactNode;
    iconBg: string;
    iconColor: string;
}

export interface CardFormData {
    title: string;
    description: string;
    pillars: Pillar[];
    status: CardStatus;
    dueDate?: string;
    progress?: Progress;
}

export type ViewMode = 'kanban' | 'calendar';

export interface ContentStudioFilters {
    search: string;
    selectedPillars: string[];
    selectedStatuses: CardStatus[];
    dateRange?: {
        from: Date;
        to: Date;
    };
}