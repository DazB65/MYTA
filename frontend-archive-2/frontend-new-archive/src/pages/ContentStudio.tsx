import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { useContentCards } from '@/hooks/useContentCards';
import CardModal from '@/components/content-studio/CardModal';

import { ContentCard, CardStatus, Suggestion, Progress } from '@/types/contentStudio';
import type { Tag } from '@/types/contentStudio';
import { CardFormData } from '@/lib/validationSchemas';

// Helper to combine class names
const cx = (...classes: any[]) => classes.filter(Boolean).join(' ');

// SVG Icons - using inline SVGs to avoid external dependencies
const CalendarIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4 mr-2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"></rect><line x1="16" x2="16" y1="2" y2="6"></line><line x1="8" x2="8" y1="2" y2="6"></line><line x1="3" x2="21" y1="10" y2="10"></line></svg>
);

const PlusIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><line x1="12" x2="12" y1="5" y2="19"></line><line x1="5" x2="19" y1="12" y2="12"></line></svg>
);

const CheckCircleIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
);

const TrendingUpIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
);

const TargetIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
);

const RepeatIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6"><path d="M17 2.1l4 4-4 4"></path><path d="M3 12.2v-2a4 4 0 0 1 4-4h12.8"></path><path d="M7 21.9l-4-4 4-4"></path><path d="M21 11.8v2a4 4 0 0 1-4 4H4.2"></path></svg>
);


// Mock data for AI suggestions (keeping this static for now)
const suggestionsData: Suggestion[] = [
    {
        id: 'sug-1',
        type: 'Trending',
        title: 'AI Video Generation',
        metric: '+128% search volume',
        description: 'Video generators like Runway, Pika Labs, and Sora are gaining significant traction. A comparison video would likely perform well.',
        tags: [{ text: 'High revenue potential', color: 'green' }],
        icon: <TrendingUpIcon />,
        iconBg: 'bg-blue-500/20',
        iconColor: 'text-blue-400'
    },
    {
        id: 'sug-2',
        type: 'Opportunity',
        title: 'Budget PC Builds',
        metric: '+48% engagement',
        description: 'Your audience engagement spikes when discussing affordable tech. A "$500 Content Creator PC Build" video could perform exceptionally well.',
        tags: [{ text: 'Medium revenue potential', color: 'yellow' }],
        icon: <TargetIcon />,
        iconBg: 'bg-green-500/20',
        iconColor: 'text-green-400'
    },
    {
        id: 'sug-3',
        type: 'Repurpose',
        title: 'Day in the Life',
        metric: '+85% subscriber growth',
        description: 'Your "Creator Workday" video from 6 months ago led to significant subscriber growth. Consider creating an updated version showing your new workflow.',
        tags: [{ text: 'High subscriber growth', color: 'purple' }],
        icon: <RepeatIcon />,
        iconBg: 'bg-purple-500/20',
        iconColor: 'text-purple-400'
    }
];

// Tag Component
const Tag = ({ text, color, icon }: Tag) => {
    const colors: Record<Tag['color'], string> = {
        blue: 'bg-blue-500/20 text-blue-400',
        green: 'bg-green-500/20 text-green-400',
        purple: 'bg-purple-500/20 text-purple-400',
        yellow: 'bg-yellow-500/20 text-yellow-400',
        red: 'bg-red-500/20 text-red-400',
        orange: 'bg-orange-500/20 text-orange-400',
        gray: 'bg-gray-500/20 text-gray-400',
    };
    return (
        <div className={cx('flex items-center text-xs font-medium px-2 py-1 rounded-full', colors[color])}>
            {icon}
            <span>{text}</span>
        </div>
    );
};

// Progress Bar Component
const ProgressBar = ({ label, value, check }: Progress) => (
    <div className="mt-4">
        <div className="flex justify-between items-center text-xs text-gray-400 mb-1">
            <span className="flex items-center">
                {check && <CheckCircleIcon className="w-4 h-4 mr-1 text-green-500" />}
                {label}
            </span>
            <span>{value}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-1.5">
            <div
                className={cx('h-1.5 rounded-full', value === 100 ? 'bg-green-500' : 'bg-blue-500')}
                style={{ width: `${value}%` }}
            ></div>
        </div>
    </div>
);

