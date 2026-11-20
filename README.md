# Ascendancy Systems on GitHub

This repository maintains the [organization profile](https://github.com/Ascendancy-Systems) and the MG-001 operational record. Visitors can begin at the [Front Desk](https://ascendancy-systems.github.io/front-desk/).

| Resource | Where to find it |
| --- | --- |
| Front Desk · public reception, directory, and map | [Visit the Front Desk](https://ascendancy-systems.github.io/front-desk/) · [Directory source and maintenance](https://github.com/Ascendancy-Systems/front-desk) |
| Public organization profile | [GitHub overview](https://github.com/Ascendancy-Systems) · [Profile source](./profile/README.md) |
| MG-001 registered instrument and EF-001 assessment | [Instrument record](./profile/META-GAUGE.md) · [Signal record](./profile/signals/meta-gauge-mg-001.json) |
| GMG-A experimental spatial instrument | [Source, specifications, and tests](https://github.com/Ascendancy-Systems/meta-gauge) · [Interactive demo](https://ascendancy-systems.github.io/meta-gauge/) |

Artwork and instrument files are indexed in the [banner collection](./assets/banners/Banners.md) and [gauge collection](./assets/gauges/Gauges.md).

## Maintaining the profile

Edit [`profile/README.md`](./profile/README.md) through a pull request. GitHub renders that file on the public organization Overview after merge. Keep the assessed sentence in **I. Orientation** synchronized with the quotation in the [EF-001 assessment](./profile/META-GAUGE.md#ef-001--institutional-research-orientation). A change to that claim triggers review of its assessment. Edit visitor listings in the [Front Desk directory](https://github.com/Ascendancy-Systems/front-desk/blob/main/data/directory.json).

## Maintaining the EF-001 display

The [legacy renderer](./scripts/render_meta_gauge.py) updates the EF-001 display labels from the authorized signal. It remains available for reviewed updates to the assessment. Keep the source SVG and prior PNG for reference. The GMG-A preview is rendered in the [Meta-Gauge repository](https://github.com/Ascendancy-Systems/meta-gauge).

The [render workflow](./.github/workflows/meta-gauge.yml) renders on a review branch after a signal change or a manual run on that branch. Review the assessment, signal, and regenerated assets together. Pull requests also run the renderer tests and check the assessed sentence against the public profile. The renderer uses the pinned CairoSVG dependency to produce the PNG from the SVG. To run those checks locally, use the following commands.

```text
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s scripts/tests -v
```
