"""Re-evaluate all experiments with VSI-Bench paper metrics."""
import json, os

src = r'C:\Users\贝贝\Documents\Three-view Cognitive Map\src'

def mra(pred, gt):
    try:
        pf = float(pred)
        gf = float(gt)
    except:
        return 0.0
    if gf == 0:
        return 0.0
    rel_err = abs(pf - gf) / gf
    thetas = [t / 100.0 for t in range(50, 100, 5)]
    ok = sum(1 for th in thetas if rel_err < 1 - th)
    return ok / len(thetas)

def load(path):
    d = json.load(open(path, encoding='utf-8'))
    if isinstance(d, dict) and 'results' in d:
        return d['results']
    return [r for r in d if '__summary__' not in r]

exps = {
    '3-pass shared': 'results_gemini35_fullvideo.json',
    'direct (无建图)': 'results_gemini35_direct_video.json',
    '3-pass noshared': 'results_gemini35_noshared.json',
    '3-pass shared+viz': 'results_gemini35_shared_viz.json',
    '3-pass noshared_video': 'results_gemini35_noshared_video.json',
}

mca = ['object_rel_distance', 'object_rel_direction_easy',
       'object_rel_direction_medium', 'object_rel_direction_hard']
na = ['object_abs_distance']

print('%-30s %7s %5s %10s %6s %6s %6s %6s' % (
    '实验', '总Score', 'MCA', 'abs(MRA)', 'rel_d', 'dir_e', 'dir_m', 'dir_h'))
print('-' * 80)

for label, fname in exps.items():
    results = load(os.path.join(src, fname))
    mc_c, mc_t, na_s, na_c = 0, 0, 0.0, 0
    pt = {}
    for r in results:
        if r.get('error'):
            continue
        qt = r.get('question_type', '')
        gt = r['ground_truth']
        if qt not in pt:
            pt[qt] = {'score': 0, 'n': 0}
        pt[qt]['n'] += 1
        if qt in na:
            pred = r.get('extracted_answer')
            s = mra(pred, gt)
            na_s += s
            na_c += 1
        elif qt in mca:
            pred = r.get('extracted_answer')
            ok = bool(pred and gt and pred.strip().upper() == gt.strip().upper())
            if ok:
                mc_c += 1
                pt[qt]['score'] += 1
            mc_t += 1
        else:
            pt[qt]['n'] -= 1

    total = na_c + mc_t
    tot_s = na_s + mc_c
    overall = tot_s / total * 100 if total > 0 else 0
    mca_acc = mc_c / mc_t * 100 if mc_t > 0 else 0
    na_mra = na_s / na_c * 100 if na_c > 0 else 0

    def g(k):
        v = pt.get(k, {})
        n = v.get('n', 0)
        if n == 0:
            return '-'
        s = v.get('score', 0)
        if isinstance(s, float):
            return '%.0f%%' % (s / n * 100)
        return '%d%%' % (s / n * 100)

    print('%-30s %5.1f%% %4.0f%% %8.1f%% %5s %5s %5s %5s' % (
        label, overall, mca_acc, na_mra,
        g('object_rel_distance'), g('object_rel_direction_easy'),
        g('object_rel_direction_medium'), g('object_rel_direction_hard')))

print()
print('=== abs_distance MRA detail ===')
for label, fname in exps.items():
    results = load(os.path.join(src, fname))
    print('\n' + label + ':')
    for r in results:
        if r.get('question_type') == 'object_abs_distance' and not r.get('error'):
            gt = r['ground_truth']
            ps = r.get('extracted_answer')
            if ps:
                s = mra(ps, gt)
                re = abs(float(ps) - float(gt)) / float(gt) * 100
                print('  %-15s GT=%4.1f  pred=%5.2f  rel_err=%5.1f%%  MRA=%d%%' % (
                    r['scene'], float(gt), float(ps), re, s * 100))
            else:
                print('  %-15s GT=%4.1f  pred=N/A  MRA=0%%' % (r['scene'], float(gt)))
