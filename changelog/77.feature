Update Jekyll and Ruby dependencies to resolve compatibility issues and improve build reliability

- Updated Jekyll from 4.2.0 to 4.2.2 for better stability
- Updated jekyll-feed from 0.12 to 0.15 for enhanced RSS functionality  
- Updated jekyll-redirect-from to 0.16 for improved redirects
- Updated webrick from 1.7 to 1.8 for better local development
- Fixed Liquid template date comparison syntax for Jekyll 4.2+ compatibility
- Updated GitHub Actions to use actions/checkout@v4 and ruby/setup-ruby@v1
- Modernized GitHub Actions workflow with proper Ruby setup and caching
- Updated Docker Compose to use Jekyll 4.2.2 image
- Added .ruby-version file to specify Ruby 2.7.0 requirement
- Fixed template syntax in study and archive pages to prevent build failures
