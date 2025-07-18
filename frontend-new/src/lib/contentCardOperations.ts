/**
 * Content Card Operations
 * Legacy compatibility layer for existing components
 * Now uses the new Supabase API instead of Firebase
 */

import { ContentCard, CardFormData, CardStatus } from '@/types/contentStudio';
import { contentCardsApi } from './contentCardsApi';

/**
 * Create a new content card
 * @param cardData The card data to create
 * @returns Promise with the created card ID
 */
export async function createContentCard(cardData: CardFormData): Promise<string> {
    try {
        console.log('Creating content card with data:', cardData);
        
        const createdCard = await contentCardsApi.createCard(cardData);
        console.log('Successfully created card with ID:', createdCard.id);
        
        return createdCard.id;
    } catch (error) {
        console.error('Error creating content card:', error);
        throw new Error(`Failed to create content card: ${error instanceof Error ? error.message : error}`);
    }
}

/**
 * Update an existing content card
 * @param cardId The ID of the card to update
 * @param updates Partial card data to update
 * @returns Promise that resolves when update is complete
 */
export async function updateContentCard(cardId: string, updates: Partial<ContentCard>): Promise<void> {
    try {
        await contentCardsApi.updateCard(cardId, updates);
    } catch (error) {
        console.error('Error updating content card:', error);
        throw new Error('Failed to update content card');
    }
}

/**
 * Delete a content card (soft delete by marking as archived)
 * @param cardId The ID of the card to delete
 * @returns Promise that resolves when deletion is complete
 */
export async function deleteContentCard(cardId: string): Promise<void> {
    try {
        await contentCardsApi.deleteCard(cardId);
    } catch (error) {
        console.error('Error deleting content card:', error);
        throw new Error('Failed to delete content card');
    }
}

/**
 * Update card status (for drag and drop)
 * @param cardId The ID of the card to update
 * @param newStatus The new status
 * @param newOrder Optional new order index
 * @returns Promise that resolves when update is complete
 */
export async function updateCardStatus(cardId: string, newStatus: CardStatus, newOrder?: number): Promise<void> {
    try {
        await contentCardsApi.updateCardStatus(cardId, newStatus, newOrder);
    } catch (error) {
        console.error('Error updating card status:', error);
        throw new Error('Failed to update card status');
    }
}

/**
 * Duplicate a content card
 * @param cardId The ID of the card to duplicate (originalCard parameter is no longer needed)
 * @param originalCard Legacy parameter for compatibility (ignored)
 * @returns Promise with the duplicated card ID
 */
export async function duplicateContentCard(cardId: string, _originalCard?: ContentCard): Promise<string> {
    try {
        const duplicatedCard = await contentCardsApi.duplicateCard(cardId);
        return duplicatedCard.id;
    } catch (error) {
        console.error('Error duplicating content card:', error);
        throw new Error('Failed to duplicate content card');
    }
}

/**
 * Batch update card orders (for reordering within columns)
 * @param cardUpdates Array of {id, order} updates
 * @returns Promise that resolves when updates are complete
 */
export async function updateCardOrders(cardUpdates: { id: string; order: number }[]): Promise<void> {
    try {
        await contentCardsApi.updateCardOrders(cardUpdates);
    } catch (error) {
        console.error('Error updating card orders:', error);
        throw new Error('Failed to update card orders');
    }
}

/**
 * Get next order value for a specific status column
 * @param status The status to get the next order for
 * @returns Promise with the next order value
 */
export async function getNextOrderForStatus(_status: CardStatus): Promise<number> {
    try {
        // This is now handled automatically by the backend
        // Return a default value for compatibility
        return Date.now();
    } catch (error) {
        console.error('Error getting next order:', error);
        return Date.now(); // Fallback to timestamp
    }
}

/**
 * Fetch cards by status (legacy compatibility)
 * @param status The status to filter by
 * @returns Promise with array of cards
 */
export async function fetchCardsByStatus(status: CardStatus): Promise<ContentCard[]> {
    try {
        return await contentCardsApi.fetchCardsByStatus(status);
    } catch (error) {
        console.error('Error fetching cards by status:', error);
        return [];
    }
}