# Ascendancy Systems on GitHub

This repository maintains the public organization profile and the MG-001 instrument record.

| Resource | Where to find it |
| --- | --- |
| Public organization profile | [GitHub overview](https://github.com/Ascendancy-Systems) · [Profile source](./profile/README.md) |
| MG-001 registered instrument and EF-001 assessment | [Instrument record](./profile/META-GAUGE.md) · [Signal record](./profile/signals/meta-gauge-mg-001.json) |
| GMG-A experimental spatial instrument | [Source, specifications, and tests](https://github.com/Ascendancy-Systems/meta-gauge) · [Interactive demo](https://ascendancy-systems.github.io/meta-gauge/) |

## Maintaining the profile

Edit [`profile/README.md`](./profile/README.md) through a pull request. GitHub renders that file on the public organization Overview after merge. Keep public links pointed at live destinations. When the standalone homepage is ready, add its URL to the Website section and verify the Meta-Gauge demo link.

## Maintaining the EF-001 display

The [legacy renderer](./scripts/render_meta_gauge.py) updates the EF-001 display labels from the authorized signal. It remains available for reviewed updates to the assessment. Keep the source SVG and prior PNG for reference. The GMG-A preview is rendered in the [Meta-Gauge repository](https://github.com/Ascendancy-Systems/meta-gauge).

The [render workflow](./.github/workflows/meta-gauge.yml) renders on a review branch after a signal change or a manual run on that branch. Review the assessment, signal, and regenerated assets together. To run the existing checks locally:

```text
python -m pip install -r requirements-meta-gauge.txt
python -m unittest discover -s tests -v
```
