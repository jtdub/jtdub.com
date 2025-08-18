#!/usr/bin/env python3
"""
Image Optimization Script
Automatically converts <img> tags to optimized {% include optimized_image.html %} includes
"""

import os
import re
import glob
from pathlib import Path

def extract_img_attributes(img_tag):
    """Extract attributes from an img tag"""
    attrs = {}
    
    # Extract src
    src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
    if src_match:
        attrs['src'] = src_match.group(1)
    
    # Extract alt (if present)
    alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag)
    if alt_match:
        attrs['alt'] = alt_match.group(1)
    
    # Extract width (if present)
    width_match = re.search(r'width=["\']?(\d+)["\']?', img_tag)
    if width_match:
        attrs['width'] = width_match.group(1)
    
    # Extract height (if present)
    height_match = re.search(r'height=["\']?(\d+)["\']?', img_tag)
    if height_match:
        attrs['height'] = height_match.group(1)
    
    return attrs

def generate_alt_text(src_url, context=""):
    """Generate meaningful alt text based on image URL and context"""
    if 'imagedelivery.net' in src_url:
        # These are likely photography/documentation images
        if 'spring-lake' in context.lower():
            return "Underwater scene at Spring Lake"
        elif 'blue-lagoon' in context.lower():
            return "Underwater diving scene at Blue Lagoon"
        elif 'sibinacocha' in context.lower():
            return "High-altitude lake Sibinacocha in Peru"
        elif any(word in context.lower() for word in ['cisco', 'router', 'network', 'mpls', 'ospf']):
            return "Network diagram or configuration screenshot"
        elif 'grub' in context.lower():
            return "Boot menu configuration screenshot"
        else:
            return "Image related to the article content"
    else:
        return "Illustration or diagram"

def convert_img_to_include(img_tag, context=""):
    """Convert an img tag to optimized include"""
    attrs = extract_img_attributes(img_tag)
    
    if 'src' not in attrs:
        return img_tag  # Return unchanged if no src
    
    # Generate alt text if missing
    if 'alt' not in attrs or not attrs['alt']:
        attrs['alt'] = generate_alt_text(attrs['src'], context)
    
    # Build the include tag
    include_parts = [
        '{% include optimized_image.html',
        f'   src="{attrs["src"]}"',
        f'   alt="{attrs["alt"]}"'
    ]
    
    if 'width' in attrs:
        include_parts.append(f'   width="{attrs["width"]}"')
    
    if 'height' in attrs:
        include_parts.append(f'   height="{attrs["height"]}"')
    
    # Add lazy loading by default
    include_parts.append('   loading="lazy" %}')
    
    return '\n'.join(include_parts)

def process_markdown_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title/context for better alt text generation
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        context = title_match.group(1) if title_match else ""
        
        # Find all img tags
        img_pattern = r'<img[^>]*/?>'
        img_tags = re.findall(img_pattern, content)
        
        if not img_tags:
            return False  # No images to process
        
        print(f"Processing {file_path} - found {len(img_tags)} images")
        
        # Replace each img tag
        updated_content = content
        for img_tag in img_tags:
            include_tag = convert_img_to_include(img_tag, context)
            updated_content = updated_content.replace(img_tag, include_tag)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files"""
    # Get all markdown files in _posts directory
    posts_dir = Path('_posts')
    markdown_files = glob.glob(str(posts_dir / '*.md'))
    
    print(f"Found {len(markdown_files)} markdown files to check")
    
    processed_count = 0
    updated_count = 0
    
    for file_path in markdown_files:
        processed_count += 1
        if process_markdown_file(file_path):
            updated_count += 1
    
    print(f"\nCompleted processing {processed_count} files")
    print(f"Updated {updated_count} files with image optimizations")

if __name__ == "__main__":
    main()
