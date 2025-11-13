# Rust Project Conventions

## Directory Structure

```
project-name/
├── src/
│   ├── main.rs (for binaries)
│   ├── lib.rs (for libraries)
│   └── api/ (modules for API projects)
├── tests/
│   └── integration_test.rs
├── .gitignore
├── .pre-commit-config.yaml
├── Cargo.toml
├── Cargo.lock (committed)
├── README.md
├── Dockerfile (if needed)
└── docker-compose.yml (if needed)
```

## Cargo.toml Structure

Standard sections:
- `[package]` - name, version, edition (2021), authors
- `[dependencies]` - runtime dependencies
- `[dev-dependencies]` - test/bench dependencies
- `[profile.release]` - optimization settings

Common optimizations:
```toml
[profile.release]
lto = true
codegen-units = 1
strip = true
```

## Pre-commit Hooks

Standard Rust pre-commit hooks:
- `cargo fmt` for formatting
- `cargo clippy` for linting
- `cargo check` for compilation check (optional, slower)

## Linting & Formatting

- **Formatter**: rustfmt (built-in)
- **Linter**: clippy (built-in)
- No additional config needed for basics

## Docker Considerations

Multi-stage builds are essential for Rust:
1. Builder stage with full toolchain
2. Runtime stage with minimal base (distroless or alpine)
3. Copy only the compiled binary
4. Results in tiny final images (~10MB vs ~2GB)

Cache optimization:
- Build dependencies first (separate layer)
- Then build application code
