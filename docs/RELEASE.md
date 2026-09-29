# Preparing the GitHub release

This candidate has not been uploaded to GitHub. It is a reviewable source tree,
not a licence grant or confirmation of consortium publication approval.

1. Review the code and methodology against the final D2.8 interpretation.
2. Confirm the responsible repository owner, software contributors and rights
   to release code/documentation. Deliverable authors are not automatically
   software authors. Choose the licence and replace LICENSE_STATUS.md with the
   appropriate confirmed text; update README and CITATION.cff.
3. Review the source-only archive for confidential material. Do not publish the
   outer preparation bundle or its private verification annex. Exclude private
   inputs, outputs, source hashes and attachments from all git history.
4. Run all synthetic commands and tests, record the interpreter and exact files.
5. If partner feedback changes methods, increment the candidate and rerun the
   affected checks. An agreed stable release may use 0.3.0; do not cite it until
   actually created and checked.
6. Publish the reviewed source tree under the chosen account/organisation. Create
   a fixed version tag and release. Check access and download from that release.
7. Replace provisional contributor metadata, set the real release URL and date
   in CITATION.cff, and optionally obtain an archive DOI. Do not invent a DOI.
8. Add the verified version-specific reference to D2.8. State which modules and
   versions were actually executed. The new cost module is optional and must not
   be described as used in an earlier draft that did not contain it.

Suggested citation structure (complete only with real publication metadata):
Confirmed contributors (year). OLGA T2.5 reproducible calculation methods,
version [released version], [actual version-specific URL or DOI].

Suggested report wording after verification: "The descriptive processing and
empirical route calculations were reproduced using [software and version].
The public source contains methodology and synthetic examples. Campaign inputs
are confidential and are held separately by the project."
