/**
 * Content Cards API Client for CreatorMate
 * Replaces Firebase Firestore operations with backend API calls
 * Provides a clean interface for Content Studio operations
 */

import { ContentCard, CardFormData, CardStatus } from '@/types/contentStudio';

// Get the API base URL from environment or default to current host
const API_BASE = `${window.location.origin}/api/content-cards`;

// Helper function to get user ID (you may need to adjust this based on your auth system)
function getUserId(): string {
  // This should match your existing user identification system
  // For now, using localStorage as per your existing patterns
  return localStorage.getItem('creatormate_user_id') || 'default_user';
}

// Helper function to handle API responses
async function handleApiResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'Network error' }));
    throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  // Backend returns {status, message, data} format
  if (data.status === 'success') {
    return data.data;
  } else {
    throw new Error(data.message || 'API request failed');
  }
}

// Helper function to make authenticated requests
async function apiRequest(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  return fetch(url, {
    ...options,
    headers: defaultHeaders,
  });
}

/**
 * Content Cards API Client
 * Provides methods to interact with content cards backend API
 */
export const contentCardsApi = {
  /**
   * Fetch content cards for the current user
   * @param status Optional status filter ('ideas', 'planning', 'inProgress', 'ready')
   * @param includeArchived Whether to include archived cards
   * @returns Promise with cards data
   */
  async fetchCards(status?: CardStatus, includeArchived: boolean = false): Promise<{
    cards: ContentCard[];
    total_count: number;
    status_counts: Record<string, number>;
  }> {
    const userId = getUserId();
    const params = new URLSearchParams({
      user_id: userId,
      include_archived: includeArchived.toString(),
    });
    
    if (status) {
      params.append('status', status);
    }
    
    const response = await apiRequest(`?${params.toString()}`);
    return handleApiResponse(response);
  },

  /**
   * Fetch cards filtered by status (for Kanban columns)
   * @param status The status to filter by
   * @returns Promise with array of cards
   */
  async fetchCardsByStatus(status: CardStatus): Promise<ContentCard[]> {
    const result = await this.fetchCards(status);
    return result.cards;
  },

  /**
   * Create a new content card
   * @param cardData The card data to create
   * @returns Promise with created card data
   */
  async createCard(cardData: CardFormData): Promise<ContentCard> {
    const userId = getUserId();
    
    const response = await apiRequest('', {
      method: 'POST',
      body: JSON.stringify({
        ...cardData,
        user_id: userId,
      }),
    });
    
    const result = await handleApiResponse<{ card: ContentCard }>(response);
    return result.card;
  },

  /**
   * Update an existing content card
   * @param cardId The ID of the card to update
   * @param updates Partial card data to update
   * @returns Promise with updated card data
   */
  async updateCard(cardId: string, updates: Partial<ContentCard>): Promise<ContentCard> {
    const userId = getUserId();
    
    const response = await apiRequest(`/${cardId}?user_id=${userId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
    
    const result = await handleApiResponse<{ card: ContentCard }>(response);
    return result.card;
  },

  /**
   * Update just the status of a content card (for drag-and-drop)
   * @param cardId The ID of the card to update
   * @param newStatus The new status
   * @param orderIndex Optional new order index
   * @returns Promise with success confirmation
   */
  async updateCardStatus(cardId: string, newStatus: CardStatus, orderIndex?: number): Promise<void> {
    const userId = getUserId();
    
    const response = await apiRequest(`/${cardId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({
        status: newStatus,
        user_id: userId,
        order_index: orderIndex,
      }),
    });
    
    await handleApiResponse(response);
  },

  /**
   * Soft delete a content card (mark as archived)
   * @param cardId The ID of the card to delete
   * @returns Promise with success confirmation
   */
  async deleteCard(cardId: string): Promise<void> {
    const userId = getUserId();
    
    const response = await apiRequest(`/${cardId}?user_id=${userId}`, {
      method: 'DELETE',
    });
    
    await handleApiResponse(response);
  },

  /**
   * Duplicate an existing content card
   * @param cardId The ID of the card to duplicate
   * @returns Promise with duplicated card data
   */
  async duplicateCard(cardId: string): Promise<ContentCard> {
    const userId = getUserId();
    
    const response = await apiRequest(`/${cardId}/duplicate?user_id=${userId}`, {
      method: 'POST',
    });
    
    const result = await handleApiResponse<{ card: ContentCard }>(response);
    return result.card;
  },

  /**
   * Get statistics about content cards for the current user
   * @returns Promise with stats data
   */
  async getStats(): Promise<{
    total_cards: number;
    status_counts: Record<string, number>;
    active_statuses: string[];
  }> {
    const userId = getUserId();
    
    const response = await apiRequest(`/stats/${userId}`);
    return handleApiResponse(response);
  },

  /**
   * Batch update card orders (for drag-and-drop reordering)
   * @param cardUpdates Array of {id, order} updates
   * @returns Promise with success confirmation
   */
  async updateCardOrders(cardUpdates: { id: string; order: number }[]): Promise<void> {
    // This could be implemented as multiple individual updates for now
    // or you could add a batch endpoint to the backend
    const promises = cardUpdates.map(update =>
      this.updateCard(update.id, { order_index: update.order })
    );
    
    await Promise.all(promises);
  },
};

/**
 * Export default for easier importing
 */
export default contentCardsApi;

/**
 * Legacy compatibility functions to match Firebase operations
 * These can be used to minimize changes in existing components
 */
export const contentCardOperations = {
  createContentCard: contentCardsApi.createCard,
  updateContentCard: contentCardsApi.updateCard,
  deleteContentCard: contentCardsApi.deleteCard,
  duplicateContentCard: contentCardsApi.duplicateCard,
  updateCardStatus: contentCardsApi.updateCardStatus,
  updateCardOrders: contentCardsApi.updateCardOrders,
};