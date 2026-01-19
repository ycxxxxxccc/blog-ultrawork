/**
 * Calculate reading time based on content length
 * Average reading speed: 200 words per minute
 * @param content - The content to calculate reading time for
 * @returns Reading time in minutes
 */
export function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const words = content.trim().split(/\s+/).length;
  return Math.ceil(words / wordsPerMinute);
}

/**
 * Format date to a readable string
 * @param date - Date to format
 * @param locale - Locale for formatting (default: 'en-US')
 * @returns Formatted date string
 */
export function formatDate(date: Date, locale: string = "en-US"): string {
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
}

/**
 * Format date to ISO string
 * @param date - Date to format
 * @returns ISO string
 */
export function formatDateISO(date: Date): string {
  return date.toISOString();
}

/**
 * Get all unique tags from blog posts
 * @param posts - Array of blog posts
 * @returns Array of unique tags sorted alphabetically
 */
export function getAllTags(
  posts: Array<{ data: { tags?: string[] } }>
): string[] {
  const tags = new Set<string>();
  posts.forEach((post) => {
    post.data.tags?.forEach((tag) => tags.add(tag));
  });
  return Array.from(tags).sort();
}

/**
 * Get all unique categories from blog posts
 * @param posts - Array of blog posts
 * @returns Array of unique categories sorted alphabetically
 */
export function getAllCategories(
  posts: Array<{ data: { category?: string } }>
): string[] {
  const categories = new Set<string>();
  posts.forEach((post) => {
    if (post.data.category) {
      categories.add(post.data.category);
    }
  });
  return Array.from(categories).sort();
}

/**
 * Get related posts based on tags and category
 * @param currentPost - Current post
 * @param allPosts - All blog posts
 * @param limit - Maximum number of related posts to return
 * @returns Array of related posts
 */
export function getRelatedPosts<
  T extends { data: { tags?: string[]; category?: string } },
>(currentPost: T, allPosts: T[], limit: number = 3): T[] {
  const currentTags = currentPost.data.tags || [];
  const currentCategory = currentPost.data.category;

  const scored = allPosts
    .filter((post) => post !== currentPost)
    .map((post) => {
      let score = 0;
      const postTags = post.data.tags || [];

      // Score based on matching tags
      const matchingTags = currentTags.filter((tag) =>
        postTags.includes(tag)
      ).length;
      score += matchingTags * 2;

      // Score based on matching category
      if (currentCategory && post.data.category === currentCategory) {
        score += 3;
      }

      return { post, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return scored.map((item) => item.post);
}

/**
 * Truncate text to a specified length
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @returns Truncated text
 */
export function truncateText(text: string, maxLength: number = 150): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength).trim() + "...";
}
