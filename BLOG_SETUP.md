# Blog Setup Guide

Your blog system is now fully set up! Here's how it works and how to create new posts.

## Quick Start

**Your blog files are located in:** `/Users/o/Desktop/웹사이트/dongjae0324.github.io/blog/`

Currently available blog posts:
1. ✅ `understanding-diffusion-models.html`
2. ✅ `safety-privacy-generative-models.html`
3. ✅ `efficient-training-strategies.html`

## How Blog Posts Are Structured

Each blog post is a **complete, standalone HTML file** with:
- Full HTML structure (head, body, navigation)
- Styling (CSS embedded in the file)
- Back link to return to main page
- Professional navigation bar

## Creating a New Blog Post

### Option 1: Copy and Edit an Existing Post (Recommended)

1. **Copy a template file:**
```bash
cp blog/understanding-diffusion-models.html blog/your-post-title.html
```

2. **Edit the new file** with your content:
   - Change `<title>` tag: `Your Title - Dongjae Jeon`
   - Change `<h1 class="post-title">`: Your blog post title
   - Change `<div class="post-meta">`: Publication date (e.g., "January 2026")
   - Replace content in `<div class="post-content">`: Your actual post content

3. **Structure your content** with HTML tags:
```html
<h2>Section Title</h2>
<p>Paragraph text here...</p>

<h3>Subsection Title</h3>
<ul>
    <li>Bullet point 1</li>
    <li>Bullet point 2</li>
</ul>

<p>More text with <strong>bold</strong> or <em>italic</em> text.</p>

<pre><code>
Code block example
</code></pre>
```

### Option 2: Create From Scratch

Copy the basic template below and save as `blog/your-post.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Post Title - Dongjae Jeon</title>
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    <style>
        /* Copy the entire <style> section from an existing blog post */
    </style>
</head>
<body>
    <!-- Copy the <nav> section from an existing blog post -->
    
    <div class="container">
        <article class="blog-post">
            <a href="../index.html#blog" class="back-link">← Back to blog</a>
            
            <div class="post-header">
                <h1 class="post-title">Your Post Title</h1>
                <div class="post-meta">Published on Month Year</div>
            </div>
            
            <div class="post-content">
                <!-- Your content here -->
                <p>Start typing your blog post content here...</p>
            </div>
        </article>
    </div>
    
    <!-- Copy the <footer> section from an existing blog post -->
</body>
</html>
```

## Adding Links to Your Homepage

Once you create a new blog post HTML file, update `build.py` to link it on your homepage:

### Step 1: Open build.py

Find the `get_blog_html()` function (around line 353).

### Step 2: Add your post to the posts list

```python
posts = [
    {
        'title': 'Understanding Diffusion Models: A Deep Dive',
        'date': 'Jan 2026',
        'excerpt': 'An introduction to score-based diffusion models...',
        'url': 'blog/understanding-diffusion-models.html'
    },
    {
        'title': 'Your New Post Title',  # ← Add your post here
        'date': 'Jan 2026',
        'excerpt': 'A short preview/description of your post...',
        'url': 'blog/your-post-slug.html'
    }
]
```

### Step 3: Regenerate the homepage

```bash
cd /Users/o/Desktop/웹사이트/dongjae0324.github.io
python build.py
```

This updates `index.html` with your new blog link.

## Publishing to GitHub

After creating your blog post:

```bash
# Navigate to your project directory
cd /Users/o/Desktop/웹사이트/dongjae0324.github.io

# Stage your changes
git add blog/*.html build.py index.html

# Commit with a descriptive message
git commit -m "Add blog post: Your Post Title"

# Push to GitHub
git push origin main
```

Your blog post will be live at:
```
https://dongjae0324.github.io/blog/your-post-slug.html
```

## Content Formatting Guide

### Headings
```html
<h2>Main Section Title</h2>
<h3>Subsection Title</h3>
```

### Text Formatting
```html
<strong>bold text</strong>
<em>italic text</em>
<code>inline code</code>
```

### Lists
```html
<ul>
    <li>Unordered list item 1</li>
    <li>Unordered list item 2</li>
</ul>

<ol>
    <li>Ordered list item 1</li>
    <li>Ordered list item 2</li>
</ol>
```

### Code Blocks
```html
<pre><code>
function hello() {
    console.log("Hello, World!");
}
</code></pre>
```

### Links
```html
<a href="https://example.com" target="_blank">Link text</a>
```

## Example Blog Post Structure

Here's a good template for organizing a blog post:

```html
<div class="post-content">
    <p>Brief introduction paragraph...</p>
    
    <h2>Problem Statement</h2>
    <p>Explain the problem you're addressing...</p>
    
    <h2>Main Section 1</h2>
    <p>Key points and discussion...</p>
    <h3>Subsection 1.1</h3>
    <p>More details...</p>
    
    <h2>Main Section 2</h2>
    <ul>
        <li>Point 1</li>
        <li>Point 2</li>
    </ul>
    
    <h2>Conclusion</h2>
    <p>Summary and takeaways...</p>
</div>
```

## File Organization

```
dongjae0324.github.io/
├── blog/
│   ├── understanding-diffusion-models.html
│   ├── safety-privacy-generative-models.html
│   ├── efficient-training-strategies.html
│   └── your-new-post.html          ← Your new posts go here
├── build.py                        ← Update this to link new posts
├── index.html                      ← Auto-generated, don't edit
└── BLOG_SETUP.md                   ← This file
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Blog post doesn't show on homepage | 1. Check post is added to `build.py` 2. Run `python build.py` 3. Check file path is correct |
| Navigation links don't work | Make sure relative paths are correct: `../index.html#blog` |
| Styling looks wrong | Copy the entire `<style>` section from an existing post |
| Post shows 404 error | Check file name matches exactly (case-sensitive) in `build.py` |

## Quick Commands

```bash
# Navigate to project
cd /Users/o/Desktop/웹사이트/dongjae0324.github.io

# Regenerate homepage (after updating build.py)
python build.py

# Check git status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message here"

# Push to GitHub
git push origin main
```

## Tips for Good Blog Posts

✅ **Do:**
- Write clear, descriptive titles
- Include a brief excerpt for the homepage
- Use proper heading hierarchy (h2, h3)
- Break up long paragraphs
- Use code blocks for technical content
- Link to relevant resources

❌ **Avoid:**
- Very long paragraphs (break them up)
- Inconsistent formatting
- Too many different heading levels
- Large images without optimization
- Broken links

## Need Help?

All three example posts are already created and can serve as templates:
1. `understanding-diffusion-models.html` - Technical tutorial style
2. `safety-privacy-generative-models.html` - Research-focused style
3. `efficient-training-strategies.html` - How-to guide style

Feel free to copy their structure and HTML for your own posts!
