.PHONY: install update clean build serve

install: .direnv/bin/github-pages

update: install
	bundle update

clean:
	rm -rf .direnv
	rm -rf _site
	rm -f Gemfile.lock

build: install
	jekyll build

serve: install
	jekyll serve --watch

test: build
	htmlproofer --check-html --check-img-http --check-opengraph --check-sri ./_site

.direnv/bin/github-pages:
	bundle install
