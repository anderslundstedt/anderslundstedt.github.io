.PHONY: install update clean serve

install: .direnv/bin/github-pages

update: install
	bundle update

clean:
	rm -rf .direnv
	rm -rf _site
	rm -f Gemfile.lock

serve: install
	jekyll serve --watch

.direnv/bin/github-pages:
	bundle install
