# E2E Test Infra: Note-JS-Desktop Notion Block System

## Test Philosophy
- Opaque-box, requirement-driven. No dependency on implementation internals.
- Methodology: Category-Partition + Boundary Value Analysis + Pairwise Combinatorial Testing + Real-World Workload Testing.
- Strict regression prevention: 100% pass across all 261 existing tests with zero regressions.

## Feature Inventory
| # | Feature | Source (requirement) | Tier 1 | Tier 2 | Tier 3 |
|---|---------|---------------------|:------:|:------:|:------:|
| 1 | Atomic creation (op.set + op.listAfter) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 2 | Pure leaf nodes (content: null) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 3 | Container blocks (content: [UUID]) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 4 | Toggleable headers (format.toggleable) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 5 | Block Catalog: header_4 | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 6 | Block Catalog: to_do | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 7 | Block Catalog: quote | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 8 | Block Catalog: callout | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 9 | Block Catalog: transclusion_container | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 10 | Block Catalog: transclusion_reference | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 11 | Block Catalog: media leaves (video, audio, file, pdf) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| 12 | Block Catalog: bookmark | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |

## Test Architecture
- Test runner: `py -m unittest discover -s tests`
- Dedicated E2E suite: `tests/test_notion_transactions_and_blocks.py`
- Test case format: Isolated SQLite database fixtures, Peewee transactions, REST API and bridge contracts.
- Pass/Fail semantics: All tests pass with exit code 0.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Toggleable meeting notes with action items and callouts | Toggleable headers, to_do tasks, callout, quote | High |
| 2 | Synced block reference across multi-page notes | transclusion_container, transclusion_reference, atomic ops | High |
| 3 | Media-rich resource board with bookmarks, videos, files | bookmark, video, audio, file, pdf, column layout | Medium |
| 4 | Deeply nested container tree with atomic rollback on failure | op.set, op.listAfter, transaction rollback, leaf validation | High |
| 5 | Rich-text formatted documentation page with H4 and quotes | header_4, quote, rich-text styling decorators | Medium |

## Coverage Thresholds
- Tier 1: ≥5 per feature
- Tier 2: ≥5 per feature (where boundaries exist)
- Tier 3: pairwise coverage of major feature interactions
- Tier 4: ≥5 realistic application scenarios
