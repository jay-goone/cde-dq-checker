# Stage 2b: rules

`rules.csv` holds 57 rules: 42 fail, 6 warn, 3 flag and 6 decision rules. Every EIR clause has at least one rule, and every data dictionary row is used by at least one rule.

## Layers

| Layer | What it checks | Rules |
|---|---|---|
| 1 | Metadata vs data dictionary: required fields, formats, allowed values, naming, classification, status and revision | 25 |
| 2 | Status vs programme: delivered by the due date, right status by the due date, revisions moving forward | 5 |
| 3 | Content and consistency: IFC ↔ COBie match, spaces and floors, systems, TMV coverage, call points, emergency lighting | 18 |
| 4 | Free-text flagging: maintenance task descriptions. **Flags only. A person decides.** | 3 |
| D | Submission decision: turns results into accept / reject per EIR Section 9 | 6 |

## Columns

| Column | Meaning |
|---|---|
| `check_logic` | What the rule does, in plain English. This is the spec for the code |
| `check_type` | The Stage 4 function that runs it. Many rules share one function (e.g. `pattern`, `lookup`, `equals_reference`) |
| `dd_ref` | Data dictionary rows the rule reads. `ALL_REQUIRED_Y`, `ALL_WITH_PATTERN` and similar mean "every dictionary row that has that property" |
| `scope` | Asset codes, `ALL`, `per dd row` (scope comes from each row's `applies_to`), `midp`, `container` or `submission` |
| `target` | IFC, COBie, REG (document register), or a combination |
| `severity` | `fail`, `warn`, `flag` (layer 4 only) or `decision` |
| `acceptance` | The EIR Section 9 outcome a fail feeds into. `ACC-03 / ACC-05` means ACC-03 if the asset is safety-critical, otherwise ACC-05 |
| `message` | Template for the results table |

## How a new requirement gets added

1. Add the attribute to `data_dictionary.csv`.
2. If it fits an existing generic rule (required, pattern, allowed values, minimum), you're done: rules L1-04 to L1-09 pick it up automatically.
3. If it needs new logic, add a rule row with a new `check_type`. That one function gets written in Stage 4.

Step 2 is the reusable part of the service: most client-specific requirements are configuration, not code.
