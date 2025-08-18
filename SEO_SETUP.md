# SEO and Discoverability Setup

This document outlines the SEO and discoverability features implemented for the website.

## Sitemap and RSS Implementation

### Sitemap.xml
- **Plugin**: `jekyll-sitemap` automatically generates sitemap.xml
- **URL**: https://www.jtdub.com/sitemap.xml
- **Purpose**: Helps search engines discover and index all pages

### RSS Feed
- **Plugin**: `jekyll-feed` automatically generates RSS feed
- **URL**: https://www.jtdub.com/feed.xml
- **Purpose**: Allows readers to subscribe to updates
- **Discovery**: Linked in HTML head with `rel="alternate"`

### Robots.txt
- **Location**: `/robots.txt`
- **Purpose**: Guides search engine crawlers
- **Sitemap Reference**: Points to sitemap.xml location

## Search Console Submission

### Google Search Console
1. Visit [Google Search Console](https://search.google.com/search-console)
2. Add property for `https://www.jtdub.com`
3. Submit sitemap: `https://www.jtdub.com/sitemap.xml`
4. Monitor indexing status and coverage

### Bing Webmaster Tools
1. Visit [Bing Webmaster Tools](https://www.bing.com/webmasters)
2. Add site: `https://www.jtdub.com`
3. Submit sitemap: `https://www.jtdub.com/sitemap.xml`
4. Configure crawl settings

## Footer Links
- Sitemap and RSS links added to footer for easy discovery
- Uses Bootstrap icons for visual consistency
- Responsive design maintains accessibility across devices

## Structured Data
- Homepage: Person schema for James Williams
- Publications: ScholarlyArticle schema for research papers
- Enhances search result rich snippets

## Testing
- Test sitemap accessibility: `curl https://www.jtdub.com/sitemap.xml`
- Test RSS feed: `curl https://www.jtdub.com/feed.xml`
- Validate with Google's Rich Results Test
- Check Google Search Console for indexing status
