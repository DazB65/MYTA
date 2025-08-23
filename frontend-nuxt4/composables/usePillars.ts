import { computed, ref } from 'vue'

// Sample pillar data structure
const pillarsData = ref([
  {
    id: 1,
    name: 'Game Development',
    icon: 'GameIcon',
    videoCount: 12,
    lastUpload: '2 days ago',
    status: 'Active • Next upload in 3 days',
    bestVideo: {
      id: 'best1',
      title: 'Building My First Indie Game in Unity',
      thumbnail: '/api/placeholder/320/180',
      views: 248300,
      uploadDate: '1 week ago',
      duration: '15:42'
    },
    recentVideos: [
      {
        id: 'vid1',
        title: 'Unity 2024 New Features Review',
        thumbnail: '/api/placeholder/320/180',
        views: 45200,
        uploadDate: '2 days ago',
        duration: '12:30',
        performance: 'Good'
      },
      {
        id: 'vid2',
        title: 'C# Tips for Game Developers',
        thumbnail: '/api/placeholder/320/180',
        views: 32100,
        uploadDate: '5 days ago',
        duration: '18:15',
        performance: 'Average'
      },
      {
        id: 'vid3',
        title: 'Game Design Patterns Explained',
        thumbnail: '/api/placeholder/320/180',
        views: 67800,
        uploadDate: '1 week ago',
        duration: '22:45',
        performance: 'Excellent'
      },
      {
        id: 'vid4',
        title: 'Debugging Unity Performance Issues',
        thumbnail: '/api/placeholder/320/180',
        views: 28900,
        uploadDate: '2 weeks ago',
        duration: '16:20',
        performance: 'Good'
      }
    ],
    contentIdeas: [
      {
        id: 'idea1',
        title: 'Mobile Game Development Tutorial',
        description: 'Complete guide to building mobile games',
        priority: 'High'
      },
      {
        id: 'idea2',
        title: 'Game Monetization Strategies',
        description: 'Different ways to monetize indie games',
        priority: 'Medium'
      },
      {
        id: 'idea3',
        title: 'Unity vs Unreal Engine Comparison',
        description: 'Pros and cons of each engine',
        priority: 'Low'
      }
    ],
    stats: {
      revenue: 2450,
      watchTime: '45.2K hrs',
      subscribers: 1200,
      engagementRate: 8.5,
      viewsGrowth: 12.5,
      revenueGrowth: 8.3,
      watchTimeGrowth: 15.2,
      subscriberGrowth: 9.8
    }
  },
  {
    id: 2,
    name: 'Game Reviews',
    icon: 'ReviewIcon',
    videoCount: 8,
    lastUpload: '4 days ago',
    status: 'Active • Planning next review',
    bestVideo: {
      id: 'best2',
      title: 'Cyberpunk 2077 Honest Review 2024',
      thumbnail: '/api/placeholder/320/180',
      views: 156700,
      uploadDate: '2 weeks ago',
      duration: '25:30'
    },
    recentVideos: [
      {
        id: 'vid5',
        title: 'Top 10 Indie Games of 2024',
        thumbnail: '/api/placeholder/320/180',
        views: 89400,
        uploadDate: '4 days ago',
        duration: '20:15',
        performance: 'Excellent'
      },
      {
        id: 'vid6',
        title: 'Baldurs Gate 3 Review',
        thumbnail: '/api/placeholder/320/180',
        views: 124300,
        uploadDate: '1 week ago',
        duration: '18:45',
        performance: 'Excellent'
      },
      {
        id: 'vid7',
        title: 'Steam Deck vs Nintendo Switch',
        thumbnail: '/api/placeholder/320/180',
        views: 76200,
        uploadDate: '2 weeks ago',
        duration: '14:30',
        performance: 'Good'
      }
    ],
    contentIdeas: [
      {
        id: 'idea4',
        title: 'Upcoming AAA Games 2024',
        description: 'Preview of most anticipated games',
        priority: 'High'
      },
      {
        id: 'idea5',
        title: 'Retro Gaming Hidden Gems',
        description: 'Underrated classic games worth playing',
        priority: 'Medium'
      }
    ],
    stats: {
      revenue: 1890,
      watchTime: '32.1K hrs',
      subscribers: 890,
      engagementRate: 9.2,
      viewsGrowth: 15.3,
      revenueGrowth: 12.1,
      watchTimeGrowth: 8.7,
      subscriberGrowth: 11.4
    }
  },
  {
    id: 3,
    name: 'Tech Tutorials',
    icon: 'TechIcon',
    videoCount: 15,
    lastUpload: '1 day ago',
    status: 'Very Active • Daily uploads',
    bestVideo: {
      id: 'best3',
      title: 'Complete Python Course for Beginners',
      thumbnail: '/api/placeholder/320/180',
      views: 342100,
      uploadDate: '3 weeks ago',
      duration: '45:20'
    },
    recentVideos: [
      {
        id: 'vid8',
        title: 'JavaScript ES2024 New Features',
        thumbnail: '/api/placeholder/320/180',
        views: 52300,
        uploadDate: '1 day ago',
        duration: '16:40',
        performance: 'Good'
      },
      {
        id: 'vid9',
        title: 'React vs Vue vs Angular 2024',
        thumbnail: '/api/placeholder/320/180',
        views: 78900,
        uploadDate: '3 days ago',
        duration: '22:15',
        performance: 'Excellent'
      },
      {
        id: 'vid10',
        title: 'Docker for Beginners',
        thumbnail: '/api/placeholder/320/180',
        views: 95600,
        uploadDate: '5 days ago',
        duration: '28:30',
        performance: 'Excellent'
      }
    ],
    contentIdeas: [
      {
        id: 'idea6',
        title: 'AI and Machine Learning Basics',
        description: 'Introduction to AI for developers',
        priority: 'High'
      },
      {
        id: 'idea7',
        title: 'Web3 Development Tutorial',
        description: 'Building decentralized applications',
        priority: 'Medium'
      },
      {
        id: 'idea8',
        title: 'Cybersecurity Best Practices',
        description: 'Security tips for developers',
        priority: 'High'
      }
    ]
  }
])

