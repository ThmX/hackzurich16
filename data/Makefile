files=$(wildcard *_raw.json)
newfiles=$(files:%_raw.json=%.json)

all: $(newfiles) $(files)

%.json: %_raw.json
	python3 ../utils/sanitize_json.py $^ $@

clean: 
	rm 