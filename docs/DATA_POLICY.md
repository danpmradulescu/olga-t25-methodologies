# Evidence and confidentiality

Use four evidence classes: measured, derived, modelled and external-reference.
Synthetic examples form a separate demonstration class and are never project
measurements. Unit conversion does not change the evidence class of an input.

The public candidate contains algorithms, formulas, limitations, synthetic
inputs and checks. It contains no actual Testo readings, vehicle consumption
nodes, original KML tracks, project workbooks, private reproduction outputs,
partner messages, or D2.8 text. Modelled quantities derived from confidential
measurements are also excluded from the public examples.

Confidential project runs must be kept outside the repository. The examples
are not anonymised project data: they were constructed for demonstration.
Execution output hashes support traceability but do not prove measurement
quality. Hashes and private filenames also need a disclosure decision before
publication; the private verification archive must never be pushed.

The ignore file is a convenience, not access control. Check all staged files
and git history before making any repository public. This supplied candidate
contains no git history. Do not upload the outer preparation bundle or its
private annex to a public repository. Publish only the reviewed source archive.

Original measurements, calibrations and rights to release results remain with
the responsible project organisations. Public methods alone allow inspection
and synthetic execution; exact OLGA reproduction requires authorised private
inputs. Do not call this unrestricted public reproducibility of the dataset.
