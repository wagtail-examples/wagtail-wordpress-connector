# Default target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo " Import commands"
	@echo "  authors	Import authors from WordPress"
	@echo "  categories	Import categories from WordPress"
	@echo "  tags		Import tags from WordPress"
	@echo "  pages		Import pages from WordPress"
	@echo "  posts		Import posts from WordPress"
	@echo "  media		Import media from WordPress"
	@echo "  comments	Import comments from WordPress"
	@echo "  all		Import all data from WordPress"

.PHONY: authors
authors:
		python manage.py import http://localhost:8888/wp-json/wp/v2/users WPAuthor

.PHONY: categories
categories:
		python manage.py import http://localhost:8888/wp-json/wp/v2/categories WPCategory

.PHONY: tags
tags:
		python manage.py import http://localhost:8888/wp-json/wp/v2/tags WPTag

.PHONY: pages
pages:
		python manage.py import http://localhost:8888/wp-json/wp/v2/pages WPPage

.PHONY: posts
posts:
		python manage.py import http://localhost:8888/wp-json/wp/v2/posts WPPost

.PHONY: media
media:
		python manage.py import http://localhost:8888/wp-json/wp/v2/media WPMedia

.PHONY: comments
comments:
		python manage.py import http://localhost:8888/wp-json/wp/v2/comments WPComment

.PHONY: all
all: authors categories tags pages posts media comments
		@echo "All done"
