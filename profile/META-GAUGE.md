# Meta-Gauge MG-001

**Ascendancy Systems · Infotech**  
*Public Orientation Instrument — Operational Record v0.2*

---

[View the source-driven MG-001 display](./assets/meta-gauge-current.png) · [Explore the GMG-A spatial simulation](https://ascendancy-systems.github.io/meta-gauge/)

---

## Instrument State

| Property | Reading |
|---|---|
| Operational record version | 0.2 |
| Mode | Source-driven status display |
| Signal connection | EF-001 connected |
| Last assessment | 2026-11-20 (provisional) |
| Authority | Display only |
| Spatial implementation | GMG-A experimental demonstrator · Working Draft v0.2 |

---

## I. Purpose

MG-001 is an instrument for presenting defined aspects of the research program's orientation, evidentiary standing, continuity, and operational readiness.

It is a display of documented states, not an independent source of authority or an autonomous system of measurement.

**Identity relationship:** MG-001 is the registered public instrument—its identity, mission, evidence rules, and public record. The **Gyroscopic Meta-Gauge Assembly (GMG-A)** is an experimental spatial and perceptual implementation of MG-001. GMG-A does not create a second evidentiary authority, and its simulated ring poses do not reinterpret EF-001.

[Open the interactive GMG-A demonstrator](https://ascendancy-systems.github.io/meta-gauge/)

[Read the working specifications](https://github.com/Ascendancy-Systems/meta-gauge/tree/main/specifications) · [Return to the Front Desk](https://ascendancy-systems.github.io/front-desk/)

## II. Assessment Summary

| Register | Current reading | Basis |
|---|---|---|
| Constitutional North | Unassessed | Bearing reference not established |
| Epistemic Fix | **Provisionally Supported** | EF-001 · Manual source comparison |
| Continuity & Drift | Unassessed | No longitudinal comparison recorded |
| Dependency Readiness | Unassessed | Blocker inventory not validated |

Each register remains unassessed or unverified until its signal definition and supporting evidence are available. EF-001 applies only to the selected public statement; it does not establish the evidentiary standing of the full research program.

## III. Operating Procedure

1. **Select** one register and a bounded assessment scope.
2. **Identify** the authoritative source materials.
3. **Define** the evaluation method and permitted states.
4. **Examine** the evidence and record the result.
5. **Validate** the reading, timestamp, and provenance.
6. **Update** the authorized signal record.
7. **Generate** the SVG master and its PNG display.
8. **Publish** the updated representation with an identifiable revision.

## IV. Signal Integrity

Every operational reading must disclose its meaning, evidence source, review date, and limitations.

Unknown, stale, and unavailable states must remain visible.

No numerical score is permitted without an explicit measurement method and defined denominator.

Visual ornament, calibration marks, and symbolic geometry must not be mistaken for empirical telemetry.

An unrecognized or incomplete signal is invalid and must not produce a confident reading. The explicit `unknown` state remains available when the evidence does not support another state.

---

## Register 01 · Constitutional North

**State:** Unassessed

**Purpose:** Establish the declared reference against which the public research program is oriented.

**Evidence:** Not yet registered.

---

## Register 02 · Epistemic Fix

**State:** Provisionally Supported

**Purpose:** Determine whether published claims are supported by identifiable research sources.

### EF-001 — Institutional Research Orientation

**Assessment date:** 2026-11-20  
**Assessment type:** Manual source comparison  
**Subject:** Public research orientation  
**Scope:** One README sentence against two research sources

**Source statement:** `profile/README.md` — I. Orientation

> The program investigates how knowledge is constituted, structured, related, represented, and made operative—across theoretical, computational, and human domains.

#### Method

Direct comparison of the selected public statement with two available internal research descriptions.

#### Finding

The selected public statement is substantially consistent with two available internal research descriptions.

These sources provide substantial support for the sentence as a description of research direction.

It characterizes the program's investigative direction without asserting that its research outcomes have been completed or independently validated.

The reviewed sources do not establish that each research direction has been completed, empirically validated, or implemented.

#### Reading

**Status:** Provisionally Supported

**Prior duplicate wording:** Provisionally Aligned. This is normalized here to EF-001's recorded status without changing the finding.

**Evidence:** Two internal working references, not presently available for public inspection.

**Public verification:** Pending

**Limitations:**

- Current canonical authority has not been confirmed.
- One reviewed source is provisional.
- Independent verification has not been established.
- Assessment applies only to the selected statement.

**Disposition:** Retain the existing wording.

**Recommendation:** Retain the sentence for now.

**Next action:** Confirm the current authoritative research reference and identify supporting material suitable for public citation.

**Next review trigger:** Confirmation or revision of the authoritative institutional research statement.

---

## Register 03 · Continuity & Drift

**State:** Unassessed

**Scope:** Public GitHub profile

**Purpose:** Identify significant discrepancies between published descriptions and approved research references.

**Evidence:** Not yet registered.

EF-001 is an epistemic source comparison. It does not establish a longitudinal measure of continuity or drift.

---

## Register 04 · Dependency Readiness

**State:** Unassessed

**Purpose:** Identify verified prerequisites and blockers to the next selected operational task.

**Evidence:** Not yet registered.

---

## V. Implementation

**Authorized signal:** [meta-gauge-mg-001.json](./signals/meta-gauge-mg-001.json)

**Renderer:** [render_meta_gauge.py](../scripts/render_meta_gauge.py)

**Generated SVG:** [meta-gauge-current.svg](./assets/meta-gauge-current.svg)

**Generated mobile PNG:** [meta-gauge-current.png](./assets/meta-gauge-current.png)

**Preserved v0.1 SVG:** [meta-gauge-v0.1.svg](./assets/meta-gauge-v0.1.svg)

**Preserved v0.1 mobile PNG:** [ascendancy-meta-gauge-v0.1-mobile.png](./assets/ascendancy-meta-gauge-v0.1-mobile.png)

**Current state:** EF-001 drives the Epistemic Fix display. The other three registers retain unknown or unassessed states. No live telemetry is represented.

The renderer transforms already recorded readings. It does not evaluate the research, approve findings, or change their evidentiary status.

### Legacy renderer limitation

The MG-001 v0.2 renderer is a bounded, source-driven **label renderer**. It validates the authorized EF-001 record and deterministically substitutes status, source, and date text into the preserved v0.1 SVG. Its circular illustration does not change geometry in response to the signal. It therefore remains an incomplete prototype of a measurement gauge, even though its evidence handling is deliberately constrained and useful.

The EF-001 assessment, signal JSON, original and generated SVG/PNG files, Python renderer, tests, and GitHub Actions workflow remain preserved as the authoritative record of that implementation. They are retained for history, source integrity, and regression testing until a reviewed replacement demonstrates equivalent or stronger safeguards.

### Experimental spatial implementation

GMG-A renders independently posed ring planes with front-hemisphere occlusion, ring-attached markers, camera-independent ring geometry, and a movable observer-relative reticle. The interactive and static GMG-A views consume the same explicit state file and orthographic projection.

That state is a geometric simulation. It is not generated from EF-001, and it does not claim alignment, coherence, confidence, direction, or research telemetry. Target lock and two-target comparison remain proposed capabilities rather than completed functions.

[Versioned reference pose](https://github.com/Ascendancy-Systems/meta-gauge/blob/main/config/gmg-a-reference-pose-v0.2.json) · [GMG-A Working Draft v0.2](https://github.com/Ascendancy-Systems/meta-gauge/blob/main/specifications/GMG-A_spatial_perceptual_relational_specification_working_draft_v0.2.md)

---

## Operating Principle

Unknown states remain visible.

Readings require source identification, assessment method, review date, and supporting evidence.

No numerical measurement may be published without a defined and validated method.

---

*An instrument reveals what may be known from its sources; it does not manufacture certainty.*

*The instrument does not establish truth. It reports what can be established from its sources.*
