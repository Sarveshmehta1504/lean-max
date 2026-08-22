# Per-stack locate + verify commands

Cheapest sufficient check per stack. Use the highest verification tier available (`verification.md`).

| Stack | Locate | Fast check | Real verify |
|---|---|---|---|
| **TypeScript** | `rg -n "symbol" src/` | `tsc --noEmit` | `vitest run <file>` / `jest <path>` |
| **JavaScript** | `rg -n "symbol" --type js` | `node --check f.js` | `vitest run` / `node f.js` |
| **Python** | `rg -n "def symbol\|symbol\(" ` | `python -c "import mod"` | `pytest path::test -q` |
| **Go** | `rg -n "func Symbol"` | `go vet ./...` | `go build ./... && go test ./pkg/...` |
| **Rust** | `rg -n "fn symbol"` | `cargo check` | `cargo test -p <crate>` |
| **Java** | `rg -n "class Symbol"` | `mvn -q compile` | `mvn test -Dtest=X` |
| **Ruby** | `rg -n "def symbol"` | `ruby -c f.rb` | `rspec path:LINE` |
| **PHP** | `rg -n "function symbol"` | `php -l f.php` | `phpunit --filter X` |
| **C#** | `rg -n "class Symbol"` | `dotnet build` | `dotnet test --filter X` |
| **Shell** | `rg -n "symbol()"` | `bash -n f.sh` + `shellcheck` | dry-run with `echo` prefixed |
| **SQL / migrations** | `rg -n "table_name" migrations/` | read generated SQL | run against scratch DB, then roll back |
| **Frontend/UI** | `rg -n "ComponentName"` | build passes | render the actual route; screenshot for visual claims |
| **Terraform** | `rg -n "resource \"type\""` | `terraform validate` | `terraform plan` — read it, never auto-apply |
| **Docker/K8s** | `rg -n "image:\|FROM"` | `docker build` / `kubectl --dry-run=client` | deploy to a scratch namespace |

## Universal shortcuts
- `rg -l "pattern"` — size blast radius before reading anything.
- `rg -n -B3 -A8 "pattern"` — enough context to judge without opening the file.
- `rg -n "symbol" --type-not test` — separate implementation from tests.
- `git diff --stat` / `git log --oneline -5 -- path` — what changed and why, cheaply.

## Stack-specific traps
- **TS:** `tsc` passing ≠ runtime safe. `any`, non-null `!`, and unchecked casts hide real breaks.
- **Python:** no compile step — an import error surfaces only at runtime. Always import the module.
- **Go:** the compiler catches most of it; the risk is behavioral (nil maps, goroutine leaks, shadowed err).
- **Rust:** if it compiles it mostly works — spend budget on logic, not lifetime debugging.
- **SQL:** never verify a migration by reading it. Run it.
- **Frontend:** "the build passed" is not "the page renders."
