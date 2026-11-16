# Stage 2a: data dictionary

The EIR (`01_EIR_Larch_Road_Health_Centre.md`) turned into machine-readable files. Every row points back to an EIR clause ID.

| File | What it holds |
|---|---|
| `data_dictionary.csv` | One row per attribute: where it lives in COBie and IFC, whether it's required, and what a valid value looks like |
| `reference/asset_types.csv` | Asset types: IFC entity, Uniclass Pr and Ss codes, safety-critical flag, maximum maintenance interval, expected quantity |
| `reference/space_schedule.csv` | The 19 spaces with room name, SL code and patient-area flag |
| `reference/code_lists.csv` | Allowed values: naming fields, floors, status codes (with order), revision prefixes, frequency units (with month factors), placeholders, withdrawn Uniclass codes |
| `reference/midp.csv` | MIDP: container, exchange, due date, status required by that date |

## Columns in `data_dictionary.csv`

| Column | Meaning |
|---|---|
| `entity` | COBie level: Floor, Space, Component, Type, Job, Contact, System, Document, or Container (document register) |
| `applies_to` | Asset codes separated by `\|`, or `ALL` |
| `table` / `field` | COBie sheet and column, or `Register` and its column. `Attribute (Type)` means a row in the COBie Attribute sheet with SheetName = Type |
| `ifc_source` | Where the same value sits in IFC4 |
| `required` | `Y` = always, `C` = only when `condition` is true |
| `data_type` | text, code, date, decimal, integer, boolean (Y/N), email, guid |
| `allowed_values` | Fixed list separated by `\|` |
| `pattern` | Regular expression the value must match |
| `lookup` | Value must exist in another table: `Table.Column`, `reference_file.column`, or `code_lists:list_name` |
| `min_value` / `max_value` | A number, or the name of another field (e.g. warranty start ≥ `InstallationDate`) |
| `purpose` | O = operation and maintenance, C = compliance, S = space management |

## Extending it (second pass)

- **New asset type:** add a row to `asset_types.csv`, then add its code to `applies_to` on the rows that apply. Also add it to the name patterns (DD-020, DD-021, DD-040).
- **More floors or a second building:** add codes to `code_lists.csv` (`floor`, `level`, `volume`), add spaces to `space_schedule.csv`, and widen the `00` in the name patterns.
- **New party:** add an `originator` row to `code_lists.csv` and to the container name pattern.
- **New milestone:** add rows to `midp.csv`.

Rules (`rules.csv`) come next and use these files. They don't repeat values.