export const usePillars = () => {
  // Computed properties
  const totalVideos = computed(() => {
    return pillarsData.value.reduce((total, pillar) => total + pillar.videoCount, 0)
  })

  const totalViews = computed(() => {
    return pillarsData.value.reduce((total, pillar) => {
      return total + pillar.recentVideos.reduce((pillarTotal, video) => pillarTotal + video.views, 0)
    }, 0)
  })

  const activePillars = computed(() => {
    return pillarsData.value.filter(pillar => pillar.status.includes('Active'))
  })

  // Methods
  const addPillar = (pillarData) => {
    const newPillar = {
      id: Date.now(),
      ...pillarData,
      recentVideos: [],
      contentIdeas: []
    }
    pillarsData.value.push(newPillar)
  }

  const updatePillar = (pillarId, updates) => {
    const index = pillarsData.value.findIndex(p => p.id === pillarId)
    if (index !== -1) {
      pillarsData.value[index] = { ...pillarsData.value[index], ...updates }
    }
  }

  const deletePillar = (pillarId) => {
    const index = pillarsData.value.findIndex(p => p.id === pillarId)
    if (index !== -1) {
      pillarsData.value.splice(index, 1)
    }
  }

  const addContentIdea = (pillarId, idea) => {
    const pillar = pillarsData.value.find(p => p.id === pillarId)
    if (pillar) {
      pillar.contentIdeas.push({
        id: Date.now(),
        ...idea
      })
    }
  }

  const addVideo = (pillarId, video) => {
    const pillar = pillarsData.value.find(p => p.id === pillarId)
    if (pillar) {
      pillar.recentVideos.unshift({
        id: Date.now(),
        ...video
      })
      pillar.videoCount += 1
    }
  }

  return {
    // Data
    pillars: pillarsData,
    
    // Computed
    totalVideos,
    totalViews,
    activePillars,
    
    // Methods
    addPillar,
    updatePillar,
    deletePillar,
    addContentIdea,
    addVideo
  }
}
