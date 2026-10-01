# Implementation provenance

The supplied v0.2.0 archive contained route and experimental modules, two
synthetic inputs and twenty unit tests. The route module is a later executable
reproduction of an earlier spreadsheet screening calculation. The experimental
module is a later reproduction of tabulated arithmetic from a historical
Python-to-Excel workflow. These are not new statistical or physical algorithms.

The original Python script was inspected during preparation. It used
python-docx to read tables, Python statistics for means/sample SD, XML/math/
datetime for GPS, matplotlib for figures, and artifact_tool for spreadsheet
export. Most comparative workbook cells contain precomputed values rather than
Excel formulas. The current package does not rerun that original authoring
pipeline and does not preserve figure styling or create Excel charts.

The original script omitted missing observations in its helper and reported
percentage differences for Celsius. The later experimental implementation
requires complete comparison triplets and reports absolute temperature
differences only. Those are explicit methodological corrections, not changes
to the preserved original workbook.

Candidate 0.3.0rc1 adds a reusable GPS implementation based on the inspected
historical equations, with stricter structural checks, and a new optional
fuel-cost module. No upstream OBD fitting implementation has been recovered.
No runtime changes to the v0.2.0 route/experimental core were required for this
candidate. Documentation and package version metadata have changed.

Confidential source hashes, input mapping and reproduction results are kept
in the separate private verification annex. Public examples contain no campaign
results. Actual project reproduction and synthetic tests verify numerical
consistency; they do not validate the model against a common-route experiment.

## Source package 0.3.0

Prepared on 1 October 2026 from the user-supplied GitHub source archive.
The archive comment identifies the base commit as
`9d5eb12ef495479c274dd72dd7af9c4277f10fa9`.
This identifies the incoming snapshot, not the commit of version 0.3.0.

The update changes licence, documentation, citation and version metadata.
All calculation modules other than the package version declaration, all tests
and all synthetic inputs remain byte-for-byte identical to that snapshot.
Fresh checks use synthetic inputs only. The earlier private reproduction
record is retained as historical evidence; it has not been rerun for 0.3.0.
D2.8's recorded v0.2.0 calculations must retain their original provenance.
The later public source is a methods reference, not a replacement execution
record for results obtained with an earlier version.
