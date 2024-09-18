# Makefile

start:
	@echo "Starting Docker containers..."
	@docker-compose up -d

	@echo "Waiting for Redis to be ready..."
	@while ! nc -z localhost 6379; do \
		sleep 1; \
	done

	@echo "Redis is ready. Running the Python application..."
	@python3 run.py

stop:
	@echo "Stopping Docker containers..."
	@docker-compose down

restart:
	@echo "Restarting the application..."
	@docker-compose down
	@make start
