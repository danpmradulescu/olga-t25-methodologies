# Publish and cite version 0.3.0

This source package is ready for upload to the existing repository. Its
preparation date is 1 October 2026. Upload, public access and a GitHub release
have not been verified by the local checks. The source archive does not
create a remote commit, tag, release or DOI.

## Upload the source

1. Unpack the source ZIP. In the existing GitHub repository use **Add file >
   Upload files** from its root. Upload the contents of the unpacked folder,
   preserving `docs/`, `examples/`, `olga_route_model/` and `tests/`. Do not
   upload the ZIP itself or create an extra enclosing directory.
2. Replace the matching paths. Include the new `LICENSE` file. If the file
   picker hides `.gitignore`, keep the existing file: it is unchanged. Review
   the changed-file list before committing. No confidential project files or
   local run outputs belong in this upload.
3. Suggested commit message: `Prepare v0.3.0 with MIT licence and verified examples`.
4. Check the root README, `LICENSE`, `CITATION.cff` and package version on
   GitHub. Run the README commands on a fresh download if uploaded file
   contents differ from this package.

The SHA256SUMS.json file covers every distributed source file other than
itself. Local output folders and Python caches are excluded. Any later edit
to a listed file requires regenerating its checksum before freezing a release.

## Freeze the reference

1. From the final reviewed commit, create a GitHub release with tag `v0.3.0`
   and title `OLGA T2.5 reproducible calculation methods 0.3.0`.
2. The release description should mention the MIT licence, four calculation
   modules and synthetic examples. State that experimental data are excluded
   and that this is a methodology reference, not independent model validation.
3. Verify that the repository, tag and downloadable source are accessible
   to the intended readers. A private repository cannot be described as a
   publicly accessible methods reference.
4. Copy the actual tag URL and full commit SHA. Do not reuse the incoming
   archive's base commit as the identifier of this updated source.
5. In D2.8 use the verified link and access date. No DOI is assigned here.

CITATION.cff names Dan Radulescu for this software citation. This does not
replace or redefine the COMOTI, TUCN and T5.1 author/contributor list in D2.8.
No release date or invented version-specific URL is included before actual
publication.

## D2.8 reference after publication

Use the following structure, replacing the bracketed fields with the actual
GitHub metadata only after verification:

Radulescu, D. (2026). OLGA T2.5 reproducible calculation methods, version
0.3.0 [software]. GitHub. [Verified tag URL]. Commit: [full SHA]. MIT License.
Accessed [date].

Describe this as the public source for the methodology. Retain the original
v0.2.0 calculation record and private reproduction bundle where they support
existing numerical results. Do not claim that 0.3.0 produced those results
unless the corresponding authorised inputs have actually been rerun with it.

A suitable methods statement after public access has been checked is:

"The calculation methods and synthetic examples are available in the
versioned OLGA T2.5 methodology repository under the MIT License. Experimental
inputs and project reproduction records are held separately under the
project's confidentiality arrangements."
