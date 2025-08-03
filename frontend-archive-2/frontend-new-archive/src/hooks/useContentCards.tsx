import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { ContentCard, CardFormData, CardStatus } from '@/types/contentStudio';
import { contentCardsApi } from '@/lib/contentCardsApi';

export function useContentCards() {
    const [cards, setCards] = useState<ContentCard[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch content cards from API
    useEffect(() => {
        let intervalId: NodeJS.Timeout;
        
        const fetchCards = async () => {
            try {
                console.log('Fetching cards from API...');
                
                // Fetch all non-archived cards from the API
                const result = await contentCardsApi.fetchCards();
                console.log('API query completed, card count:', result.cards.length);
                
                setCards(result.cards);
                setLoading(false);
                setError(null);
            } catch (error) {
                console.error('Error fetching cards:', error);
                setError('Failed to load content cards. Please refresh the page.');
                setLoading(false);
            }
        };

        // Initial fetch
        fetchCards();
        
        // Poll every 10 seconds for updates (can be adjusted or replaced with websockets later)
        intervalId = setInterval(fetchCards, 10000);

        return () => {
            console.log('Cleaning up card polling');
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, []); // No dependencies to prevent restart loops

    // Create new card
    const addCard = async (cardData: CardFormData): Promise<boolean> => {
        try {
            console.log('useContentCards: Starting card creation...');
            const newCard = await contentCardsApi.createCard(cardData);
            console.log('useContentCards: Card created successfully with ID:', newCard.id);
            
            // Optimistically update local state
            setCards(prevCards => [...prevCards, newCard]);
            
            toast.success('Content card created successfully!');
            return true;
        } catch (error) {
            console.error('useContentCards: Error creating card:', error);
            toast.error('Failed to create content card');
            return false;
        }
    };

    // Update existing card
    const editCard = async (cardId: string, updates: Partial<ContentCard>): Promise<boolean> => {
        try {
            const updatedCard = await contentCardsApi.updateCard(cardId, updates);
            
            // Optimistically update local state
            setCards(prevCards => 
                prevCards.map(card => 
                    card.id === cardId ? updatedCard : card
                )
            );
            
            toast.success('Content card updated successfully!');
            return true;
        } catch (error) {
            toast.error('Failed to update content card');
            console.error('Error updating card:', error);
            return false;
        }
    };

    // Delete card
    const removeCard = async (cardId: string): Promise<boolean> => {
        try {
            await contentCardsApi.deleteCard(cardId);
            
            // Optimistically update local state (remove the card)
            setCards(prevCards => prevCards.filter(card => card.id !== cardId));
            
            toast.success('Content card deleted successfully!');
            return true;
        } catch (error) {
            toast.error('Failed to delete content card');
            console.error('Error deleting card:', error);
            return false;
        }
    };

    // Duplicate card
    const copyCard = async (cardId: string): Promise<boolean> => {
        try {
            const originalCard = cards.find(card => card.id === cardId);
            if (!originalCard) {
                toast.error('Card not found');
                return false;
            }
            
            const duplicatedCard = await contentCardsApi.duplicateCard(cardId);
            
            // Optimistically update local state
            setCards(prevCards => [...prevCards, duplicatedCard]);
            
            toast.success('Content card duplicated successfully!');
            return true;
        } catch (error) {
            toast.error('Failed to duplicate content card');
            console.error('Error duplicating card:', error);
            return false;
        }
    };

    // Move card to different status
    const moveCard = async (cardId: string, newStatus: CardStatus): Promise<boolean> => {
        try {
            await contentCardsApi.updateCardStatus(cardId, newStatus);
            
            // Optimistically update local state
            setCards(prevCards => 
                prevCards.map(card => 
                    card.id === cardId ? { ...card, status: newStatus } : card
                )
            );
            
            toast.success(`Card moved to ${newStatus}`);
            return true;
        } catch (error) {
            toast.error('Failed to move content card');
            console.error('Error moving card:', error);
            return false;
        }
    };

    // Reorder cards (for drag and drop)
    const reorderCards = async (cardUpdates: { id: string; order: number }[]): Promise<boolean> => {
        try {
            await contentCardsApi.updateCardOrders(cardUpdates);
            
            // Optimistically update local state
            setCards(prevCards => {
                const updated = [...prevCards];
                cardUpdates.forEach(update => {
                    const cardIndex = updated.findIndex(card => card.id === update.id);
                    if (cardIndex !== -1) {
                        updated[cardIndex] = { ...updated[cardIndex], order_index: update.order };
                    }
                });
                return updated;
            });
            
            return true;
        } catch (error) {
            toast.error('Failed to reorder cards');
            console.error('Error reordering cards:', error);
            return false;
        }
    };

    // Filter cards by status
    const getCardsByStatus = (status: CardStatus): ContentCard[] => {
        return cards.filter(card => card.status === status && !card.archived);
    };

    // Get card by ID
    const getCardById = (cardId: string): ContentCard | undefined => {
        return cards.find(card => card.id === cardId);
    };

    // Search cards
    const searchCards = (searchTerm: string): ContentCard[] => {
        if (!searchTerm.trim()) return cards;
        
        const term = searchTerm.toLowerCase();
        return cards.filter(card => 
            card.title.toLowerCase().includes(term) ||
            card.description.toLowerCase().includes(term) ||
            card.pillars?.some(pillar => pillar.name.toLowerCase().includes(term))
        );
    };

    return {
        cards,
        loading,
        error,
        addCard,
        editCard,
        removeCard,
        copyCard,
        moveCard,
        reorderCards,
        getCardsByStatus,
        getCardById,
        searchCards
    };
}