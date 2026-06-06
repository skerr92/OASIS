# OASIS-16 v0.2 Draft Release Notes

Status: draft notes for the first official OASIS-16 release.

OASIS-16 v0.2 promotes the Base-16 and Base-16T work from experimental bring-up
to a documented implementation and toolchain contract.

## Highlights

- Base-16 absolute data-memory operands use `addr12`, expanding the baseline
  data-memory address space to 4096 words.
- Base-16T remains the 16-bit compiler/toolchain profile and keeps the existing
  class `00` compiler-facing instruction set stable.
- The freestanding Base-16T C ABI is documented, including register roles,
  calling convention, stack-frame layout, and linker/runtime symbols.
- Initial freestanding C++ support is documented for compile/link smoke testing:
  explicit guard-helper calls, pure-virtual abort handling, init/fini range
  symbols, and heapless weak `new`/`delete` hooks.
- Init/fini range symbols are required, but automatic constructor/destructor
  execution is optional platform runtime behavior in v0.2.
- Compliance coverage now includes v0.2 memory addressing, runtime exit/debug
  observation, ABI stack-frame behavior, and runtime/linker symbol expectations.
- External-memory-control guidance defines memory-mapped IO as the portable
  baseline while leaving dedicated peripheral instructions as optional
  extensions.

## Compatibility

The archived OASIS v0.1 specification remains the compatibility reference for
v0.1 implementations. OASIS-16 v0.2 keeps v0.1 instruction meanings stable, but
current topic pages and generated metadata define the updated `addr12`, ABI,
runtime, and compliance expectations for v0.2 claims.

Implementations moving from v0.1 to v0.2 should review:

- [../spec/memory-model.md](../spec/memory-model.md)
- [../spec/base16t.md](../spec/base16t.md)
- [../spec/abi.md](../spec/abi.md)
- [conformance-report-template.md](conformance-report-template.md)

## Toolchain Artifacts

The Linux toolchain installer and source/compliance package are produced by
GitHub Actions on release-producing refs. Darwin arm64 toolchain artifacts are
release-manager built on local Apple Silicon hardware because the current
toolchain build is not reliable on GitHub-hosted macOS runners.

For Darwin arm64 releases, build and validate locally:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16-darwin-arm64" \
  --gcc-src "$PWD/.build/sources/gcc-14.3.0" \
  --binutils-src "$PWD/.build/sources/binutils-2.46.0" \
  --jobs 4 \
  --clean \
  --force \
  --run-tests

toolchain/scripts/package-toolchain-installer.sh \
  --prefix "$PWD/.toolchain/oasis16-darwin-arm64" \
  --name oasis16-toolchain-v0.2-darwin-arm64 \
  --output "$PWD/.build/artifacts/oasis16-toolchain-v0.2-darwin-arm64.tar.gz"
```

Attach the Darwin arm64 archive to the release manually alongside the Actions
artifacts.

## Non-Goals

OASIS-16 v0.2 does not require hosted libc, full libstdc++, threads, dynamic
linking, operating-system ABIs, exceptions, RTTI, new required peripheral
instructions, automatic constructor/destructor execution in the default startup
object, or OASIS-32 implementation support.

## Remaining Release Decisions

- Finalize release artifact names and checksums.
