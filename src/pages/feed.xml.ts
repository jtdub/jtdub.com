import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import { postUrl } from '../utils/post-url';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime(),
  );

  return rss({
    title: 'James Williams',
    description:
      'Software engineer by profession. Anthropologist by education. Field notes, engineering writing, and everything between.',
    site: context.site ?? 'https://www.jtdub.com',
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description,
      link: postUrl(post),
      categories: post.data.tags,
    })),
    customData: `<language>en-us</language>`,
  });
}
