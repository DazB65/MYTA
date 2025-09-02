/**
 * SEO composable for dynamic meta tags and structured data
 * Provides easy-to-use functions for optimizing page SEO
 */
import { useHead, useSeoMeta } from '#app'

export const useSEO = () => {
  // Set page SEO with comprehensive meta tags
  const setPageSEO = ({
    title,
    description,
    keywords,
    image = '/MY YT AGENT.png',
    url,
    type = 'website',
    author = 'MYTA',
    publishedTime,
    modifiedTime,
    section,
    tags = []
  }) => {
    // Construct full title
    const fullTitle = title ? `${title} | MYTA` : 'MYTA - Your AI Team for YouTube Growth'
    const fullDescription = description || 'Your AI team for YouTube growth. Built for teams, perfect for individuals. Coordinated AI agents working together to grow your channel strategically.'
    const fullUrl = url ? `https://myta.app${url}` : 'https://myta.app'
    const fullImage = image.startsWith('http') ? image : `https://myta.app${image}`

    // Set meta tags using Nuxt's useSeoMeta
    useSeoMeta({
      title: fullTitle,
      description: fullDescription,
      keywords: keywords || 'YouTube analytics, AI content optimization, YouTube growth, video analytics, content strategy',
      author,
      robots: 'index, follow',
      
      // Open Graph
      ogTitle: fullTitle,
      ogDescription: fullDescription,
      ogImage: fullImage,
      ogUrl: fullUrl,
      ogType: type,
      ogSiteName: 'MYTA',
      
      // Twitter Card
      twitterCard: 'summary_large_image',
      twitterTitle: fullTitle,
      twitterDescription: fullDescription,
      twitterImage: fullImage,
      twitterSite: '@myta_app',
      twitterCreator: '@myta_app',
      
      // Article specific (for blog posts, etc.)
      ...(publishedTime && { articlePublishedTime: publishedTime }),
      ...(modifiedTime && { articleModifiedTime: modifiedTime }),
      ...(section && { articleSection: section }),
      ...(tags.length > 0 && { articleTag: tags }),
      
      // Additional SEO
      canonical: fullUrl,
      language: 'en',
      revisitAfter: '7 days'
    })

    // Set additional head elements
    useHead({
      link: [
        { rel: 'canonical', href: fullUrl }
      ]
    })
  }

  // Set structured data for better search engine understanding
  const setStructuredData = (data) => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify(data)
        }
      ]
    })
  }

  // Predefined structured data templates
  const setWebsiteStructuredData = () => {
    setStructuredData({
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: 'MYTA',
      description: 'AI-powered YouTube analytics and content optimization platform',
      url: 'https://myta.app',
      potentialAction: {
        '@type': 'SearchAction',
        target: 'https://myta.app/search?q={search_term_string}',
        'query-input': 'required name=search_term_string'
      },
      publisher: {
        '@type': 'Organization',
        name: 'MYTA',
        url: 'https://myta.app',
        logo: {
          '@type': 'ImageObject',
          url: 'https://myta.app/MY YT AGENT.png'
        }
      }
    })
  }

  const setSoftwareApplicationStructuredData = () => {
    setStructuredData({
      '@context': 'https://schema.org',
      '@type': 'SoftwareApplication',
      name: 'MYTA',
      description: 'AI-powered YouTube analytics and content optimization platform',
      url: 'https://myta.app',
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Web',
      browserRequirements: 'Requires JavaScript. Requires HTML5.',
      softwareVersion: '1.0',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'USD',
        availability: 'https://schema.org/InStock'
      },
      creator: {
        '@type': 'Organization',
        name: 'MYTA',
        url: 'https://myta.app'
      },
      screenshot: 'https://myta.app/screenshot-desktop.png',
      featureList: [
        'YouTube Analytics Dashboard',
        'AI-Powered Content Recommendations',
        'Performance Tracking',
        'Growth Optimization',
        'Real-time Insights'
      ]
    })
  }

  const setBreadcrumbStructuredData = (breadcrumbs) => {
    const breadcrumbList = breadcrumbs.map((crumb, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: crumb.name,
      item: `https://myta.app${crumb.url}`
    }))

    setStructuredData({
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: breadcrumbList
    })
  }

  const setArticleStructuredData = ({
    title,
    description,
    image,
    datePublished,
    dateModified,
    author = 'MYTA Team',
    section = 'YouTube Analytics'
  }) => {
    setStructuredData({
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: title,
      description,
      image: image ? `https://myta.app${image}` : 'https://myta.app/MY YT AGENT.png',
      datePublished,
      dateModified: dateModified || datePublished,
      author: {
        '@type': 'Organization',
        name: author,
        url: 'https://myta.app'
      },
      publisher: {
        '@type': 'Organization',
        name: 'MYTA',
        url: 'https://myta.app',
        logo: {
          '@type': 'ImageObject',
          url: 'https://myta.app/MY YT AGENT.png'
        }
      },
      articleSection: section,
      mainEntityOfPage: {
        '@type': 'WebPage',
        '@id': 'https://myta.app'
      }
    })
  }

  // Generate meta keywords from content
  const generateKeywords = (content, baseKeywords = []) => {
    const commonWords = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'a', 'an']
    
    const words = content
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/)
      .filter(word => word.length > 3 && !commonWords.includes(word))
    
    const wordCount = {}
    words.forEach(word => {
      wordCount[word] = (wordCount[word] || 0) + 1
    })
    
    const topWords = Object.entries(wordCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([word]) => word)
    
    return [...baseKeywords, ...topWords].join(', ')
  }

  // Optimize meta description length
  const optimizeDescription = (description, maxLength = 160) => {
    if (description.length <= maxLength) return description
    
    const truncated = description.substring(0, maxLength - 3)
    const lastSpace = truncated.lastIndexOf(' ')
    
    return lastSpace > 0 ? truncated.substring(0, lastSpace) + '...' : truncated + '...'
  }

  // Page-specific SEO helpers
  const setDashboardSEO = () => {
    setPageSEO({
      title: 'Dashboard',
      description: 'Your YouTube analytics dashboard with AI-powered insights, performance tracking, and growth recommendations.',
      keywords: 'YouTube dashboard, analytics dashboard, video performance, channel insights',
      url: '/dashboard'
    })
    setBreadcrumbStructuredData([
      { name: 'Home', url: '/' },
      { name: 'Dashboard', url: '/dashboard' }
    ])
  }

  const setAnalyticsSEO = () => {
    setPageSEO({
      title: 'Analytics',
      description: 'Comprehensive YouTube analytics with detailed performance metrics, audience insights, and growth tracking.',
      keywords: 'YouTube analytics, video analytics, channel performance, audience insights, growth metrics',
      url: '/analytics'
    })
    setBreadcrumbStructuredData([
      { name: 'Home', url: '/' },
      { name: 'Analytics', url: '/analytics' }
    ])
  }

  const setVideosSEO = () => {
    setPageSEO({
      title: 'Videos',
      description: 'Manage and analyze your YouTube videos with AI-powered performance insights and optimization recommendations.',
      keywords: 'YouTube videos, video management, video analytics, content optimization',
      url: '/videos'
    })
    setBreadcrumbStructuredData([
      { name: 'Home', url: '/' },
      { name: 'Videos', url: '/videos' }
    ])
  }

  return {
    setPageSEO,
    setStructuredData,
    setWebsiteStructuredData,
    setSoftwareApplicationStructuredData,
    setBreadcrumbStructuredData,
    setArticleStructuredData,
    generateKeywords,
    optimizeDescription,
    setDashboardSEO,
    setAnalyticsSEO,
    setVideosSEO
  }
}
