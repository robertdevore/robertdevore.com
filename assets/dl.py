import requests
import os
import json
from urllib.parse import urlparse, urljoin
from pathlib import Path
import time
import re
from bs4 import BeautifulSoup

class WordPressContentImageDownloader:
    def __init__(self, site_url, images_folder="images"):
        self.site_url = site_url.rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.images_folder = Path(images_folder)
        self.session = requests.Session()
        
        # Create images folder if it doesn't exist
        self.images_folder.mkdir(exist_ok=True)
        
        # Set headers to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Track downloaded images to avoid duplicates
        self.downloaded_images = set()
        # Track filenames to handle duplicates
        self.used_filenames = set()
    
    def get_all_posts(self):
        """Retrieve all posts from the WordPress site"""
        posts = []
        page = 1
        per_page = 100  # WordPress default max is 100
        
        print(f"Fetching posts from {self.site_url}...")
        
        while True:
            try:
                response = self.session.get(
                    f"{self.api_base}/posts",
                    params={
                        'page': page,
                        'per_page': per_page,
                        '_embed': False  # We don't need embedded data for content images
                    }
                )
                response.raise_for_status()
                
                page_posts = response.json()
                
                if not page_posts:
                    break
                
                posts.extend(page_posts)
                print(f"Retrieved {len(page_posts)} posts from page {page}")
                
                # Check if there are more pages
                total_pages = int(response.headers.get('X-WP-TotalPages', 1))
                if page >= total_pages:
                    break
                
                page += 1
                time.sleep(0.5)  # Be respectful to the server
                
            except requests.RequestException as e:
                print(f"Error fetching posts on page {page}: {e}")
                break
        
        print(f"Total posts retrieved: {len(posts)}")
        return posts
    
    def extract_images_from_content(self, content_html, post_title, post_id):
        """Extract all image URLs from post content HTML"""
        if not content_html:
            return []
        
        image_urls = []
        
        # Parse HTML content
        soup = BeautifulSoup(content_html, 'html.parser')
        
        # Find all img tags
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src')
            if not src:
                continue
            
            # Convert relative URLs to absolute URLs
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = urljoin(self.site_url, src)
            elif not src.startswith(('http://', 'https://')):
                src = urljoin(self.site_url, src)
            
            # Get alt text for better filename
            alt_text = img.get('alt', '')
            
            # Get additional attributes
            img_class = img.get('class', [])
            img_id = img.get('id', '')
            
            image_info = {
                'url': src,
                'post_title': post_title,
                'post_id': post_id,
                'alt_text': alt_text,
                'img_class': img_class,
                'img_id': img_id
            }
            
            image_urls.append(image_info)
        
        # Also look for images in WordPress blocks (Gutenberg)
        block_images = self.extract_block_images(content_html, post_title, post_id)
        image_urls.extend(block_images)
        
        # Look for images in shortcodes
        shortcode_images = self.extract_shortcode_images(content_html, post_title, post_id)
        image_urls.extend(shortcode_images)
        
        return image_urls
    
    def extract_block_images(self, content_html, post_title, post_id):
        """Extract images from WordPress Gutenberg blocks"""
        images = []
        
        # Look for WordPress image blocks
        # These often contain JSON-like data or specific patterns
        block_patterns = [
            r'wp:image.*?"url":"([^"]+)"',
            r'wp:gallery.*?"url":"([^"]+)"',
            r'wp:cover.*?"url":"([^"]+)"'
        ]
        
        for pattern in block_patterns:
            matches = re.findall(pattern, content_html, re.IGNORECASE)
            for match in matches:
                # Decode JSON-escaped URLs
                url = match.replace('\\/', '/')
                
                # Convert to absolute URL if needed
                if url.startswith('//'):
                    url = 'https:' + url
                elif url.startswith('/'):
                    url = urljoin(self.site_url, url)
                elif not url.startswith(('http://', 'https://')):
                    url = urljoin(self.site_url, url)
                
                images.append({
                    'url': url,
                    'post_title': post_title,
                    'post_id': post_id,
                    'alt_text': '',
                    'img_class': ['wp-block-image'],
                    'img_id': ''
                })
        
        return images
    
    def extract_shortcode_images(self, content_html, post_title, post_id):
        """Extract images from WordPress shortcodes"""
        images = []
        
        # Look for common image shortcodes
        shortcode_patterns = [
            r'\[gallery[^\]]*ids="([^"]+)"',
            r'\[img[^\]]*src="([^"]+)"',
            r'\[image[^\]]*src="([^"]+)"'
        ]
        
        for pattern in shortcode_patterns:
            matches = re.findall(pattern, content_html, re.IGNORECASE)
            for match in matches:
                if 'ids=' in pattern:
                    # Handle gallery shortcode with IDs
                    ids = match.split(',')
                    for img_id in ids:
                        img_id = img_id.strip()
                        if img_id.isdigit():
                            # Fetch media by ID
                            media_url = self.get_media_url_by_id(img_id)
                            if media_url:
                                images.append({
                                    'url': media_url,
                                    'post_title': post_title,
                                    'post_id': post_id,
                                    'alt_text': '',
                                    'img_class': ['shortcode-image'],
                                    'img_id': img_id
                                })
                else:
                    # Direct URL in shortcode
                    url = match
                    if url.startswith('//'):
                        url = 'https:' + url
                    elif url.startswith('/'):
                        url = urljoin(self.site_url, url)
                    elif not url.startswith(('http://', 'https://')):
                        url = urljoin(self.site_url, url)
                    
                    images.append({
                        'url': url,
                        'post_title': post_title,
                        'post_id': post_id,
                        'alt_text': '',
                        'img_class': ['shortcode-image'],
                        'img_id': ''
                    })
        
        return images
    
    def get_media_url_by_id(self, media_id):
        """Get media URL by WordPress media ID"""
        try:
            response = self.session.get(f"{self.api_base}/media/{media_id}")
            response.raise_for_status()
            media_data = response.json()
            return media_data.get('source_url')
        except requests.RequestException:
            return None
    
    def extract_all_content_images(self, posts):
        """Extract all image URLs from all post contents"""
        all_image_urls = []
        
        print("Extracting images from post content...")
        
        for i, post in enumerate(posts, 1):
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_id = post['id']
            
            # Get post content
            content_html = post.get('content', {}).get('rendered', '')
            
            if content_html:
                images = self.extract_images_from_content(content_html, post_title, post_id)
                all_image_urls.extend(images)
                
                if images:
                    print(f"[{i}/{len(posts)}] Found {len(images)} images in: {post_title[:50]}...")
                else:
                    print(f"[{i}/{len(posts)}] No images in: {post_title[:50]}...")
            else:
                print(f"[{i}/{len(posts)}] No content in: {post_title[:50]}...")
        
        # Remove duplicates based on URL
        unique_images = []
        seen_urls = set()
        
        for img in all_image_urls:
            if img['url'] not in seen_urls:
                unique_images.append(img)
                seen_urls.add(img['url'])
        
        print(f"\nTotal images found: {len(all_image_urls)}")
        print(f"Unique images: {len(unique_images)}")
        
        return unique_images
    
    def generate_filename(self, image_info):
        """Generate a filename using the original image name"""
        url = image_info['url']
        
        # Parse URL to get original filename
        parsed_url = urlparse(url)
        original_filename = os.path.basename(parsed_url.path)
        
        # Remove any query parameters from filename
        if '?' in original_filename:
            original_filename = original_filename.split('?')[0]
        
        # If no filename found, create a basic one
        if not original_filename or original_filename == '/':
            original_filename = 'image.jpg'
        
        # Ensure the filename has an extension
        if '.' not in original_filename:
            original_filename += '.jpg'
        
        # Basic sanitization - remove any problematic characters
        filename = "".join(c for c in original_filename if c.isalnum() or c in '.-_')
        
        # Handle duplicate filenames
        if filename in self.used_filenames:
            name, ext = os.path.splitext(filename)
            counter = 1
            while f"{name}_{counter}{ext}" in self.used_filenames:
                counter += 1
            filename = f"{name}_{counter}{ext}"
        
        # Add to used filenames
        self.used_filenames.add(filename)
        
        return filename
    
    def download_image(self, image_info):
        """Download a single image"""
        url = image_info['url']
        
        try:
            # Generate filename
            filename = self.generate_filename(image_info)
            filepath = self.images_folder / filename
            
            # Skip if file already exists
            if filepath.exists():
                print(f"Skipping {filename} (already exists)")
                return True
            
            # Skip if URL already downloaded (with different filename)
            if url in self.downloaded_images:
                print(f"Skipping {filename} (URL already downloaded)")
                return True
            
            # Download the image
            print(f"Downloading: {filename}")
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Skipping {filename} (not an image: {content_type})")
                return False
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.downloaded_images.add(url)
            print(f"✓ Downloaded: {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading {url}: {e}")
            return False
    
    def download_all_images(self, image_urls):
        """Download all content images"""
        print(f"\nStarting download of {len(image_urls)} images...")
        
        successful = 0
        failed = 0
        
        for i, image_info in enumerate(image_urls, 1):
            print(f"\n[{i}/{len(image_urls)}] ", end="")
            
            if self.download_image(image_info):
                successful += 1
            else:
                failed += 1
            
            # Small delay between downloads
            time.sleep(0.3)
        
        print(f"\n\nDownload complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Images saved to: {self.images_folder.absolute()}")
    
    def run(self):
        """Main execution method"""
        try:
            # Get all posts
            posts = self.get_all_posts()
            
            if not posts:
                print("No posts found. Check your WordPress site URL.")
                return
            
            # Extract all images from post content
            image_urls = self.extract_all_content_images(posts)
            
            if not image_urls:
                print("No images found in post content.")
                return
            
            # Download all images
            self.download_all_images(image_urls)
            
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    # Configuration
    WORDPRESS_SITE_URL = input("Enter WordPress site URL (e.g., https://example.com): ").strip()
    
    if not WORDPRESS_SITE_URL:
        print("Please provide a valid WordPress site URL.")
        return
    
    # Ensure URL has protocol
    if not WORDPRESS_SITE_URL.startswith(('http://', 'https://')):
        WORDPRESS_SITE_URL = 'https://' + WORDPRESS_SITE_URL
    
    print(f"Starting content image download from: {WORDPRESS_SITE_URL}")
    
    # Create downloader and run
    downloader = WordPressContentImageDownloader(WORDPRESS_SITE_URL)
    downloader.run()

if __name__ == "__main__":
    main()