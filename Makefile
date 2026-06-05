check:
	python3 tools/validate_opcode_table.py
	python3 tools/validate_register_table.py
	python3 tools/validate_instruction_docs.py
	python3 tools/validate_compliance_tests.py
	python3 tools/test_assembler.py
	python3 tools/test_elf2img.py
	python3 tools/test_toolchain_scaffold.py
	python3 tools/validate_gcc_backend.py
	python3 tools/validate_binutils_backend.py

generate:
	python3 tools/generate_instruction_docs.py
	python3 tools/generate_toolchain_metadata.py

assemble-example:
	python3 tools/oasis_asm.py examples/base16/add_store.oas -o examples/base16/add_store.mem

program-image-example:
	python3 tools/oasis_program_image.py examples/base16/add_store.oas -o examples/base16/add_store.dap16
	python3 tools/oasis_program_image.py examples/base16/add_store.oas --format spi16-hex -o examples/base16/add_store.spi16

clean:
	rm -rf .pytest_cache examples/base16/add_store.mem examples/base16/add_store.dap16 examples/base16/add_store.spi16 toolchain/generated