// Content Card Component
const ContentCardComponent = ({ 
    card, 
    onEdit, 
    onDelete, 
    onDuplicate, 
    onMove 
}: { 
    card: ContentCard; 
    onEdit: (card: ContentCard) => void;
    onDelete: (cardId: string) => void;
    onDuplicate: (cardId: string) => void;
    onMove: (cardId: string, status: CardStatus) => void;
}) => {
    const [showContextMenu, setShowContextMenu] = useState(false);
    const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });

    const handleContextMenu = (e: React.MouseEvent) => {
        e.preventDefault();
        setContextMenuPosition({ x: e.clientX, y: e.clientY });
        setShowContextMenu(true);
    };

    const handleClick = () => {
        onEdit(card);
    };

    const statusOptions = [
        { value: 'ideas', label: 'Ideas' },
        { value: 'planning', label: 'Planning' },
        { value: 'inProgress', label: 'In Progress' },
        { value: 'ready', label: 'Ready to Publish' }
    ] as const;

    return (
        <>
            <div 
                className="bg-white p-4 rounded-lg border border-gray-200 mb-4 cursor-pointer hover:border-gray-300 hover:shadow-md transition-all duration-200 relative"
                onClick={handleClick}
                onContextMenu={handleContextMenu}
            >
                <h4 className="font-semibold text-gray-900">{card.title}</h4>
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">{card.description}</p>
                <div className="flex flex-wrap gap-2 mt-3">
                    {card.pillars?.map((pillar, index) => (
                        <div key={index} className="flex items-center space-x-1 px-2 py-1 bg-gray-100 rounded text-xs">
                            <div className={`w-3 h-3 rounded bg-gradient-to-br ${pillar.color} flex items-center justify-center text-xs`}>
                                {pillar.icon}
                            </div>
                            <span className="text-gray-700">{pillar.name}</span>
                        </div>
                    ))}
                </div>
                {card.dueDate && (
                    <p className="text-xs text-gray-600 mt-3">Due: {card.dueDate}</p>
                )}
                {card.progress && <ProgressBar {...card.progress} />}
            </div>

            {/* Context Menu */}
            {showContextMenu && (
                <>
                    <div 
                        className="fixed inset-0 z-40" 
                        onClick={() => setShowContextMenu(false)}
                    />
                    <div 
                        className="fixed z-50 bg-white border border-gray-200 rounded-lg shadow-xl py-2 min-w-[160px]"
                        style={{ 
                            left: contextMenuPosition.x, 
                            top: contextMenuPosition.y 
                        }}
                    >
                        <button
                            onClick={() => {
                                onEdit(card);
                                setShowContextMenu(false);
                            }}
                            className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                        >
                            Edit
                        </button>
                        <button
                            onClick={() => {
                                onDuplicate(card.id);
                                setShowContextMenu(false);
                            }}
                            className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                        >
                            Duplicate
                        </button>
                        <div className="border-t border-gray-200 my-1" />
                        <div className="px-4 py-1">
                            <p className="text-xs text-gray-500 uppercase tracking-wide">Move to</p>
                        </div>
                        {statusOptions
                            .filter(option => option.value !== card.status)
                            .map((option) => (
                                <button
                                    key={option.value}
                                    onClick={() => {
                                        onMove(card.id, option.value);
                                        setShowContextMenu(false);
                                    }}
                                    className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                                >
                                    {option.label}
                                </button>
                            ))
                        }
                        <div className="border-t border-gray-200 my-1" />
                        <button
                            onClick={() => {
                                onDelete(card.id);
                                setShowContextMenu(false);
                            }}
                            className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 transition-colors"
                        >
                            Delete
                        </button>
                    </div>
                </>
            )}
        </>
    );
};

// Kanban Column Component
const KanbanColumn = ({ 
    title, 
    count, 
    children, 
    accentColor, 
    status, 
    onQuickAdd 
}: { 
    title: string; 
    count: number; 
    children: React.ReactNode; 
    accentColor: string;
    status: CardStatus;
    onQuickAdd: (status: CardStatus) => void;
}) => (
    <div>
        <div className="flex justify-between items-center mb-4">
            <div className="flex items-center">
                <div className={cx("w-2 h-2 rounded-full mr-2", accentColor)}></div>
                <h3 className="font-semibold text-gray-900">{title}</h3>
                <span className="ml-2 text-sm text-gray-600 bg-gray-100 px-2 py-0.5 rounded-full">{count}</span>
            </div>
            <button 
                onClick={() => onQuickAdd(status)}
                className="text-gray-400 hover:text-gray-700 transition-colors"
                title={`Add new card to ${title}`}
            >
                <PlusIcon className="w-5 h-5" />
            </button>
        </div>
        <div className="min-h-[200px]">{children}</div>
    </div>
);

