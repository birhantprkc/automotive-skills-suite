# cdd-builder — Example

**What this skill produces:** A CANdela Diagnostic Description (CDD) authoring workbook for Vector CANdela Studio — 12 tabs, verified against the generator on 2026-08-11: `Title`, `Document Control`, `ECU Identity`, `Session Catalog`, `Service Inventory`, `DID Catalog`, `RID Catalog`, `DTC Cross-Reference`, `Security Access Levels`, `Variant Coding`, `Communication Configuration`, `References`. It captures an ECU's full diagnostic specification — supported UDS services, data identifiers, routine identifiers, sessions, security access levels and variant coding — in a form suitable for authoring a Vector diagnostic database.

**Typical input shape:** A single JSON file — `examples/sample_input.json` ships inside the skill archive as a worked BCM example. Keys: `ecu` (name, abbr, project, doc_id, revision, date, author, approver, supplier, hw_version, sw_version, market); `sessions[]` (id, name, default_session, description, transitions); `services[]` (service_id, name, enabled, description, data_length); `diids[]` (id, name, read_access, write_access, periodic_data_identifier, description); `riids[]` (id, name, routine_control_type, description, options); `security_levels[]` (level, request_seed_service, send_key_service, description); `variant_coding[]` (variant_id, variant_name, parent_variant, differences); and `dtc_catalog_ref`, a path to the upstream `dtc-catalog-builder` workbook.

**Expected output:** `<ecu>-cdd.xlsx`. The DTC tab is a **cross-reference only** — DTC content itself lives in the `dtc-catalog-builder` output named by `dtc_catalog_ref`, and the two should be generated as a pair.

**Sample I/O:**

```bash
python scripts/generate_cdd.py examples/sample_input.json BCM-cdd.xlsx
python scripts/recalc.py BCM-cdd.xlsx
```

returns `{"status": "success", "services": 3, "diids": 2, "riids": 1, "variants": 1}` — a Body Control Module exposing UDS `0x22` / `0x2E` / `0x31`, DIDs `0xF190` (VIN) and `0xF187` (spare part number), routine `0x0203` (EraseMemory), and security level `0x01` on the standard `27 01` / `27 02` seed-key pair.

**Paired reviewer:** `cdd-checklist-reviewer` — note it resolves tabs by **exact name** (`wb["DID Catalog"]`), not by keyword. Renaming any tab in this builder breaks the reviewer silently and must be done in the same commit.

**Schema note:** the input keys are `diids` / `riids` (double-i), not `dids` / `rids`. The prose and tab names use the conventional single-i spelling. See the polish log — the keys were left alone deliberately, since renaming them breaks every existing input file.
