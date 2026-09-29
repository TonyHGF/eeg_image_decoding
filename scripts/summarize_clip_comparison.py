"""Summarize complete ten-subject runs without ML dependencies or test-driven tuning."""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev


GROUPS = {
    'retrieval_topk': range(1, 11), 'text_topk': range(1, 11),
    'retrieval_way': (2, 4, 10, 20, 50, 100),
    'text_way': (2, 4, 10, 20, 50, 100),
}
CONTROLS = ('epoch', 'batch_size', 'encoder_type', 'seed', 'alpha',
            'no_pretrain', 'load_pretrain_groups', 'init_groups', 'early_stopping',
            'insubject', 'eeg_data_path', 'pretrain_dir')


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(root, output, conditions):
    runs, reference, identities = {}, None, {}
    for condition in conditions:
        subjects = {}
        for path in sorted((root / condition).glob('metrics_sub*.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            subject = data['subject']
            if subject in subjects:
                raise ValueError(f'Duplicate subject: {condition}/{subject}')
            controls = {k: data['config'][k] for k in CONTROLS}
            reference = reference or controls
            if controls != reference:
                raise ValueError(f'Configuration mismatch: {condition}/{subject}')
            if not data['loaded_parameter_keys'] or not data['pretrain_checkpoint']:
                raise ValueError(f'Missing pretraining evidence: {condition}/{subject}')
            identity = (data['split_sha256'], data['pretrain_checkpoint'],
                        tuple(sorted(data['loaded_parameter_keys'])))
            if identity != identities.setdefault(subject, identity):
                raise ValueError(f'Split/pretraining mismatch: {condition}/{subject}')
            history_path = path.with_name(f'history_sub{subject:02d}.json')
            history = json.loads(history_path.read_text(encoding='utf-8'))
            if len(history) != data['epochs_completed'] or len(history) > controls['epoch']:
                raise ValueError(f'Incomplete training history: {path}')
            if not set(data['selected_epochs']) <= {h['epoch'] for h in history}:
                raise ValueError(f'Invalid selected epochs: {path}')
            for group, ks in GROUPS.items():
                if set(data[group]) != {str(k) for k in ks}:
                    raise ValueError(f'Missing metrics: {path}/{group}')
                values = [data[group][str(k)] for k in ks]
                if not all(math.isfinite(v) and 0 <= v <= 1 for v in values):
                    raise ValueError(f'Invalid metrics: {path}/{group}')
                if group.endswith('topk') and values != sorted(values):
                    raise ValueError(f'Nonmonotonic Top-k: {path}/{group}')
            subjects[subject] = data
        if set(subjects) != set(range(1, 11)):
            raise ValueError(f'{condition} requires all ten subjects; found {sorted(subjects)}')
        runs[condition] = subjects

    rows, summaries, differences = [], [], []
    for condition, subjects in runs.items():
        for subject, data in sorted(subjects.items()):
            row = dict(condition=condition, subject=subject,
                       split_sha256=data['split_sha256'],
                       best_val_loss=data['best_val_loss'],
                       selected_epochs=';'.join(map(str, data['selected_epochs'])),
                       epochs_completed=data['epochs_completed'], seconds=data['seconds'],
                       peak_gpu_gib=data['peak_gpu_memory_bytes'] / 2**30)
            for group, ks in GROUPS.items():
                row.update({f'{group}_{k}_pct': 100 * data[group][str(k)] for k in ks})
            rows.append(row)
        for group, ks in GROUPS.items():
            for k in ks:
                values = [100 * d[group][str(k)] for d in subjects.values()]
                summaries.append(dict(condition=condition, metric=f'{group}_{k}', n=10,
                                      mean_pct=mean(values), sd_pct=stdev(values)))

    for left, right in [('cn-shared', 'openai-shared'), ('cn-cached', 'cn-shared'),
                        ('cn-cached', 'openai-shared')]:
        if left not in runs or right not in runs:
            continue
        for group, ks in GROUPS.items():
            for k in ks:
                values = [100 * (runs[right][s][group][str(k)] - runs[left][s][group][str(k)])
                          for s in range(1, 11)]
                differences.append(dict(comparison=f'{right} minus {left}',
                                        metric=f'{group}_{k}', n=10,
                                        mean_difference_pp=mean(values),
                                        sd_difference_pp=stdev(values),
                                        **{f'sub{s:02d}_pp': v for s, v in enumerate(values, 1)}))

    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'per_subject.csv', rows)
    write_csv(output / 'summary.csv', summaries)
    if differences:
        write_csv(output / 'paired_differences.csv', differences)
    lines = ['# CLIP comparison: completed conditions', '',
             'This report includes only the complete conditions listed below. Scheduler success',
             'and feature/caption provenance must also be verified in the run record.', '',
             'Values are mean ± sample SD across ten subjects, in percent. One seed only.',
             'Each subject value averages metrics from three validation-selected checkpoints;',
             'this is not prediction ensembling. Text metrics are caption retrieval.', '',
             'CN-cached uses original repository features with shared runtime/evaluation fixes.',
             'CN-shared versus OpenAI-shared isolates the encoder with identical new captions.',
             'Comparisons involving CN-cached also include caption differences.', '',
             '## All accuracy metrics', '', '| Condition | Metric | Mean ± SD (%) |',
             '|---|---|---:|']
    lines += [f"| {r['condition']} | {r['metric']} | {r['mean_pct']:.3f} ± {r['sd_pct']:.3f} |"
              for r in summaries]
    lines += ['', '## Training and selected checkpoints', '',
              '| Condition | Subject | Epochs | Selected epochs (zero based) | Best val loss | Seconds | Peak allocated GPU GiB |',
              '|---|---:|---:|---|---:|---:|---:|']
    lines += [f"| {r['condition']} | {r['subject']} | {r['epochs_completed']} | {r['selected_epochs']} | "
              f"{r['best_val_loss']:.6f} | {r['seconds']:.2f} | {r['peak_gpu_gib']:.3f} |" for r in rows]
    if differences:
        lines += ['', '## Paired differences', '',
                  'Positive values favor the first named condition. Units: percentage points.', '',
                  '| Comparison | Metric | Mean ± SD (pp) |', '|---|---|---:|']
        lines += [f"| {r['comparison']} | {r['metric']} | {r['mean_difference_pp']:.3f} ± {r['sd_difference_pp']:.3f} |"
                  for r in differences]
    lines += ['', '## Shared configuration', '', '```json', json.dumps(reference, indent=2), '```', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Validated {len(rows)} subject runs; report: {output / "report.md"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--conditions', nargs='+', default=['cn-cached', 'cn-shared', 'openai-shared'])
    args = parser.parse_args()
    summarize(args.root, args.output, args.conditions)