// Suggestion Card Component
const SuggestionCard = ({ suggestion }: { suggestion: Suggestion }) => (
    <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow flex flex-col">
        <div className="flex items-start justify-between">
            <div className={cx("w-10 h-10 rounded-lg flex items-center justify-center", suggestion.iconBg, suggestion.iconColor)}>
                {suggestion.icon}
            </div>
            <div className="text-right">
                <p className="font-semibold text-green-400">{suggestion.metric}</p>
                <p className="text-sm text-gray-400">{suggestion.type}</p>
            </div>
        </div>
        <div className="mt-4 flex-grow">
            <h4 className="font-semibold text-gray-900">{suggestion.title}</h4>
            <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
        </div>
        <div className="flex items-center justify-between mt-4">
            <div className="flex flex-wrap gap-2">
                {suggestion.tags.map((tag, index) => (
                    <Tag key={index} {...tag} />
                ))}
            </div>
            <button className="text-sm font-semibold text-blue-400 hover:text-blue-300">Add to Ideas</button>
        </div>
    </div>
);

export default function ContentStudio() {
    const [activeTab, setActiveTab] = useState('Ideas & Planning');
    const [isCardModalOpen, setIsCardModalOpen] = useState(false);
    const [editingCard, setEditingCard] = useState<ContentCard | null>(null);
    const [defaultStatus, setDefaultStatus] = useState<CardStatus>('ideas');
    
    const tabs = ['Ideas & Planning', 'Scripts', 'Thumbnails', 'Keywords', 'Analytics'];

    // Use the custom hook for card operations
    const {
        loading,
        error,
        addCard,
        editCard,
        removeCard,
        copyCard,
        moveCard,
        getCardsByStatus
    } = useContentCards();

    // Filter cards by status
    const ideasCards = getCardsByStatus('ideas');
    const planningCards = getCardsByStatus('planning');
    const inProgressCards = getCardsByStatus('inProgress');
    const readyCards = getCardsByStatus('ready');

    // Modal handlers
    const handleNewContent = () => {
        setEditingCard(null);
        setDefaultStatus('ideas');
        setIsCardModalOpen(true);
    };

    const handleQuickAdd = (status: CardStatus) => {
        setEditingCard(null);
        setDefaultStatus(status);
        setIsCardModalOpen(true);
    };

    const handleEditCard = (card: ContentCard) => {
        setEditingCard(card);
        setIsCardModalOpen(true);
    };

    const handleCardSubmit = async (data: CardFormData): Promise<boolean> => {
        if (editingCard) {
            return await editCard(editingCard.id, data);
        } else {
            return await addCard(data);
        }
    };

    const handleCloseModal = () => {
        setIsCardModalOpen(false);
        setEditingCard(null);
    };

    const handleDeleteCard = async (cardId: string) => {
        if (confirm('Are you sure you want to delete this content card?')) {
            await removeCard(cardId);
        }
    };

    const handleDuplicateCard = async (cardId: string) => {
        await copyCard(cardId);
    };

    const handleMoveCard = async (cardId: string, newStatus: CardStatus) => {
        await moveCard(cardId, newStatus);
    };

    if (loading) {
        return (
            <div className="min-h-screen font-sans p-4 sm:p-6 lg:p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="flex items-center justify-center h-64">
                        <div className="text-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                            <p className="mt-4 text-gray-600">Loading content cards...</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen font-sans p-4 sm:p-6 lg:p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="flex items-center justify-center h-64">
                        <div className="text-center">
                            <div className="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <p className="text-red-600 font-medium">{error}</p>
                            <p className="mt-2 text-gray-600 text-sm">
                                Please ensure the Supabase database is properly configured and the content_cards table exists
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen font-sans">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">Content Studio</h1>
                        <p className="text-gray-600 mt-1">Create, plan, and optimize your content</p>
                    </div>
                    <div className="flex items-center gap-2 mt-4 sm:mt-0">
                        <button className="flex items-center bg-white border border-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:bg-gray-50 hover:shadow-sm transition-all duration-200">
                            <CalendarIcon />
                            <span>Calendar View</span>
                        </button>
                        <button 
                            onClick={handleNewContent}
                            className="flex items-center bg-primary-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors duration-200"
                        >
                            <PlusIcon className="w-5 h-5 mr-1" />
                            <span>New Content</span>
                        </button>
                    </div>
                </header>

                {/* Tabs */}
                <nav className="mb-8">
                    <div className="border-b border-gray-200">
                        <div className="flex space-x-4 sm:space-x-8 -mb-px">
                            {tabs.map(tab => (
                                <button
                                    key={tab}
                                    onClick={() => setActiveTab(tab)}
                                    className={cx(
                                        'py-3 px-1 text-sm sm:text-base font-medium transition-colors duration-200',
                                        activeTab === tab
                                            ? 'border-b-2 border-primary-500 text-gray-900'
                                            : 'border-b-2 border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                                    )}
                                >
                                    {tab}
                                </button>
                            ))}
                        </div>
                    </div>
                </nav>

                {/* Kanban Board */}
                <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <KanbanColumn 
                        title="Ideas" 
                        count={ideasCards.length} 
                        accentColor="bg-purple-500"
                        status="ideas"
                        onQuickAdd={handleQuickAdd}
                    >
                        {ideasCards.map(card => (
                            <ContentCardComponent 
                                key={card.id} 
                                card={card}
                                onEdit={handleEditCard}
                                onDelete={handleDeleteCard}
                                onDuplicate={handleDuplicateCard}
                                onMove={handleMoveCard}
                            />
                        ))}
                    </KanbanColumn>
                    <KanbanColumn 
                        title="Planning" 
                        count={planningCards.length} 
                        accentColor="bg-yellow-500"
                        status="planning"
                        onQuickAdd={handleQuickAdd}
                    >
                        {planningCards.map(card => (
                            <ContentCardComponent 
                                key={card.id} 
                                card={card}
                                onEdit={handleEditCard}
                                onDelete={handleDeleteCard}
                                onDuplicate={handleDuplicateCard}
                                onMove={handleMoveCard}
                            />
                        ))}
                    </KanbanColumn>
                    <KanbanColumn 
                        title="In Progress" 
                        count={inProgressCards.length} 
                        accentColor="bg-blue-500"
                        status="inProgress"
                        onQuickAdd={handleQuickAdd}
                    >
                        {inProgressCards.map(card => (
                            <ContentCardComponent 
                                key={card.id} 
                                card={card}
                                onEdit={handleEditCard}
                                onDelete={handleDeleteCard}
                                onDuplicate={handleDuplicateCard}
                                onMove={handleMoveCard}
                            />
                        ))}
                    </KanbanColumn>
                    <KanbanColumn 
                        title="Ready to Publish" 
                        count={readyCards.length} 
                        accentColor="bg-green-500"
                        status="ready"
                        onQuickAdd={handleQuickAdd}
                    >
                        {readyCards.map(card => (
                            <ContentCardComponent 
                                key={card.id} 
                                card={card}
                                onEdit={handleEditCard}
                                onDelete={handleDeleteCard}
                                onDuplicate={handleDuplicateCard}
                                onMove={handleMoveCard}
                            />
                        ))}
                    </KanbanColumn>
                </main>

                {/* AI Suggestions Section */}
                <section className="mt-12">
                     <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
                        <h2 className="text-xl font-bold text-gray-900">AI Content Suggestions</h2>
                        <button className="mt-3 sm:mt-0 bg-white border border-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:bg-gray-50 hover:shadow-sm transition-all duration-200">
                            All Pillars
                        </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {suggestionsData.map(suggestion => (
                            <SuggestionCard key={suggestion.id} suggestion={suggestion} />
                        ))}
                    </div>
                </section>
            </div>
            
            {/* Card Modal */}
            <CardModal
                isOpen={isCardModalOpen}
                onClose={handleCloseModal}
                onSubmit={handleCardSubmit}
                card={editingCard}
                defaultStatus={defaultStatus}
            />
            
            {/* Toast Notifications */}
            <Toaster
                position="bottom-right"
                toastOptions={{
                    duration: 4000,
                    style: {
                        background: '#ffffff',
                        color: '#374151',
                        border: '1px solid #e5e7eb',
                    },
                    success: {
                        iconTheme: {
                            primary: '#10b981',
                            secondary: '#ffffff',
                        },
                    },
                    error: {
                        iconTheme: {
                            primary: '#ef4444',
                            secondary: '#ffffff',
                        },
                    },
                }}
            />
        </div>
    );
}