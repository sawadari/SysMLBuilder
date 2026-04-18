#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / 'profiles'
TEST_GFSE = ROOT / 'example'
REPORTS = ROOT / 'reports'
DOCS = ROOT / 'docs'

def load_yaml(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

results = {
    'root': str(ROOT),
    'yaml_parse': [],
    'docs_present': [],
    'case_files_exist': [],
    'contract_required_fields': [],
    'canonical_checks': [],
    'overlay_checks': [],
    'rubric_checks': [],
    'strict_suite_checks': []
}
all_ok = True

required_yaml = [
    PROFILES / 'automotive_control_profile_v3.yaml',
    PROFILES / 'benchmark_lints.yaml',
    PROFILES / 'domain_vocabulary_automotive_control.yaml',
    PROFILES / 'example_retrieval.yaml',
    PROFILES / 'gfse_reference_benchmark_profile.yaml',
    PROFILES / 'model_lints.yaml',
    PROFILES / 'projection_profiles.yaml',
    PROFILES / 'reference_model_trace.yaml',
    PROFILES / 'requirement_contract.yaml',
    PROFILES / 'requirement_patterns.yaml',
    PROFILES / 'review_overlay.yaml',
    PROFILES / 'satisfiability_model.yaml',
    TEST_GFSE / 'case_manifest.yaml',
    TEST_GFSE / 'scoring_rubric.yaml',
]
for path in required_yaml:
    try:
        data = load_yaml(path)
        results['yaml_parse'].append({'file': str(path.relative_to(ROOT)), 'status': 'ok', 'type': type(data).__name__})
    except Exception as e:
        results['yaml_parse'].append({'file': str(path.relative_to(ROOT)), 'status': 'error', 'error': str(e)})
        all_ok = False

required_docs = [
    ROOT / 'README.md',
    DOCS / 'developer_design_rationale.md',
    DOCS / 'gfse_testdata_design_feedback.md',
    DOCS / 'benchmark_scoring_guide.md',
    DOCS / 'customization_map.md',
]
for path in required_docs:
    exists = path.exists()
    results['docs_present'].append({'file': str(path.relative_to(ROOT)), 'status': 'ok' if exists else 'error'})
    if not exists:
        all_ok = False

manifest = load_yaml(TEST_GFSE / 'case_manifest.yaml')
rubric = load_yaml(TEST_GFSE / 'scoring_rubric.yaml')
strict_cases = {c['case_id']: c for c in manifest['cases']}
rubric_profiles = rubric['case_profiles']

for case_id, case in strict_cases.items():
    base = TEST_GFSE / case_id
    req_path = TEST_GFSE / case_id / 'input' / 'requirements_en.md'
    contracts_path = TEST_GFSE / case_id / 'output' / 'expected_en_contracts.yaml'
    canonical_path = TEST_GFSE / case_id / 'output' / 'expected_en_canonical.sysml'
    overlay_path = TEST_GFSE / case_id / 'output' / 'expected_en_review_overlay.sysml'
    manifest_path = TEST_GFSE / case_id / 'output' / 'expected_en_projection_manifest.yaml'

    expected = {
        'requirements': req_path.exists(),
        'contracts': contracts_path.exists(),
        'canonical': canonical_path.exists(),
        'overlay': overlay_path.exists(),
        'projection_manifest': manifest_path.exists(),
    }

    target = case['target_satisfiability']
    missing = []
    if not expected['requirements']:
        missing.append(req_path.name)
    if not expected['contracts']:
        missing.append(contracts_path.name)
    if target == 'high':
        if not expected['canonical']:
            missing.append(canonical_path.name)
        if not expected['projection_manifest']:
            missing.append(manifest_path.name)
    elif target == 'medium':
        if not expected['canonical']:
            missing.append(canonical_path.name)
        if not expected['overlay']:
            missing.append(overlay_path.name)
    elif target == 'low':
        if not expected['overlay']:
            missing.append(overlay_path.name)

    status = 'ok' if not missing else 'error'
    results['case_files_exist'].append({'case_id': case_id, 'status': status, 'missing_files': missing})
    if missing:
        all_ok = False

    if case['source_model_trace']['trace_quality'] != 'direct_file_grounded':
        results['strict_suite_checks'].append({'case_id': case_id, 'rule': 'trace_quality_must_be_direct_file_grounded', 'status': 'error'})
        all_ok = False
    else:
        results['strict_suite_checks'].append({'case_id': case_id, 'rule': 'trace_quality_must_be_direct_file_grounded', 'status': 'ok'})

    if case['scoring_profile'] not in rubric_profiles:
        results['rubric_checks'].append({'case_id': case_id, 'status': 'error', 'reason': 'missing_scoring_profile'})
        all_ok = False
    else:
        dims = rubric_profiles[case['scoring_profile']]['dimensions']
        total = sum(dims.values())
        status = 'ok' if total == 100 else 'error'
        results['rubric_checks'].append({'case_id': case_id, 'status': status, 'total': total})
        if total != 100:
            all_ok = False

    if contracts_path.exists():
        data = load_yaml(contracts_path)
        for contract in data.get('contracts', []):
            required_fields = ['contract_id', 'source_requirement_id', 'source_anchor', 'trace_quality', 'classification', 'subject', 'evidence']
            missing_fields = [f for f in required_fields if f not in contract]
            status = 'ok' if not missing_fields else 'error'
            results['contract_required_fields'].append({
                'case_id': case_id,
                'contract_id': contract.get('contract_id'),
                'status': status,
                'missing_fields': missing_fields
            })
            if missing_fields:
                all_ok = False

    if canonical_path.exists():
        text = canonical_path.read_text(encoding='utf-8')
        contains_draft = any(tok in text for tok in ['DraftRequirementContracts', 'MissingSlots', 'OpenQuestions', 'Assumptions', 'BehaviorCandidates'])
        results['canonical_checks'].append({'case_id': case_id, 'rule': 'must_not_contain_draft_packages', 'status': 'ok' if not contains_draft else 'error'})
        if contains_draft:
            all_ok = False

        # requirement def blocks must have subject
        req_blocks = re.findall(r'requirement def\s+[^{}]+\{(.*?)\n\}', text, re.S)
        req_missing_subject = [i for i, body in enumerate(req_blocks, start=1) if 'subject ' not in body]
        results['canonical_checks'].append({'case_id': case_id, 'rule': 'requirement_defs_must_have_subject', 'status': 'ok' if not req_missing_subject else 'error', 'failures': req_missing_subject})
        if req_missing_subject:
            all_ok = False

        untyped_ports = re.findall(r'^\s*port\s+[A-Za-z_][A-Za-z0-9_]*\s*;\s*$', text, re.M)
        results['canonical_checks'].append({'case_id': case_id, 'rule': 'all_ports_must_be_typed', 'status': 'ok' if not untyped_ports else 'error', 'failures': untyped_ports})
        if untyped_ports:
            all_ok = False

        has_arrow = '->' in text
        results['canonical_checks'].append({'case_id': case_id, 'rule': 'must_not_use_arrow_placeholders', 'status': 'ok' if not has_arrow else 'error'})
        if has_arrow:
            all_ok = False

        if 'use case def' in text:
            usecase_blocks = re.findall(r'use case def\s+[^{}]+\{(.*?)\n\}', text, re.S)
            usecase_bad = [i for i, body in enumerate(usecase_blocks, start=1) if ('subject ' not in body or 'objective' not in body)]
            results['canonical_checks'].append({'case_id': case_id, 'rule': 'use_case_defs_must_have_subject_and_objective', 'status': 'ok' if not usecase_bad else 'error', 'failures': usecase_bad})
            if usecase_bad:
                all_ok = False

    if overlay_path.exists():
        text = overlay_path.read_text(encoding='utf-8')
        required_overlay = ['package DraftRequirementContracts', 'package ReviewGuide']
        missing_pkgs = [pkg for pkg in required_overlay if pkg not in text]
        has_review_action = '[review-action]' in text
        results['overlay_checks'].append({'case_id': case_id, 'rule': 'overlay_packages_exist', 'status': 'ok' if not missing_pkgs else 'error', 'missing': missing_pkgs})
        results['overlay_checks'].append({'case_id': case_id, 'rule': 'review_action_token_exists', 'status': 'ok' if has_review_action else 'error'})
        if missing_pkgs or not has_review_action:
            all_ok = False

results['summary'] = {'overall_status': 'ok' if all_ok else 'error'}

report_path = REPORTS / 'validation_report.yaml'
report_path.write_text(yaml.safe_dump(results, sort_keys=False, allow_unicode=True), encoding='utf-8')
print(report_path)
print(results['summary']['overall_status'])
