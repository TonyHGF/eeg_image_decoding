"""Evaluate the frozen C/L grid and select settings using validation only."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean, stdev

import numpy as np
from rank_fusion import fuse, metrics


def csv_write(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def evaluate(args):
    config = json.loads(args.config.read_text(encoding='utf-8'))
    config_hash = hashlib.sha256(args.config.read_bytes()).hexdigest()
    if (args.output / 'summary.csv').exists():
        raise FileExistsError('Use a fresh report output directory')
    args.output.mkdir(parents=True, exist_ok=True)
    caption_rows = [json.loads(x) for x in args.captions.read_text(encoding='utf-8').splitlines()]
    candidates = {r['index']: r for r in caption_rows if r['split'] == 'test'}
    if sorted(candidates) != list(range(200)):
        raise ValueError('Incomplete test candidate pairs')
    caption_hash = hashlib.sha256(args.captions.read_bytes()).hexdigest()
    methods = [(f'{family}_C{c.replace("/", "-")}_L{window}', family, c, window, weights)
               for family, weights in config['combinations'].items()
               for c in config['c_values'] for window in config['windows']]
    all_metrics, predictions, audits = [], [], []
    for subject in args.subjects:
        path = args.ranks / f'sub{subject:02d}.npz'
        audit = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
        if audit['config_sha256'] != config_hash or audit['captions_sha256'] != caption_hash:
            raise ValueError('Extraction configuration/caption provenance differs')
        if audit['ranks_sha256'] != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Rank cache hash mismatch')
        audits.append(audit)
        with np.load(path) as data:
            for split in ('val', 'test'):
                ranks, truth = data[f'{split}_ranks'], data[f'{split}_truth']
                for method, family, c, window, weights in methods:
                    order, votes = fuse(ranks, weights, c, window)
                    selected = order[:, 0]
                    all_metrics.append(dict(subject=subject, split=split, method=method, family=family,
                                            c=c, window=window, **metrics(order, truth),
                                            top1_vote_tie_fraction=float(np.mean(np.sum(
                                                np.isclose(votes, votes.max(axis=1, keepdims=True), atol=1e-12, rtol=0), axis=1) > 1))))
                    if split == 'test':
                        for query, column in enumerate(selected):
                            candidate = int(data['test_candidates'][query, column])
                            pair = candidates[candidate]
                            predictions.append(dict(subject=subject, method=method, query_id=query,
                                                    true_pair_id=query, predicted_pair_id=candidate,
                                                    predicted_image=pair['path'], predicted_text=pair['caption'],
                                                    correct=int(query == candidate), vote=float(votes[query, column]),
                                                    **{f'{b}_rank': int(ranks[i, query, column]) for i, b in enumerate(config['branches'])}))
                for i, branch in enumerate(config['branches']):
                    order = np.argsort(ranks[i], axis=-1)
                    all_metrics.append(dict(subject=subject, split=split, method=branch, family='single_branch',
                                            c='', window='', **metrics(order, truth), top1_vote_tie_fraction=0.0))
    summaries = []
    method_order = [m[0] for m in methods] + config['branches']
    for split in ('val', 'test'):
        for method in method_order:
            rows = [r for r in all_metrics if r['split'] == split and r['method'] == method]
            if len(rows) != len(args.subjects):
                raise ValueError('Incomplete method results')
            summary = dict(split=split, method=method, family=rows[0]['family'], c=rows[0]['c'], window=rows[0]['window'], n=len(rows))
            for k in range(1, 11):
                values = [100 * r[f'top{k}'] for r in rows]
                summary.update({f'top{k}_mean_pct': mean(values), f'top{k}_sd_pct': stdev(values) if len(values) > 1 else 0.0})
            summary['top1_vote_tie_fraction'] = mean(r['top1_vote_tie_fraction'] for r in rows)
            summaries.append(summary)
    selected = {}
    for family in config['combinations']:
        validation = [r for r in summaries if r['split'] == 'val' and r['family'] == family]
        chosen = max(validation, key=lambda r: (r['top1_mean_pct'], r['top5_mean_pct']))
        test = next(r for r in summaries if r['split'] == 'test' and r['method'] == chosen['method'])
        selected[family] = dict(method=chosen['method'], validation=chosen, test=test)
    global_choice = max(selected, key=lambda f: (selected[f]['validation']['top1_mean_pct'], selected[f]['validation']['top5_mean_pct']))
    paired = []
    for choice in selected.values():
        for baseline in config['branches']:
            for k in (1, 5, 10):
                deltas = []
                for subject in args.subjects:
                    lookup = {r['method']: r[f'top{k}'] for r in all_metrics if r['subject'] == subject and r['split'] == 'test'}
                    deltas.append(100 * (lookup[choice['method']] - lookup[baseline]))
                paired.append(dict(method=choice['method'], baseline=baseline, metric=f'top{k}',
                                   mean_pp=mean(deltas), sd_pp=stdev(deltas) if len(deltas) > 1 else 0.0,
                                   **{f'sub{s:02d}_pp': d for s, d in zip(args.subjects, deltas)}))
    csv_write(args.output / 'per_subject.csv', all_metrics)
    csv_write(args.output / 'summary.csv', summaries)
    csv_write(args.output / 'paired_predictions.csv', predictions)
    csv_write(args.output / 'selected_differences.csv', paired)
    result = dict(config=config, config_sha256=config_hash, subjects=args.subjects,
                  validation_selected=selected, global_selected_family=global_choice,
                  extraction_audits=audits)
    (args.output / 'selection.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    lines = ['# Paired image/text rank fusion', '',
             'Exploratory follow-up using one validation-best checkpoint per backend. No retraining.',
             'All branches vote on the same image/caption ID. C/L are selected by validation only.',
             'Validation: 740 queries, each with its positive plus 199 fixed distractors from validation.',
             'Test: 200 queries against all 200 test pairs. Values: subject mean ± sample SD (%).',
             'These are single-checkpoint baselines, distinct from the prior three-checkpoint metric averages.', '',
             '| Split | Method | Top-1 | Top-5 | Top-10 |', '|---|---|---:|---:|---:|']
    for r in summaries:
        lines.append(f'| {r["split"]} | {r["method"]} | ' + ' | '.join(
            f'{r[f"top{k}_mean_pct"]:.3f} ± {r[f"top{k}_sd_pct"]:.3f}' for k in (1, 5, 10)) + ' |')
    lines += ['', 'Validation-selected methods:', '']
    lines += [f'- {f}: {v["method"]}' for f, v in selected.items()]
    lines += [f'- Global validation selection: {selected[global_choice]["method"]}', '',
              'Ties: vote rounded to 12 decimals, then lower weighted mean full rank, then candidate ID.',
              'All per-query selected image/caption pairs and contributing branch ranks are in paired_predictions.csv.', '']
    (args.output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({f: v['method'] for f, v in selected.items()}, indent=2))
    print(f'COMPLETE {len(args.subjects)} subjects, {len(methods)} fusion settings')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('config', 'ranks', 'captions', 'output'):
        parser.add_argument(f'--{name}', type=Path, required=True)
    parser.add_argument('--subjects', type=int, nargs='+', default=list(range(1, 11)))
    evaluate(parser.parse_args())
