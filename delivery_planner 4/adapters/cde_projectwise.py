"""ProjectWise adapter: reads a saved-search export (one row per version) into the standard
'cde_versions' table. Another CDE (ACC, Asite) gets its own adapter returning the same columns.

Standard columns:
  container_name, file_name, title_cde, title_attr, version, workflow_state, status_date, updated_by,
  folder, doc_guid, project, originator, volume, level, type, role, number, revision, suitability, exported
"""
import pandas as pd

RENAME = {
    "Name": "container_name", "File Name": "file_name", "Description": "title_cde", "ATTR_Title": "title_attr",
    "Version": "version", "State": "workflow_state", "State Changed": "status_date", "Updated By": "updated_by",
    "Folder": "folder", "Document GUID": "doc_guid", "ATTR_Project": "project", "ATTR_Originator": "originator",
    "ATTR_Volume": "volume", "ATTR_Level": "level", "ATTR_Type": "type", "ATTR_Role": "role",
    "ATTR_Number": "number", "ATTR_Revision": "revision", "ATTR_Suitability": "suitability", "Exported": "exported",
}


def from_csv(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = [c for c in RENAME if c not in df.columns]
    if missing:
        raise ValueError(f"CDE export is missing columns: {missing}")
    df = df.rename(columns=RENAME)[list(RENAME.values())]
    for c in ("status_date", "exported"):
        df[c] = pd.to_datetime(df[c], format="%d/%m/%Y %H:%M", errors="coerce")   # bad or blank dates become NaT; C05 reports them
    df["version"] = pd.to_numeric(df["version"])
    return df.sort_values(["container_name", "version"]).reset_index(drop=True)
