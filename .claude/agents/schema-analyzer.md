# Schema Analyzer

Analyze the JSON schema files in `schema/` and cross-reference them against implemented API endpoints to identify gaps and inconsistencies.

## Purpose

The `schema/` directory contains large JSON schema files (`infra.json`, `manage.json`) that define the expected API structure. This agent compares those schemas against the actual endpoint implementations in `app/v1/` and `app/v2/` to find:

1. **Missing endpoints**: Paths defined in schemas but not implemented
2. **Extra endpoints**: Implemented endpoints not present in schemas
3. **Model mismatches**: Response/request models that differ from schema definitions
4. **Missing fields**: Fields defined in schemas but absent from SQLModel/Pydantic models

## Workflow

1. Parse `schema/infra.json` and `schema/manage.json` to extract defined paths and models
2. Scan `app/v1/endpoints/` and `app/v2/endpoints/` to catalog all implemented routes
3. Scan `app/v1/models/` and `app/v2/models/` to catalog all defined models and their fields
4. Cross-reference and produce a gap analysis report

## Output

Produce a markdown summary with:
- Table of schema paths vs implementation status
- List of model field discrepancies
- Prioritized recommendations for what to implement next
