# Makefile for Wagtail-WordPress Connector

# Constants
WORDPRESS_ROOT = wordpress.docker
WORDPRESS_URL = http://localhost:8888
WORDPRESS_API = wp-json/wp/v2
DC = docker-compose

# Help command
.PHONY: help
help:
	@echo "Wagtail-WordPress Connector Commands"
	@echo ""
	@echo "WordPress Container Commands:"
	@echo "  make wp-build      - Wordpress: initial setup"
	@echo "  make wp-up         - Wordpress: start the container"
	@echo "  make wp-load       - Wordpress: import the demo data"
	@echo "  make wp-down       - Wordpress: stop the container"
	@echo "  make wp-destroy    - Wordpress: destroy the container"
	@echo ""
	@echo "Wagtail Virtual Environment Commands:"
	@echo "  make wt-migrate    - Wagtail: run migrations"
	@echo "  make wt-superuser  - Wagtail: create superuser"
	@echo "  make wt-run        - Wagtail: run the server"
	@echo "  make wt-fixtree    - Wagtail: fix the tree"
	@echo ""
	@echo "Django Import Commands:"
	@echo "  make import-authors    - Django: import authors from wordpress"
	@echo "  make import-categories - Django: import categories from wordpress"
	@echo "  make import-tags       - Django: import tags from wordpress"
	@echo "  make import-pages      - Django: import pages from wordpress"
	@echo "  make import-posts      - Django: import posts from wordpress"
	@echo "  make import-media      - Django: import media from wordpress"
	@echo "  make import-comments   - Django: import comments from wordpress"
	@echo "  make import-all        - Django: import all data from wordpress"
	@echo ""
	@echo "Node.js Commands:"
	@echo "  make node-setup         - Install Node.js dependencies"
	@echo "  make node-build         - Build all frontend assets for production"
	@echo "  make node-start         - Start the frontend development server"
	@echo "  make node-styles        - Compile CSS styles"
	@echo "  make node-styles-watch  - Watch and compile CSS styles"
	@echo "  make node-scripts       - Compile JavaScript"
	@echo "  make node-scripts-watch - Watch and compile JavaScript"
	@echo ""
	@echo "Convenience Commands:"
	@echo "  make start     - Run all commands to set up and start the development environment"
	@echo "  make stop      - Stop all running services"
	@echo "  make destroy   - Destroy and cleanup wordpress and wagtail"

# WordPress Commands
.PHONY: wp-build
wp-build:
	@echo "WordPress: initial setup"
	@if [ ! -f "$(WORDPRESS_ROOT)/.env" ]; then \
		cp $(WORDPRESS_ROOT)/.env.example $(WORDPRESS_ROOT)/.env; \
	fi
	@mkdir -p $(WORDPRESS_ROOT)/wp-content/plugins
	@cd $(WORDPRESS_ROOT)/wp-content/plugins && \
	if [ ! -d "wp-graphql-offset-pagination" ]; then \
		git clone https://github.com/valu-digital/wp-graphql-offset-pagination.git; \
	else \
		echo "Plugin wp-graphql-offset-pagination already exists"; \
	fi

.PHONY: wp-up
wp-up:
	@echo "WordPress: start the container"
	@cd $(WORDPRESS_ROOT) && $(DC) up -d

.PHONY: wp-down
wp-down:
	@echo "WordPress: stop the container"
	@cd $(WORDPRESS_ROOT) && $(DC) down

.PHONY: wp-destroy
wp-destroy:
	@echo "WordPress: destroy the container"
	@cd $(WORDPRESS_ROOT) && $(DC) down --volumes
	@echo "Do you want to clean up the files? (y/n)"
	@read cleanup; \
	if [ "$$cleanup" = "y" ]; then \
		if [ -f "$(WORDPRESS_ROOT)/.env" ]; then \
			rm $(WORDPRESS_ROOT)/.env; \
			echo "Removed .env file"; \
		fi; \
		if [ -d "$(WORDPRESS_ROOT)/wp-content" ]; then \
			rm -rf $(WORDPRESS_ROOT)/wp-content; \
			echo "Removed wp-content directory"; \
		fi; \
		if [ -d "$(WORDPRESS_ROOT)/xml" ]; then \
			rm -rf $(WORDPRESS_ROOT)/xml; \
			echo "Removed xml directory"; \
		fi; \
		if [ -f "db.sqlite3" ]; then \
			rm -rf db.sqlite3; \
			echo "Removed wagtail database"; \
		fi; \
	fi

.PHONY: wp-load
wp-load:
	@echo "WordPress: import the demo data"
	@if [ -z "$$(cd $(WORDPRESS_ROOT) && $(DC) ps | grep wordpress)" ]; then \
		$(MAKE) wp-up; \
	fi
	@cd $(WORDPRESS_ROOT) && $(DC) exec -T wordpress bin/init.sh

# Wagtail/Django Commands
.PHONY: wt-migrate
wt-migrate:
	@echo "Wagtail: run migrations"
	uv run manage.py migrate

.PHONY: wt-superuser
wt-superuser:
	@echo "Wagtail: create superuser"
	uv run manage.py createsuperuser

.PHONY: wt-run
wt-run:
	@echo "Wagtail: run the server"
	uv run manage.py runserver

.PHONY: wt-fixtree
wt-fixtree:
	@echo "Wagtail: fix the tree"
	uv run manage.py fixtree

# Import Commands
.PHONY: import-authors
import-authors:
	@echo "Django: import authors from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/users WPAuthor

.PHONY: import-categories
import-categories:
	@echo "Django: import categories from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/categories WPCategory

.PHONY: import-tags
import-tags:
	@echo "Django: import tags from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/tags WPTag

.PHONY: import-pages
import-pages:
	@echo "Django: import pages from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/pages WPPage

.PHONY: import-posts
import-posts:
	@echo "Django: import posts from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/posts WPPost

.PHONY: import-media
import-media:
	@echo "Django: import media from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/media WPMedia

.PHONY: import-comments
import-comments:
	@echo "Django: import comments from wordpress"
	uv run manage.py import $(WORDPRESS_URL)/$(WORDPRESS_API)/comments WPComment

.PHONY: import-all
import-all: import-authors import-categories import-tags import-pages import-posts import-media import-comments
	@echo "Imported all WordPress data"

# Convenience Commands
.PHONY: start
start: wp-build wp-up wp-load wt-migrate wt-superuser import-all wt-run
	@echo "Development environment started"

.PHONY: stop
stop: wp-down
	@echo "Development environment stopped"
	@echo "Note: There is no direct equivalent for 'dj stop' and 'wt stop' in the CLI, but WordPress container has been stopped."

.PHONY: destroy
destroy: wp-destroy
	@echo "Development environment destroyed"

# Node.js Commands
.PHONY: node-setup
node-setup:
	@echo "Installing Node.js dependencies"
	@npm install

.PHONY: node-build
node-build:
	@echo "Building frontend assets"
	@npm run build

.PHONY: node-start
node-start:
	@echo "Starting the frontend development server"
	@npm start

.PHONY: node-styles
node-styles:
	@echo "Compiling CSS styles"
	@npm run styles

.PHONY: node-styles-watch
node-styles-watch:
	@echo "Watching and compiling CSS styles"
	@npm run styles:watch

.PHONY: node-scripts
node-scripts:
	@echo "Compiling JavaScript"
	@npm run scripts

.PHONY: node-scripts-watch
node-scripts-watch:
	@echo "Watching and compiling JavaScript"
	@npm run scripts:watch
