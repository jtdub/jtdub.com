import type { CollectionEntry } from 'astro:content';

/**
 * Given a post collection entry, return the public URL.
 * Post IDs are in the Jekyll shape `YYYY-MM-DD-slug`; the live URL is
 * `/YYYY/MM/DD/slug/`, matching the old Jekyll permalinks exactly.
 */
export function postUrl(post: CollectionEntry<'posts'>): string {
  const match = post.id.match(/^(\d{4})-(\d{2})-(\d{2})-(.+)$/);
  if (!match) {
    throw new Error(`Post id does not match YYYY-MM-DD-slug pattern: ${post.id}`);
  }
  const [, year, month, day, slug] = match;
  return `/${year}/${month}/${day}/${slug}`;
}
