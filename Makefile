check:
	python3 tools/validate_opcode_table.py
	python3 tools/validate_compliance_tests.py

generate:
	python3 tools/generate_instruction_docs.py

clean:
	rm -rf .pytest_cache
