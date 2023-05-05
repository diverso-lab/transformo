clean_drupal:
	@echo "Cleaning Drupal..."
	cd auto-drupal && docker-compose down -v
	cd ..
	rm -rf auto-drupal
	@echo "Done."

clean_wordpress:
	@echo "Cleaning wordPress..."
	cd auto-wp && docker-compose down -v
	cd ..
	rm -rf auto-wp
	@echo "Done."

prepare_drupal:
	git clone https://github.com/drorganvidez/auto-drupal
	cd auto-drupal && make prepare

install_drupal:
	cd auto-drupal && make autoinstall

prepare_wordpress:
	git clone https://github.com/drorganvidez/auto-wp

install_wordpress:
	cd auto-wp && make autoinstall

up:
	cd auto-drupal && docker compose up -d
	cd ..
	cd
	cd auto-wp && docker compose up -d

down:
	cd auto-drupal && docker compose down
	cd ..
	cd
	cd auto-wp && docker compose down
