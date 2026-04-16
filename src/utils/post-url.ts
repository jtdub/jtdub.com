import type { CollectionEntry } from 'astro:content';

const POST_ID_RE = /^(\d{4})-(\d{2})-(\d{2})-(.+)$/;

export function parsePostId(id: string) {
  const match = id.match(POST_ID_RE);
  if (!match) {
    throw new Error(`Post id does not match YYYY-MM-DD-slug pattern: ${id}`);
  }
  const [, year, month, day, slug] = match;
  return { year, month, day, slug };
}

// Matches old Jekyll permalinks exactly.
export function postUrl(post: CollectionEntry<'posts'>): string {
  const { year, month, day, slug } = parsePostId(post.id);
  return `/${year}/${month}/${day}/${slug}`;
}
