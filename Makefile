.PHONY: build run clean

build:
	cd backend && cargo build --release

run: build
	python3 gui/main.py

clean:
	rm -rf backend/target
	rm -rf notes/*.ghost
	rm -rf notes/*.cali
