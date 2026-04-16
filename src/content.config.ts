import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    author: z.string().optional(),
    tags: z.array(z.string()).default([]),
    zone: z.enum(['field', 'engineering', 'essays']).default('field'),
    description: z.string().optional(),
    external_url: z.string().url().optional(),
  }),
});

export const collections = { posts };
