.PHONY: install clean build serve serve-all test doctor

.direnv:
	direnv allow
	direnv reload

install: .direnv

clean:
	rm -rf .direnv
	rm -rf _site
	rm -f Gemfile.lock

build: install
	jekyll build

serve: install
	jekyll serve --watch

serve-all: install
	jekyll serve --watch --host 0.0.0.0

test: build
	htmlproofer --check-html --check-img-http --check-opengraph --check-sri ./_site

doctor: build
	jekyll doctor --config _config.yml,_doctor_config.yml
