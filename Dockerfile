FROM jekyll/builder:latest
COPY _site .
CMD ["jekyll", "serve"]
