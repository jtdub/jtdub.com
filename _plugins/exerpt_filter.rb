module Jekyll
  module ExcerptFilter
    def custom_excerpt(input, length)
      # Remove HTML tags including images
      input = input.gsub(/<img[^>]*>/, '')
      input = input.gsub(/<[^>]*>/, '')

      # Truncate to the specified number of words
      words = input.split(' ')
      if words.length > length
        words[0...length].join(' ') + '...'
      else
        input
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::ExcerptFilter)

